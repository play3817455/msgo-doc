# -*- coding: utf-8 -*-
"""
战服报文：为每条 recv/send 补上「处理者（业务回调）+ 解析序列摘要」，产出交互总表。
- recv：case 尾部 `mov edx,[esi]; mov edx,[edx+OFFh]; <push...> call edx` ⇒ vt 槽 OFF（vtable 基址 0xEED7AC）
        ⇒ thunk（可跟 jmp）⇒ impl VA
- 解析序列：case 入口 → dump 头之间的读取器调用序列（宽度映射见 READ/W0/VAR）
产物：
  formats/battle_handlers.json      机读
  formats/battle-交互总表.md         人读（合并 报文/闸门/体长/字段/处理者/解析序列）
"""
import idc
import idautils
import json
import os
import re
from collections import Counter

FMT = r"f:\9ymsgo\9you\reverse-login-chain\formats"
RAW = os.path.join(FMT, "battle_protocol_raw.json")
BL = os.path.join(FMT, "battle_bodylen.json")
OUT = os.path.join(FMT, "battle_handlers.json")
MD = os.path.join(FMT, "battle-交互总表.md")
VT = 0xEED7AC              # CGVOProtoBattle vtable（+0x54 = 分发器）

READ = {                   # 读取器 → 线上宽度
    "sub_B02DD0": 4, "sub_B02DF0": 2, "sub_B06230": 1,
    "sub_B41470": 0, "sub_B413B0": 0, "sub_B05E30": 0,
}
VAR = {
    "sub_B02BA0": "str(cap)", "sub_B02B40": "str(cap)", "sub_B02E20": "u32+定长串",
    "sub_B02D30": "间接", "sub_B077B0": "复合u16+", "sub_B07880": "复合u32+", "sub_B08160": "复合u16+",
    "sub_B05EA0": "循环", "sub_B418C0": "跳读40", "sub_B05ED0": "跳读64", "sub_B05EE0": "跳读516",
    "sub_B02D80": "写u32", "sub_B02DA0": "写u16", "sub_B061C0": "写u8",
}

def insn(ea):
    return idc.generate_disasm_line(ea, 0) or ""

def mnem(ea):
    return idc.print_insn_mnem(ea)

def opnd(ea, n):
    return idc.get_operand_value(ea, n)

def follow_jmp(ea):
    """若 ea 处是 jmp，跟到底（最多 4 跳）"""
    for _ in range(4):
        if ea == idc.BADADDR or mnem(ea) != "jmp":
            return ea
        t = opnd(ea, 0)
        if t == idc.BADADDR or t == ea:
            return ea
        ea = t
    return ea

def vt_impl(off):
    if off is None:
        return None, None
    thunk = idc.get_wide_dword(VT + off)
    impl = follow_jmp(thunk)
    return thunk, impl

def callees(fn_ea, maxn=12):
    """函数的一级被调（仅属于本函数体的代码引用）"""
    res = []
    if fn_ea is None:
        return res
    for x in idautils.XrefsTo(fn_ea):
        if x.type not in (idc.fl_CN, idc.fl_CF):
            continue
        if idc.get_func_attr(x.frm, idc.FUNCATTR_START) != fn_ea:
            continue
        nm = idc.get_func_name(x.frm)
        if nm and nm not in res:
            res.append(nm)
        if len(res) >= maxn:
            break
    return res

def count_args(call_ea):
    n = 0
    cur = call_ea
    for _ in range(80):
        cur = idc.prev_head(cur)
        if cur == idc.BADADDR:
            break
        m = mnem(cur)
        if m in ("call", "jmp"):
            break
        if m == "push":
            n += 1
    return n

def tail_call(ent, limit):
    """在 [ent, limit) 里找"最后一次 经 vtable 槽 的间接调用"= 业务回调"""
    cands = []
    pending = {}
    cur = ent
    while cur != idc.BADADDR and cur < limit:
        d = insn(cur)
        mm = re.match(r"mov\s+(\w+),\s*\[(\w+)\+([0-9A-Fa-f]+)h\]", d)
        if mm and mm.group(1) == mm.group(2):
            pending[mm.group(1)] = int(mm.group(3), 16)
        if mnem(cur) == "call" and idc.get_operand_type(cur, 0) == idc.o_reg:
            reg = (idc.print_operand(cur, 0) or "").strip()
            if reg in pending:
                cands.append((cur, pending[reg], count_args(cur)))
                pending.pop(reg, None)
        cur = idc.next_head(cur)
    if not cands:
        return None, 0, None
    return cands[-1]

def parse_seq(ent, site):
    seq, loops, alloc = [], False, None
    reader_addrs = set()
    cur = ent
    while cur != idc.BADADDR and cur < site:
        m = mnem(cur)
        if m == "push" and idc.get_operand_type(cur, 0) == idc.o_imm:
            nx = idc.next_head(cur)
            if alloc is None and nx != idc.BADADDR and mnem(nx) == "call" \
                    and idc.get_operand_type(nx, 0) == idc.o_reg:
                alloc = opnd(cur, 0)
        if m == "call":
            callee = insn(cur).split()[-1]
            if callee in READ:
                seq.append(callee); reader_addrs.add(cur)
            elif callee in VAR:
                seq.append(callee + "?"); reader_addrs.add(cur)
        if m.startswith("j") and idc.get_operand_type(cur, 0) == idc.o_near:
            t = opnd(cur, 0)
            if t < cur and t in reader_addrs:
                loops = True
        cur = idc.next_head(cur)
    return seq, loops, alloc

raw = json.load(open(RAW, encoding="utf-8"))
bl = {}
for r in json.load(open(BL, encoding="utf-8")):
    bl[r["name"]] = r

def seq_str(seq, loops):
    c = Counter(seq)
    parts = []
    for k in sorted(c, key=lambda x: -c[x]):
        n = c[k]
        base = k.replace("sub_", "")
        w = READ.get(k)
        lab = VAR.get(k, "")
        if w:
            lab = "u%d" % (w * 8)
        parts.append("%s×%d(%s)" % (base, n, lab))
    if loops:
        parts.append("★循环")
    return " ".join(parts) if parts else "-"

out = {"recv": [], "send": []}
recv_entries = sorted(int(x["entry"], 16) for x in raw["recv"] if x["entry"])
import bisect
for r in raw["recv"]:
    ent = int(r["entry"], 16) if r["entry"] else None
    site = int(r["site"], 16)
    rec = dict(r)
    if ent:
        j = bisect.bisect_right(recv_entries, ent)
        nxt = recv_entries[j] if j < len(recv_entries) else ent + 0x800
        limit = min(nxt, ent + 0x1800)
        call, off, npush = tail_call(ent, limit)
        thunk, impl = vt_impl(off)
        seq, loops, alloc2 = parse_seq(ent, site)
        rec.update({"vt_off": ("0x%X" % off) if off else None,
                    "vt_thunk": idc.get_func_name(thunk) if thunk else None,
                    "handler": idc.get_func_name(impl) if impl else None,
                    "handler_va": hex(impl) if impl else None,
                    "handler_callees": callees(impl),
                    "args": npush,
                    "seq": seq, "seq_str": seq_str(seq, loops), "loop": loops})
    b = bl.get(r["name"], {})
    rec["alloc"] = b.get("alloc")
    rec["sum_fixed"] = b.get("sum_fixed")
    rec["verdict"] = b.get("verdict")
    out["recv"].append(rec)

for r in raw["send"]:
    rec = dict(r)
    fn = int(r["func_addr"], 16)
    fn_end = idc.get_func_attr(fn, idc.FUNCATTR_END)
    seq, loops, alloc2 = parse_seq(fn, fn_end)
    rec.update({"seq": seq, "seq_str": seq_str(seq, loops), "loop": loops})
    b = bl.get(r["name"], {})
    rec["verdict"] = b.get("verdict")
    out["send"].append(rec)

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- Markdown ----------------
recv_ok = sorted([r for r in out["recv"] if r["id"]], key=lambda r: r["id"])
send_ok = sorted([r for r in out["send"] if r["id"]], key=lambda r: r["id"])
L = ["# 战服报文 · 交互总表（ID / 闸门 / 体长 / 字段 / 处理者 / 解析序列）\n",
     "> 生成：`tools/dump_battle_protocol.py` + `tools/battle_bodylen.py` + `tools/battle_handlers.py`（可重跑）。",
     "> `处理者` = 收包 case 尾部 `call vt[OFF]` 经 thunk 跟到的实现；`解析序列` = case 入口→dump 头之间的读取器调用（u32/u16/u8/变长）。",
     "> `体长` 判据见 `battle-体长线索.md`（143/205 三条验证）。\n",
     "## 0. 规模\n",
     "| 项 | 值 |", "|---|---|",
     "| S→C | %d 条 |" % len(recv_ok),
     "| C→S | %d 条 |" % len(send_ok),
     "| 体长已定（★定长） | %d 条 |" % len([r for r in recv_ok if str(r.get("verdict", "")).startswith("★")]),
     "| 解析含循环/变长 | %d 条 |" % len([r for r in recv_ok if r.get("loop") or any("?" in s for s in r.get("seq", []))]),
     ""]
L.append("## 1. S→C 全表\n")
L.append("| ID | 报文 | 闸门 | 体长 | 处理者(impl) | 参数数 | 解析序列 | 处理者一级被调 | 字段（序） |")
L.append("|---|---|---|---|---|---|---|---|---|")
for r in recv_ok:
    L.append("| `%s` | %s | %s | %s | `%s` | %s | %s | %s | %s |" % (
        r["id_hex"], r["name"], r["gate_index"], r.get("verdict", "-"),
        r.get("handler") or "-", r.get("args"),
        r.get("seq_str", "-"),
        " ".join(r.get("handler_callees", [])[:6]) or "-",
        " ".join(f["name"] for f in r["fields"]) if r["fields"] else "-"))
L.append("")
L.append("## 2. C→S 全表\n")
L.append("| ID | 报文 | 发送函数 | 解析/打包序列 | 字段（序） |")
L.append("|---|---|---|---|---|")
for r in send_ok:
    L.append("| `%s` | %s | `%s` | %s | %s |" % (
        r["id_hex"], r["name"], r["func"], r.get("seq_str", "-"),
        " ".join(f["name"] for f in r["fields"]) if r["fields"] else "-"))

# ---------- 3. 生命周期分组 ----------
STAGES = [
    ("S1 连接/握手", ("proto_version", "authenticate", "cpf_")),
    ("S2 房间大厅", ("roomlobby", "room_")),
    ("S3 开局/出击", ("game_", "msma_spawn", "entity_deploy", "entity_msma_show", "braodcast")),
    ("S4 实体同步", ("entity_", "pos_warp", "funnel_", "weapon_state", "active_weapon", "eqparts")),
    ("S5 开火/弹道", ("weapon_fire", "bullet_", "wrestle_")),
    ("S6 命中/伤害/死亡", ("weapon_hit", "shield_", "module_", "repair_", "entity_msma_dead",
                            "entity_msma_reborn", "entity_msma_hide", "entity_msma_disappear")),
    ("S7 得分/进度", ("score_", "kill_", "game_round", "mission_", "battle_contribute", "area_", "conquer", "system_")),
    ("S8 指挥官/战术", ("commander_", "combat_operation", "dynamic_taskforce")),
    ("S9 NPC AI 托管", ("msma_AI",)),
    ("S10 载具/道具", ("battleship", "rideable", "itembox", "preset_voice", "cutin", "map_event", "chara")),
    ("S11 其它", ()),
]

def stage_of(name):
    for st, pres in STAGES:
        for p in pres:
            if name.startswith(p):
                return st
    return "S11 其它"

L.append("")
L.append("## 3. 生命周期分组（把 287 条按战斗流程归位）\n")
grp = {}
for r in recv_ok:
    grp.setdefault(stage_of(r["name"]), []).append(("recv", r))
for r in send_ok:
    grp.setdefault(stage_of(r["name"]), []).append(("send", r))
for st, _ in STAGES:
    items = grp.get(st)
    if not items:
        continue
    L.append("### %s（%d 条）\n" % (st, len(items)))
    L.append("| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |")
    L.append("|---|---|---|---|---|---|")
    for d, r in sorted(items, key=lambda x: x[1]["id"] or 0):
        if d == "recv":
            L.append("| S→C | `%s` | %s | %s / %s参 | `%s` | %s |" % (
                r["id_hex"], r["name"], r.get("verdict", "-"), r.get("args"),
                r.get("handler") or "-", " ".join(f["name"] for f in r["fields"]) or "-"))
        else:
            L.append("| C→S | `%s` | %s | - | `%s`(发送) | %s |" % (
                r["id_hex"], r["name"], r["func"], " ".join(f["name"] for f in r["fields"]) or "-"))
    L.append("")
open(MD, "w", encoding="utf-8").write("\n".join(L) + "\n")

noh = [r["name"] for r in recv_ok if not r.get("handler")]
offc = Counter(r.get("vt_off") for r in recv_ok)
print("recv=%d send=%d  有处理者=%d  无处理者=%d" %
      (len(recv_ok), len(send_ok), len(recv_ok) - len(noh), len(noh)))
print("vt 槽分布 top10:", offc.most_common(10))
print("无处理者:", noh[:12])
for probe in ("weapon_hit_from", "authenticate_r", "game_begin", "score_update",
              "entity_msma_show_hp", "entity_snapshot_splitdelta_compress"):
    for r in recv_ok:
        if r["name"] == probe:
            print("  %-34s %s vt=%s 参数=%s → %s | %s" %
                  (probe, r["id_hex"], r.get("vt_off"), r.get("args"),
                   r.get("handler"), r.get("seq_str")[:70]))

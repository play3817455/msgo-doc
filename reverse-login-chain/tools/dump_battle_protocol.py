# -*- coding: utf-8 -*-
"""
批量提取 _proto_battle_client 收/发报文清单（v5 —— 补齐 switch 跳转表 + 闸门 + 出文档）
recv ID 来源：sub_B0CC20 分派器
  ① 二叉查找（cmp eax,IMM / jg / jz）
  ② 稀疏残段（sub eax,IMM 累加 + jz / jnz default）
  ③ switch 跳转表（sub eax,BASE; cmp eax,N; ja def; movzx eax,byte_TBL[eax]; jmp jpt[eax*4]）
send ID：发送函数内（限函数范围）第一个 word 立即数存储。
字段：dump 头之后的 `push offset aXXX; "字段名="` + 紧随的 dump 助手（类型线索）。
产物：
  reverse-login-chain/formats/battle_protocol_raw.json   （机读全量）
  reverse-login-chain/formats/battle-报文总表.md           （人读总表）
  reverse-login-chain/formats/_battle_dispatch_diag.txt    （分派器解析诊断）
"""
import idc
import idautils
import json
import bisect
import os
import re

FMT = r"f:\9ymsgo\9you\reverse-login-chain\formats"
OUT = os.path.join(FMT, "battle_protocol_raw.json")
MD = os.path.join(FMT, "battle-报文总表.md")
DIAG = os.path.join(FMT, "_battle_dispatch_diag.txt")
DISP = 0xB0CC20
DEND = idc.get_func_attr(DISP, idc.FUNCATTR_END)

# dump 助手 → 类型线索（实测：B03580=4B数值 / B032A0=2B数值(按注册 flags 0x400 无符号 0x800 有符号)
# B03420=2B数值 / B08500=8B数值 / B0C1F0=1B / B036E0|B02D30=变长/字节串）
TYPE_HINT = {
    "sub_B03580": "i32",
    "sub_B032A0": "i16/u16",
    "sub_B03420": "i16(2B)",
    "sub_B08500": "i64",
    "sub_B0C1F0": "u8/bool",
    "sub_B061C0": "u8/bool",
    "sub_B036E0": "var",
    "sub_B02D30": "var/bytes",
    "sub_B02D80": "u16",
    "sub_B02DA0": "u32",
    "sub_B02DD0": "u32",
    "sub_B02DF0": "u16",
}


def insn(ea):
    return idc.generate_disasm_line(ea, 0) or ""


def mnem(ea):
    return idc.print_insn_mnem(ea)


def opnd(ea, n):
    return idc.get_operand_value(ea, n)


def otext(ea, n):
    return (idc.print_operand(ea, n) or "").strip()


def is_cmp_eax(ea):
    if ea == idc.BADADDR:
        return False
    d = insn(ea)
    return d.startswith("cmp ") and d[4:].split(",", 1)[0].strip() == "eax"


case_id, bails = {}, []


def add(addr, cid, how):
    if addr in case_id and case_id[addr][0] != cid:
        bails.append("CONFLICT %08X: %s vs %s" % (addr, case_id[addr][0], cid))
    case_id.setdefault(addr, (cid, how))


def try_switch(ea, base):
    """ea 指向 `cmp eax, N`：判断是否为 switch 跳转表；是则登记并返回 True"""
    if mnem(ea) != "cmp" or otext(ea, 0) != "eax":
        return False
    n = opnd(ea, 1)
    j = idc.next_head(ea)
    if mnem(j) not in ("ja", "jbe", "jae", "jb"):
        return False
    m2 = idc.next_head(j)
    if mnem(m2) != "movzx" or "byte_" not in insn(m2):
        # 变体：movzx 可能不在下一条
        for _ in range(2):
            m2 = idc.next_head(m2)
            if mnem(m2) == "movzx":
                break
    if mnem(m2) != "movzx":
        return False
    tbl = opnd(m2, 1) if "byte_" in insn(m2) else None
    jmp = None
    cur = m2
    for _ in range(3):
        cur = idc.next_head(cur)
        if mnem(cur) == "jmp":
            jmp = cur
            break
    if tbl is None or jmp is None:
        return False
    jpt = opnd(jmp, 0)
    if not (0x400000 < tbl < 0x1200000 and 0x400000 < jpt < 0x1200000):
        return False
    # 找到 default 槽（byte 值最多的那个）
    vals = {}
    for i in range(n + 1):
        b = idc.get_wide_byte(tbl + i)
        vals.setdefault(b, []).append(i)
    dslot = max(vals, key=lambda k: len(vals[k])) if vals else None
    cnt = 0
    for i in range(n + 1):
        b = idc.get_wide_byte(tbl + i)
        if b == dslot:
            continue
        tgt = idc.get_wide_dword(jpt + b * 4)
        if not (DISP <= tgt <= DEND):
            continue
        add(tgt, base + i, "switch")
        cnt += 1
    bails.append("SWITCH %08X base=0x%04X n=%d slots=%d default=%s"
                 % (ea, base, n, cnt, dslot))
    return True


def walk(ea, lo, hi, depth=0):
    if depth > 90 or ea == idc.BADADDR:
        return
    cur, low, high, sb = ea, lo, hi, 0
    guard = 0
    while guard < 800:
        guard += 1
        if cur == idc.BADADDR:
            return
        if is_cmp_eax(cur):
            sb = 0
            imm = opnd(cur, 1)
            n1 = idc.next_head(cur)
            m1 = mnem(n1)
            if m1 in ("jg", "ja"):
                T = opnd(n1, 0)
                n2 = idc.next_head(n1)
                if mnem(n2) in ("jz", "je"):
                    add(opnd(n2, 0), imm, "jz")
                    walk(T, imm + 1, high, depth + 1)
                    high = imm - 1
                    cur = idc.next_head(n2)
                    if high < low:
                        return
                    continue
                walk(T, imm + 1, high, depth + 1)
                high = imm
                cur = n2
                continue
            if m1 in ("jl", "jb"):
                T = opnd(n1, 0)
                n2 = idc.next_head(n1)
                if mnem(n2) in ("jz", "je"):
                    add(opnd(n2, 0), imm, "jz-after-jl")
                    walk(T, low, imm - 1, depth + 1)
                    low = imm + 1
                    cur = idc.next_head(n2)
                    if low > high:
                        return
                    continue
                walk(T, low, imm - 1, depth + 1)
                low = imm
                cur = n2
                continue
            if m1 in ("jz", "je"):
                add(opnd(n1, 0), imm, "jz")
                high = imm - 1
                cur = idc.next_head(n1)
                if high < low:
                    return
                continue
            if m1 in ("jnz", "jne"):
                add(idc.next_head(n1), imm, "fallthrough")
                return
            bails.append("BAIL-cmp %08X %s" % (cur, insn(cur)))
            return
        if mnem(cur) == "sub" and otext(cur, 0) == "eax":
            sb += opnd(cur, 1)
            n1 = idc.next_head(cur)
            if try_switch(n1, sb):
                return
            m1 = mnem(n1)
            if m1 in ("jz", "je"):
                add(opnd(n1, 0), sb, "sub-jz")
                cur = idc.next_head(n1)
                continue
            if m1 in ("jnz", "jne"):
                add(idc.next_head(n1), sb, "sub-fallthrough")
                return
            cur = n1
            continue
        if high == low:
            add(cur, high, "direct")
        else:
            bails.append("RANGE %08X hi=%s lo=%s" % (cur, high, low))
        return


walk(0xB0CCAD, 0, 0xFFFF)
starts = sorted(case_id.keys())

# ---------- dump 串 ----------
recv_strings, send_strings, core = [], [], []
for s in idautils.Strings():
    t = str(s)
    if "::recv_" not in t and "::send_" not in t:
        continue
    if "_proto_battle_client" in t:
        d = "recv" if "::recv_" in t else "send"
        nm = t.split("::" + d + "_", 1)[1].split("(", 1)[0].strip()
        if nm:
            (recv_strings if d == "recv" else send_strings).append((nm, s.ea, t))
    elif "_proto_battle::" in t:
        d = "recv" if "::recv_" in t else "send"
        nm = t.split("::" + d + "_", 1)[1].split("(", 1)[0].strip()
        if nm:
            core.append((nm, s.ea, t, d))


def field_name(str_ea):
    t = idc.get_strlit_contents(str_ea, -1, 0)
    if not t:
        return None
    t = t.decode("utf-8", "ignore") if isinstance(t, bytes) else t
    t = t.strip()
    if t.endswith('="'):            # 字符串字段：room_name="
        return t[:-2]
    if t.endswith("{"):
        return t[:-1].rstrip("= ").rstrip() + "[]"
    if t.endswith("="):
        return t[:-1]
    return None


def scan_fields(site, limit):
    """字段名由 dump 拼接给出。
    形态 A（值带 '=' 后缀）：push offset aFrameCount("frame_count=")
    形态 B（名与值分开）：push offset aRoomName("room_name") + push offset asc_EDAD54("=") + 值
    类型线索 = 该字段名之后、下一个字段名之前的第一个 TYPE_HINT 助手。"""
    seq = []          # [(insn_ea, text|None, str_ea|None)]
    cur = idc.next_head(site)
    while cur != idc.BADADDR and cur < limit:
        d = insn(cur)
        if d.startswith("push") and "offset" in d:
            tgt = opnd(cur, 0)
            t = idc.get_strlit_contents(tgt, -1, 0)
            if t:
                t = t.decode("utf-8", "ignore") if isinstance(t, bytes) else t
                if "_proto_" in t:
                    break
                seq.append((cur, t, tgt))
        elif d.startswith("call "):
            seq.append((cur, None, None))
        cur = idc.next_head(cur)
    fields, pending, calls = [], None, []
    for i, (ea, t, sea) in enumerate(seq):
        if t is None:
            calls.append(insn(ea).split()[-1])
            continue
        nxt = seq[i + 1][1] if i + 1 < len(seq) else None
        prv = seq[i - 1][1] if i > 0 else None
        SEPS = ("=", " =", ":", '"', '="')
        # 形态 B：分隔符可出现在名字前（dump 串值写法：<值>'"'" <名字>）或后（<名字>"=" <值>）
        is_sep = (nxt is not None and nxt.strip() in SEPS) or \
                 (prv is not None and prv.strip() in SEPS)
        # 只接受"像字段名"的串（字母/下划线开头）
        ok_name = re.match(r"^[A-Za-z_][A-Za-z0-9_]{1,39}$", t.strip()) is not None
        fn = field_name(sea)
        if fn:
            if pending is not None:
                fields.append({"name": pending, "hint": pick_hint(calls)})
            pending, calls = fn, []
        elif is_sep and ok_name:
            # 形态 B：名字串 + "=" 分隔
            if pending is not None:
                fields.append({"name": pending, "hint": pick_hint(calls)})
            pending, calls = t.strip(), []
    if pending is not None:
        fields.append({"name": pending, "hint": pick_hint(calls)})
    return fields


def pick_hint(calls):
    for c in calls:
        if c in TYPE_HINT:
            return TYPE_HINT[c]
    return "?"


def find_gate(ent, site):
    cur = ent
    while cur is not None and cur < site:
        d = insn(cur)
        if d.startswith("call") and ("sub_B41120" in d or "sub_B05DA0" in d):
            p = cur
            for _ in range(4):
                p = idc.prev_head(p)
                if p == idc.BADADDR:
                    break
                if mnem(p) == "push" and idc.get_operand_type(p, 0) == idc.o_imm:
                    return opnd(p, 0), d.split()[-1]
                if mnem(p) in ("call", "jmp"):
                    break
        cur = idc.next_head(cur)
    return None, None


def send_id_first(fn, fn_end):
    cur = fn
    while cur != idc.BADADDR and cur < fn_end:
        d = insn(cur)
        if mnem(cur) in ("mov", "movzx") and "word ptr" in d and "," in d:
            op1 = d.split(",", 1)[1].strip()
            v = None
            if op1.endswith("h"):
                try:
                    v = int(op1[:-1], 16)
                except ValueError:
                    v = None
            if v and 0x0001 <= v <= 0xFFFF:
                return cur, v
        cur = idc.next_head(cur)
    return None, None


out = {"recv": [], "send": [], "core": [], "unmatched": [],
       "meta": {"dispatcher": hex(DISP), "dispatcher_end": hex(DEND)}}

for nm, sea, raw in recv_strings:
    for site in [x.frm for x in idautils.XrefsTo(sea)]:
        if not (DISP <= site <= DEND):
            out["unmatched"].append({"name": nm, "kind": "recv", "site": hex(site),
                                     "fn": idc.get_func_name(site)})
            continue
        i = bisect.bisect_right(starts, site) - 1
        ent = starts[i] if i >= 0 else None
        cid, how = case_id.get(ent, (None, None))
        if ent is None or (site - ent) > 0x4000:
            cid, how, ent = None, "no-entry", None
        j = bisect.bisect_right(starts, site)
        limit = starts[j] if j < len(starts) else site + 0x2000
        gate, gate_fn = find_gate(ent, site)
        out["recv"].append({
            "name": nm, "id": cid, "id_hex": ("0x%04X" % cid) if cid else None,
            "id_from": how, "entry": hex(ent) if ent else None, "site": hex(site),
            "gate_index": gate, "gate_fn": gate_fn,
            "fields": scan_fields(site, limit),
        })

for nm, sea, raw in send_strings:
    for site in [x.frm for x in idautils.XrefsTo(sea)]:
        fn = idc.get_func_attr(site, idc.FUNCATTR_START)
        fn_end = idc.get_func_attr(site, idc.FUNCATTR_END)
        at, v = send_id_first(fn, fn_end)
        out["send"].append({
            "name": nm, "func": idc.get_func_name(fn), "func_addr": hex(fn),
            "id": v, "id_hex": ("0x%04X" % v) if v else None,
            "id_at": hex(at) if at else None,
            "fields": scan_fields(site, fn_end + 0x40),
        })

for nm, sea, raw, d in core:
    out["core"].append({"name": nm, "dir": d, "str": raw})

os.makedirs(FMT, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
with open(DIAG, "w", encoding="utf-8") as f:
    f.write("entries=%d\n" % len(starts))
    f.write("\n".join(bails))

# ---------------- Markdown ----------------
def fstr(fs):
    return " | ".join("%s:%s" % (f["name"], f["hint"]) for f in fs) if fs else "-"


recv_ok = sorted([r for r in out["recv"] if r["id"]], key=lambda r: r["id"])
send_ok = sorted([r for r in out["send"] if r["id"]], key=lambda r: r["id"])
lines = []
lines.append("# 战服（battle）报文总表 —— `_proto_battle_client`\n")
lines.append("> 自动提取：`reverse-login-chain/tools/dump_battle_protocol.py`（IDA，2026-09-15）。")
lines.append("> 机读版：`battle_protocol_raw.json`。字段**顺序**来自客户端自动生成的 dump 拼接（可靠）；")
lines.append("> `类型` 是 dump 助手给出的**线索**（i32/i16/u8/i64/var），**体长与精确类型需逐条反编译 parse 段确认**。")
lines.append("> ★**体长**见 `battle-体长线索.md`：**143/205** 条已三重验证为定长（可直接造包），其余 62 条（含变长串/数组/复合）待人工。\n")
lines.append("## 0. 概览\n")
lines.append("| 项 | 值 |")
lines.append("|---|---|")
lines.append("| 收包分发器 | `sub_B0CC20`（%s..%s）|" % (hex(DISP), hex(DEND)))
lines.append("| S→C（recv） | **%d** 条（有 ID %d） |" % (len(out["recv"]), len(recv_ok)))
lines.append("| C→S（send） | **%d** 条（有 ID %d） |" % (len(out["send"]), len(send_ok)))
lines.append("| 其它类 `_proto_battle` | %d 条（entity_msma_fix 收发）|" % len(out["core"]))
lines.append("| ID 区间 | recv %s..%s ／ send %s..%s |" %
             (recv_ok[0]["id_hex"], recv_ok[-1]["id_hex"],
              send_ok[0]["id_hex"], send_ok[-1]["id_hex"]))
lines.append("")
lines.append("## 1. ★ 战服 MVP 必做的报文（按流程）\n")
MVP = [
    ("握手", ["proto_version_check_r", "authenticate_r", "cpf_authenticate", "cpf_authenticate_error"]),
    ("大厅/房间", ["roomlobby_pilot_add", "roomlobby_pilot_del", "roomlobby_pilot_mindex_update_r",
                   "roomlobby_game_ready_r", "roomlobby_game_start_r", "roomlobby_exit_r",
                   "room_chat_down", "room_kick_vote_r"]),
    ("开局/生成", ["game_begin", "msma_spawn_list_get_r_begin", "msma_spawn_list_get_r_end",
                   "msma_spawn_select_r", "msma_spawn_warp_start_r", "msma_spawn_wait_update",
                   "entity_deploy_arms_appear"]),
    ("移动/状态同步", ["entity_snapshot", "entity_snapshot_splitdelta_compress", "pos_warp_force",
                       "entity_msma_reborn", "entity_msma_hide", "entity_msma_disappear",
                       "weapon_state_update", "active_weapon_change_r", "eqparts_toggle"]),
    ("命中/伤害/死亡", ["weapon_hit_from", "weapon_hit_from_with_stumble", "weapon_hit_from_with_tumble",
                        "weapon_hit_from_with_module", "weapon_hit_to_r", "shield_any_damage",
                        "entity_msma_show_hp", "entity_msma_dead", "module_toggle_point",
                        "module_toggle_level", "module_toggle_time", "system_message"]),
    ("得分/进度", ["score_update", "score_update_coopwave", "kill_count_update",
                   "mission_goal_text", "game_mission_progress_update", "game_round_end",
                   "battle_contribute_rank", "game_score_ranker_notice"]),
]
for title, names in MVP:
    lines.append("**%s**" % title)
    for n in names:
        r = next((x for x in out["recv"] if x["name"] == n), None)
        if r:
            lines.append("- `%s` **%s** 闸门=%s 字段: %s" %
                         (n, r["id_hex"], r["gate_index"], fstr(r["fields"])))
        else:
            lines.append("- `%s` ⚠️ 未在 recv 表找到" % n)
    lines.append("")
lines.append("## 2. S→C 全表（服务端必须能发）\n")
lines.append("| # | ID | 报文名 | 闸门 | 字段（序） |")
lines.append("|---|---|---|---|---|")
for idx, r in enumerate(recv_ok, 1):
    lines.append("| %d | `%s` | %s | %s | %s |" %
                 (idx, r["id_hex"], r["name"], r["gate_index"], fstr(r["fields"])))
lines.append("")
lines.append("## 3. C→S 全表（服务端必须能收/解析）\n")
lines.append("| # | ID | 报文名 | 发送函数 | 字段（序） |")
lines.append("|---|---|---|---|---|")
for idx, r in enumerate(send_ok, 1):
    lines.append("| %d | `%s` | %s | `%s` | %s |" %
                 (idx, r["id_hex"], r["name"], r["func"], fstr(r["fields"])))
lines.append("")
if out["unmatched"]:
    lines.append("## 4. 未落在战服分发器里的 dump 串（需人工看）\n")
    for r in out["unmatched"]:
        lines.append("- %s @ %s (%s)" % (r["name"], r["site"], r["fn"]))
with open(MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

ids = sorted(set(r["id"] for r in recv_ok))
byid = {}
for r in recv_ok:
    byid.setdefault(r["id"], []).append(r["name"])
dups = {k: v for k, v in byid.items() if len(v) > 1}
print("entries=%d recv=%d send=%d core=%d unmatched=%d diag=%d" %
      (len(starts), len(out["recv"]), len(out["send"]), len(out["core"]),
       len(out["unmatched"]), len(bails)))
print("recv id %d/%d  range %s..%s" % (len(recv_ok), len(out["recv"]),
                                       recv_ok[0]["id_hex"], recv_ok[-1]["id_hex"]))
print("send id %d/%d" % (len(send_ok), len(out["send"])))
print("dup ids: %d %s" % (len(dups), {("0x%04X" % k): v for k, v in list(dups.items())[:6]}))
print("no-id recv: %s" % [r["name"] for r in out["recv"] if not r["id"]][:12])
print("no-id send: %s" % [r["name"] for r in out["send"] if not r["id"]][:12])
print("diag: %s" % bails[:6])
for probe in ("weapon_hit_from", "weapon_hit_to_r", "entity_msma_show_hp", "score_update",
              "entity_snapshot_splitdelta_compress", "proto_version_check_r"):
    r = next((x for x in out["recv"] if x["name"] == probe), None)
    if r:
        print("  %-36s %s gate=%s nf=%d %s" %
              (probe, r["id_hex"], r["gate_index"], len(r["fields"]), fstr(r["fields"])[:90]))
for probe in ("proto_version_check", "authenticate", "weapon_hit_to", "pos_move"):
    r = next((x for x in out["send"] if x["name"] == probe), None)
    if r:
        print("  S %-34s %s nf=%d %s" %
              (probe, r["id_hex"], len(r["fields"]), fstr(r["fields"])[:90]))
print("helpers:", {k: idc.get_type(idc.get_name_ea_simple(k)) for k in
                   ("sub_B03580", "sub_B032A0", "sub_B03420", "sub_B08500", "sub_B0C1F0")})

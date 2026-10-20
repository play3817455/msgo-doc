# -*- coding: utf-8 -*-
"""
按【地址顺序】打印指定报文的解析轨迹（保留真实交错）：
  push <imm>            → 上限/计数/分配大小
  call <reader>         → u32/u16/u8/有界串/复合
  push offset aXXX      → dump 字段名（= 该字段的语义名）
  call <business>       → 业务回调（参数从后往前压栈）
输出：formats/_battle_detail_<name>.txt；同时在 stdout 打摘要
"""
import idc
import idautils
import json
import os

FMT = r"f:\9ymsgo\9you\reverse-login-chain\formats"
H = json.load(open(os.path.join(FMT, "battle_handlers.json"), encoding="utf-8"))
TARGETS = ["authenticate_r", "game_begin", "entity_msma_show_hp",
           "entity_snapshot_splitdelta_compress", "roomlobby_pilot_add",
           "msma_spawn_list_get_r_begin"]
READERS = ("sub_B02DD0", "sub_B02DF0", "sub_B06230", "sub_B02BA0", "sub_B02B40",
           "sub_B02E20", "sub_B02D30", "sub_B077B0", "sub_B07880", "sub_B08160",
           "sub_B05EA0", "sub_B418C0", "sub_B05ED0", "sub_B05EE0",
           "sub_B41470", "sub_B413B0", "sub_B05E30", "sub_B05D90", "sub_B05DA0",
           "sub_B41120", "sub_B41110", "sub_ABB2F0", "sub_CA0CE0", "sub_41D990",
           "sub_B03020", "sub_ADC810", "sub_B02FF0", "sub_B03580", "sub_B032A0",
           "sub_B03420", "sub_B08500", "sub_B0C1F0", "sub_B061C0", "sub_B036E0",
           "sub_B02D30")

def insn(ea):
    return idc.generate_disasm_line(ea, 0) or ""

def mnem(ea):
    return idc.print_insn_mnem(ea)

def opnd(ea, n):
    return idc.get_operand_value(ea, n)

out = []
for nm in TARGETS:
    r = None
    for x in H["recv"]:
        if x["name"] == nm:
            r = x
            break
    if not r:
        out.append("##### %s NOT FOUND" % nm)
        continue
    ent = int(r["entry"], 16)
    site = int(r["site"], 16)
    out.append("=" * 96)
    out.append("##### %s id=%s alloc=%s verdict=%s handler=%s args=%s" %
               (nm, r["id_hex"], r.get("alloc"), r.get("verdict"), r.get("handler"), r.get("args")))
    out.append("字段（dump 序）: " + " ".join("%s" % f["name"] for f in r["fields"]))
    out.append("-" * 96)
    cur = ent
    n = 0
    while cur != idc.BADADDR and cur < site + 0xA00 and n < 4000:
        n += 1
        d = insn(cur).strip()
        m = mnem(cur)
        show = None
        if m == "push" and idc.get_operand_type(cur, 0) == idc.o_imm:
            show = "  push %s" % idc.print_operand(cur, 0)
        elif m == "push" and "offset" in d:
            t = idc.get_strlit_contents(opnd(cur, 0), -1, 0)
            if t:
                t = t.decode("utf-8", "ignore") if isinstance(t, bytes) else t
                show = "  NAME  %r" % t
        elif m == "call":
            cal = d.split()[-1]
            if cal in READERS or cal.startswith("sub_B0") or cal.startswith("sub_AFB"):
                show = "  CALL  %s" % cal
        elif m == "cmp" and idc.get_operand_type(cur, 1) == idc.o_imm:
            show = "  cmp   %s" % d
        elif m in ("ja", "jae", "jb", "jbe", "jz", "jnz", "jl", "jle", "jg", "jge"):
            show = "  jcc   %s" % d
        if show:
            out.append("%08X %s" % (cur, show))
        cur = idc.next_head(cur)
    out.append("")

txt = "\n".join(out)
open(os.path.join(FMT, "_battle_detail_trace.txt"), "w", encoding="utf-8").write(txt)
print("written _battle_detail_trace.txt lines=%d" % len(out))

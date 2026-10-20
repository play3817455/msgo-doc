# -*- coding: utf-8 -*-
"""
对指定 recv 报文，导出其 case 的"解析调用轨迹"（entry → dump 头），用于定体长/字段宽度。
输出 reverse-login-chain/formats/_battle_case_trace.txt
"""
import idc
import idautils
import json
import os

FMT = r"f:\9ymsgo\9you\reverse-login-chain\formats"
RAW = os.path.join(FMT, "battle_protocol_raw.json")
OUT = os.path.join(FMT, "_battle_case_trace.txt")

TARGETS = [
    "proto_version_check_r",
    "authenticate_r",
    "cpf_authenticate",
    "roomlobby_game_start_r",
    "game_begin",
    "entity_snapshot",
    "entity_snapshot_splitdelta_compress",
    "weapon_hit_from",
    "weapon_hit_to_r",
    "entity_msma_show_hp",
    "entity_msma_dead",
    "score_update",
    "kill_count_update",
    "game_round_end",
    "roomlobby_pilot_add",
    "msma_spawn_list_get_r_begin",
    "pos_warp_force",
]

READERS = ("sub_B02D80", "sub_B02DA0", "sub_B02BA0", "sub_B02B40", "sub_B061C0", "sub_B02DD0",
           "sub_B02DF0", "sub_B02E20", "sub_B0C1F0", "sub_B41A10", "sub_B06200", "sub_B41470",
           "sub_B41120", "sub_B05DA0", "sub_B41110", "sub_B02D30", "sub_B02FF0", "sub_B02C90")

with open(RAW, encoding="utf-8") as f:
    data = json.load(f)

by_name = {}
for r in data["recv"]:
    by_name.setdefault(r["name"], r)

lines = []
for nm in TARGETS:
    r = by_name.get(nm)
    if not r:
        lines.append("##### %s : NOT FOUND" % nm)
        continue
    ent = int(r["entry"], 16)
    site = int(r["site"], 16)
    lines.append("=" * 100)
    lines.append("##### %s  id=%s gate=%s entry=%s site=%s" %
                 (nm, r["id_hex"], r["gate_index"], r["entry"], r["site"]))
    lines.append("      fields(order): " +
                 " | ".join("%s:%s" % (f["name"], f["hint"]) for f in r["fields"]))
    lines.append("-" * 100)
    cur = ent
    n = 0
    while cur != idc.BADADDR and cur < site + 0x40 and n < 900:
        n += 1
        d = idc.generate_disasm_line(cur, 0) or ""
        m = idc.print_insn_mnem(cur)
        txt = d.strip()
        interesting = False
        if m == "call":
            interesting = True
        elif m in ("push",) and idc.get_operand_type(cur, 0) == idc.o_imm:
            interesting = True
        elif m in ("cmp", "sub") and idc.get_operand_type(cur, 1) == idc.o_imm:
            interesting = True
        elif m in ("ja", "jae", "jb", "jbe", "jl", "jle", "jg", "jge", "jz", "jnz"):
            interesting = True
        elif "offset" in txt and '"' in txt:
            interesting = True
        if interesting:
            lines.append("   %08X  %s" % (cur, txt))
        cur = idc.next_head(cur)
    lines.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("written %s  lines=%d  sections=%d" % (OUT, len(lines), len(TARGETS)))
for nm in TARGETS:
    r = by_name.get(nm)
    print("  %-38s id=%-7s gate=%-4s nf=%d" %
          (nm, r["id_hex"] if r else "-", r["gate_index"] if r else "-",
           len(r["fields"]) if r else -1))

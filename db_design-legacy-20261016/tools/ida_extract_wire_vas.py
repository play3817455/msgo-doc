"""Run inside IDA via MCP py_exec_file. Emits wire-offset -> evidence_va JSON."""
import json
import sys
import ida_funcs
import idc

BATCH = sys.argv[1] if len(sys.argv) > 1 else "2"
OUT = rf"F:\9ymsgo\9you\db_design\schema\_meta\ida_wire_vas_batch{BATCH}.json"


def parse_imm(text: str) -> int:
    t = text.split(";")[0].strip()
    if t.endswith("h") or t.endswith("H"):
        return int(t[:-1], 16)
    return int(t, 0)


HELPER = {
    "sub_B02DF0": 2,
    "sub_B02DD0": 4,
    "sub_B02D80": 4,
    "sub_B02DA0": 2,
    "sub_B06290": 18,
    "sub_B06230": 1,
    "sub_B061C0": 1,
    "sub_B068B0": 24,
    "sub_B06200": 8,
    "sub_B42330": 72,
    "sub_B423F0": 256,
    "sub_B434B0": 16,
    "sub_B46FC0": 11,
    "sub_B08920": 18,
}


def parse_function(func_name: str) -> dict:
    ea = idc.get_name_ea_simple(func_name)
    func = ida_funcs.get_func(ea)
    if not func:
        return {"error": "no func"}

    insns = []
    cur = func.start_ea
    while cur < func.end_ea:
        insns.append(
            {
                "ea": cur,
                "mnem": idc.print_insn_mnem(cur),
                "op0": idc.print_operand(cur, 0),
                "op1": idc.print_operand(cur, 1),
            }
        )
        cur = idc.next_head(cur, func.end_ea)

    segs = []
    wire = 0
    i = 0
    while i < len(insns):
        ins = insns[i]
        mnem = ins["mnem"]

        if mnem == "add" and "ptr" in ins["op0"]:
            try:
                imm = parse_imm(ins["op1"])
            except ValueError:
                i += 1
                continue
            if imm <= 0:
                i += 1
                continue
            expanded = False
            if imm == 1 and i + 3 < len(insns):
                i2, i3 = insns[i + 2], insns[i + 3]
                if i2["mnem"] == "cmp" and i3["mnem"] in ("jb", "jbe", "jl", "jle"):
                    try:
                        bound = parse_imm(i2["op1"])
                        if bound > 1:
                            segs.append({"offset": wire, "size": bound, "va": hex(ins["ea"]), "kind": "loop1"})
                            wire += bound
                            i += 4
                            expanded = True
                    except ValueError:
                        pass
            if not expanded and imm == 8 and i + 4 < len(insns):
                i3, i4 = insns[i + 3], insns[i + 4]
                if i3["mnem"] == "cmp" and i4["mnem"] in ("jb", "jbe"):
                    try:
                        bound = parse_imm(i3["op1"])
                        if bound > 1:
                            segs.append({"offset": wire, "size": bound * 8, "va": hex(ins["ea"]), "kind": "loop8"})
                            wire += bound * 8
                            i += 5
                            expanded = True
                    except ValueError:
                        pass
            if not expanded and imm == 2 and i + 4 < len(insns):
                i3, i4 = insns[i + 3], insns[i + 4]
                if i3["mnem"] == "cmp" and i4["mnem"] in ("jb", "jbe"):
                    try:
                        bound = parse_imm(i3["op1"])
                        if bound > 1:
                            segs.append({"offset": wire, "size": bound * 2, "va": hex(ins["ea"]), "kind": "loop2"})
                            wire += bound * 2
                            i += 5
                            expanded = True
                    except ValueError:
                        pass
            if not expanded and imm == 4 and i + 3 < len(insns):
                for j in range(i + 1, min(i + 6, len(insns))):
                    if insns[j]["mnem"] == "cmp":
                        i4 = insns[j + 1] if j + 1 < len(insns) else None
                        if i4 and i4["mnem"] in ("jb", "jbe"):
                            try:
                                bound = parse_imm(insns[j]["op1"])
                                if bound > 1:
                                    segs.append({"offset": wire, "size": bound * 4, "va": hex(ins["ea"]), "kind": "loop4"})
                                    wire += bound * 4
                                    i = j + 2
                                    expanded = True
                                    break
                            except ValueError:
                                pass
            if not expanded:
                segs.append({"offset": wire, "size": imm, "va": hex(ins["ea"]), "kind": "add"})
                wire += imm
                i += 1
            continue

        if mnem == "call":
            tgt = (
                idc.get_name_ea_simple(ins["op0"])
                if ins["op0"].startswith("sub_")
                else idc.get_operand_value(ins["ea"], 0)
            )
            nm = idc.get_func_name(tgt)
            sz = HELPER.get(nm, 0)
            if sz:
                expanded = False
                call_ea = ins["ea"]
                for j in range(i + 1, min(i + 12, len(insns))):
                    if insns[j]["mnem"] != "cmp":
                        continue
                    ijb = insns[j + 1] if j + 1 < len(insns) else None
                    if not ijb or ijb["mnem"] not in ("jb", "jbe", "jl", "jle"):
                        continue
                    try:
                        bound = parse_imm(insns[j]["op1"])
                        jb_tgt = idc.get_operand_value(ijb["ea"], 0)
                    except (ValueError, TypeError):
                        continue
                    if bound <= 1:
                        continue
                    if jb_tgt <= call_ea:
                        total = bound * sz
                        segs.append({"offset": wire, "size": total, "va": hex(call_ea), "kind": "call_loop", "fn": nm, "count": bound})
                        wire += total
                        i = j + 2
                        expanded = True
                        break
                if not expanded:
                    segs.append({"offset": wire, "size": sz, "va": hex(ins["ea"]), "kind": "call", "fn": nm})
                    wire += sz
                    i += 1
            else:
                i += 1
            continue
        i += 1

    return {"function": func_name, "total": wire, "segments": segs}


BATCH_FN = {
    "1": {
        "item": "sub_B434F0",
        "ms_set": "sub_B41B10",
        "equip_set": "sub_B41C60",
        "pilot": "sub_B06360",
        "missionunit_set": "sub_B41BF0",
        "roominfo": "sub_B44880",
        "cinfo": "sub_B45940",
        "pilot_detail": "sub_B42640",
        "pilots_list": "sub_B42BB0",
        "pcard": "sub_B42BB0",
    },
    "2": {
        "lpcard": "sub_B43100",
        "ms": "sub_B06D80",
        "snapshot": "sub_B075A0",
        "funnelss": "sub_B081C0",
        "unlockw": "sub_B439D0",
        "adop_list": "sub_B43D90",
        "recruits": "sub_B45400",
        "leaders": "sub_B454D0",
        "bracket": "sub_B47060",
        "AI": "sub_B07230",
    },
    "3": {
        "item_list": "sub_B458A0",
        "party_member_stat": "sub_B432C0",
        "order": "sub_B46420",
        "rankself": "sub_B464A0",
        "ranking": "sub_B46560",
        "special_a_next": "sub_B46CD0",
        "sort_info": "sub_B461E0",
    },
    "4": {
        "ext_subrule": "sub_B456F0",
        "xwar_ext_rule": "sub_B08160",
        "wbonus": "sub_B453B0",
        "buffitem": "sub_B07E70",
        "config": "sub_B077B0",
        "progress": "sub_B07880",
        "bgm_desc": "sub_B07E00",
    },
    "5": {
        "phase_info": "sub_B46D20",
        "bracket_info": "sub_B46D80",
        "buildup_info": "sub_B44050",
        "challenge_info": "sub_B07540",
        "check_quest": "sub_B06C00",
        "wave_res": "sub_B08020",
        "appear_info": "sub_B07EC0",
        "avatar": "sub_B068B0",
    },
    "6": {
        "beginner_challenge_info": "sub_B42440",
        "clan_eff": "sub_B45F30",
        "dailycup_conf": "sub_B46E80",
        "dc_point": "sub_B47120",
        "examination_state": "sub_B42330",
    },
    "7": {
        "intro_info": "sub_B46140",
        "hack_check": "sub_B065D0",
        "lvjudge_hist": "sub_B44750",
        "unlocked_navi": "sub_B434B0",
        "pointdmg": "sub_B45760",
        "total_result_wave": "sub_B45580",
        "recruit": "sub_B45400",
    },
    "8": {
        "replay_info": "sub_B47340",
        "season_rb_conf": "sub_B471E0",
        "precord": "sub_B440B0",
    },
}

FN = BATCH_FN.get(BATCH, BATCH_FN.get("2", {}))
out = {ent: parse_function(fn) for ent, fn in FN.items()}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("Wrote", OUT, "batch", BATCH)
for ent, fn in FN.items():
    d = out[ent]
    print(f"{ent:16} fn={fn:14} total={d.get('total'):4} segs={len(d.get('segments', []))}")

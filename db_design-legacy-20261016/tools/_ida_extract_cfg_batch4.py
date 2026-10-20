#!/usr/bin/env python3
"""Extract cfg table column reads from IDA disassembly (run inside IDA via py_exec_file)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import ida_funcs
import idc

READERS = {
    "MISSION_VS": 0x59FEE0,
    "MISSION_COOP": 0x59DC00,
    "MISSION_GROUP": 0x59E8A0,
    "MISSION_SAFETY_AREA": 0x59EF40,
    "MISSION_EXTRULE": 0x59E170,
    "MISSION_XWAR_BANPICK": 0x5A0300,
    "COMMANDER_NPC": 0x572EE0,
    "COMMANDER_SUPPORT": 0x574300,
    "COMBAT_OPERATION": 0x572560,
    "AI_PARAM": 0x56EA00,
    "AI_WEAPON_PARAM": 0x56F080,
    "GACHA": 0x578220,
    "BYWORD": 0x570FC0,
    "QUEST": 0x58DCA0,
    "BUFF": 0x570750,
    "DAILY_RECORD": 0x575840,
    "CLAN_CHALLENGE": 0x571DA0,
    "TROOP_CHALLENGE": 0x592E50,
    "NETCAFE_CHALLENGE": 0x5875E0,
    "CHALLENGE_HIGHSCORE": 0x578630,
    "PLAY_BONUS_REWARD": 0x58C440,
    "BANNER_INFO": 0x56FF30,
    "BEGINNER_CHALLENGE": 0x570420,
    "MONTHLY_BONUS_REWARD": 0x57B0A0,
    "FORCEGAUGE_INFO": 0x577560,
    "ACTION_MODULE_INFO": 0x56DCD0,
    "PLAYER_NAVI": 0x58C7C0,
    "SEASON_CLASS_IMFORMATION": 0x5900A0,
    "SEASON_CLASS_UP_REWARD": 0x590ED0,
    "SEASON_RANKERBATTLE_REWARD": 0x5921A0,
    "TREND_DATA_WEAPON": 0x5928E0,
    "SCORE_CONFIG_CATEGORY": 0x58DDB0,
    "BGMPACKAGE": 0x570560,
}

CALL_KIND = {
    "sub_BBB370": "u32",
    "sub_BBB470": "float",
    "sub_BBB3F0": "i64",
    "sub_BBB4F0": "str_enum",
    "sub_456D90": "str",
    "sub_5976F0": "str_cond",
    "sub_BBB920": "str_opt",
    "sub_570950": "enum",
    "sub_56F4B0": "enum",
    "sub_56F3A0": "enum",
    "sub_575A60": "enum",
    "sub_5954A0": "enum",
    "sub_5951D0": "enum",
    "sub_5952C0": "enum",
    "sub_5953B0": "enum",
    "sub_593770": "enum",
    "sub_595870": "enum",
    "sub_5968A0": "enum",
    "sub_596990": "enum",
    "sub_596A80": "enum",
    "sub_596B70": "enum",
    "sub_596510": "enum",
    "sub_596C60": "enum",
    "sub_5965F0": "enum",
    "sub_5964A0": "enum",
    "sub_596D50": "enum",
    "sub_596E40": "enum",
    "sub_40CE20": "bool_enum",
    "sub_59E070": "enum",
    "sub_59E0F0": "enum",
    "sub_59FA70": "enum",
    "sub_59FB20": "enum",
    "sub_570660": "enum",
    "sub_570E80": "enum",
    "sub_5703A0": "enum",
    "sub_5812E0": "enum",
}


def call_name(ea: int) -> str:
    tgt = idc.get_operand_value(ea, 0)
    return idc.get_name(tgt) or ""


def extract_reader(func_ea: int) -> list[dict]:
    func = ida_funcs.get_func(func_ea)
    if not func:
        return []
    ea = func.start_ea
    end = func.end_ea
    pending_cols: list[int] = []
    reads: list[dict] = []
    reg_base = "esi"
    last_str_enum_col: int | None = None
    last_str_enum_va: int | None = None

    while ea < end:
        dis = idc.print_insn_mnem(ea)
        op0 = idc.print_operand(ea, 0)
        op1 = idc.print_operand(ea, 1)

        if dis == "mov" and op1 in ("esi", "edi", "ebp"):
            reg_base = op1

        if dis == "push":
            try:
                pending_cols.append(int(op0, 0))
            except ValueError:
                pass

        if dis == "call":
            cname = call_name(ea)
            kind = None
            for prefix, k in CALL_KIND.items():
                if prefix in cname:
                    kind = k
                    break
            col = pending_cols.pop() if pending_cols else None
            if kind == "str_enum" and col is not None:
                last_str_enum_col = col
                last_str_enum_va = ea + 1
            elif kind == "enum" and last_str_enum_col is not None:
                reads.append(
                    {
                        "csv_index": last_str_enum_col,
                        "type": "enum",
                        "asm_va": hex(last_str_enum_va or (ea + 1)),
                        "call": cname,
                        "wire_call": "sub_BBB4F0",
                    }
                )
                last_str_enum_col = None
                last_str_enum_va = None
            elif kind is not None and col is not None:
                reads.append(
                    {
                        "csv_index": col,
                        "type": kind,
                        "asm_va": hex(ea + 1),
                        "call": cname,
                    }
                )

        # bool: cmp eax, 0 / setg / mov byte
        if dis == "cmp" and reads and op1 == "0":
            if reads[-1].get("type") == "u32":
                reads[-1]["type"] = "bool"

        if dis == "mov" and reads:
            m = re.search(rf"\[{reg_base}\+(0x[0-9a-fA-F]+|\d+)\]", op0)
            if m and "memory_offset" not in reads[-1]:
                reads[-1]["memory_offset"] = int(m.group(1), 0)
            m2 = re.search(rf"\[({reg_base})\+(0x[0-9a-fA-F]+|\d+)\]", op1)
            if m2 and "memory_offset" not in reads[-1]:
                reads[-1]["memory_offset"] = int(m2.group(2), 0)

        ea = idc.next_head(ea, end)

    out: dict[int, dict] = {}
    for r in reads:
        col = r["csv_index"]
        if col not in out:
            out[col] = r
    return [out[k] for k in sorted(out)]


def main() -> None:
    result = {}
    for table, ea in READERS.items():
        cols = extract_reader(ea)
        result[table] = {
            "reader": hex(ea),
            "reader_func": idc.get_name(ea) or hex(ea),
            "column_count": len(cols),
            "columns": cols,
        }
    out = Path(r"F:\9ymsgo\9you\db_design\schema\_meta\ida_cfg_batch4_extract.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    for t, info in result.items():
        print(f"{t}: {len(info['columns'])} cols")


if __name__ == "__main__":
    main()

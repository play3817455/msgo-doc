#!/usr/bin/env python3
"""Extract cfg column reads from Hex-Rays decompile (IDA py_exec_file)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import ida_hexrays

READERS = {
    "WEAPON_SETTING": 0x597F50,
    "WEAPON_BATTLE_DETAIL": 0xA47BC0,
    "BULLET": 0x5709F0,
    "WRESTLE_PARAM": 0x56F5F0,
    "BUILDUP_WEAPON": 0x570880,
    "DAMAGE_FIELD_PARAM": 0x575D00,
    "ITEM": 0x593B70,
    "ITEM_PART": 0x5955A0,
    "ITEM_USE": 0x5959B0,
    "ITEM_TOKEN": 0x595960,
    "ITEMPACK_INFO": 0x5933C0,
}

COL_CALL = re.compile(
    r"sub_(BBB370|BBB470|BBB3F0|BBB4F0|456D90|5976F0|BBB920)\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)"
)
ENUM_AFTER_STR = re.compile(
    r"sub_BBB4F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)[^;]*;\s*[^;]*sub_(5968A0|596990|596A80|596B70|596510|596C60|5965F0|5964A0|596D50|596E40|570950|56F4B0|56F3A0|575A60|5954A0|5951D0|5952C0|5953B0|593770|595870|40CE20|402310)\("
)
VAR_COL = re.compile(r"\b(v\d+|a2)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*;[^;]*sub_BBB370\([^,]+,\s*\1")
MEM_STORE = re.compile(
    r"\*\(_(?:DWORD|BYTE|WORD|QWORD|float)\s*\*\)\((?:v7|a3|a4|esi|\*a3|\*a4|\w+)\s*\+\s*(0x[0-9a-fA-F]+|\d+)\)"
)
VA_TAIL = re.compile(r"/\*(0x[0-9a-fA-F]+)\*/\s*$")


def stmt_va(stmt: str) -> str | None:
    m = VA_TAIL.search(stmt.strip())
    return m.group(1) if m else None


def extract_from_decompile(func_ea: int) -> list[dict]:
    cfunc = ida_hexrays.decompile(func_ea)
    if not cfunc:
        return []
    text = str(cfunc)
    stmts = [s.strip() for s in text.split(";") if s.strip()]
    reads: list[dict] = []

    for i, stmt in enumerate(stmts):
        va = stmt_va(stmt)
        mem = None
        mm = MEM_STORE.search(stmt)
        if mm:
            mem = int(mm.group(1), 0)

        col = None
        kind = None
        m = COL_CALL.search(stmt)
        if m:
            fn, col_s = m.group(1), m.group(2)
            col = int(col_s, 0)
            kind = {
                "BBB370": "u32",
                "BBB470": "float",
                "BBB3F0": "i64",
                "BBB4F0": "str_enum",
                "456D90": "str",
                "5976F0": "str_cond",
                "BBB920": "str_opt",
            }[fn]
        else:
            em = ENUM_AFTER_STR.search(stmt + ";")
            if em:
                col = int(em.group(1), 0)
                kind = "enum"

        if col is None:
            vm = VAR_COL.search(stmt + ";" + (stmts[i + 1] if i + 1 < len(stmts) else ""))
            if vm:
                col = int(vm.group(2), 0)
                kind = kind or "u32"

        if col is None:
            continue

        if mem is None:
            for j in range(i, min(i + 4, len(stmts))):
                mm2 = MEM_STORE.search(stmts[j])
                if mm2:
                    mem = int(mm2.group(1), 0)
                    break

        reads.append(
            {
                "csv_index": col,
                "type": kind or "u32",
                "asm_va": va,
                "memory_offset": mem,
                "ord": i,
            }
        )

    out: dict[int, dict] = {}
    for r in reads:
        col = r["csv_index"]
        if col not in out:
            out[col] = {k: v for k, v in r.items() if k != "ord"}
        else:
            cur = out[col]
            if r.get("asm_va") and not cur.get("asm_va"):
                cur["asm_va"] = r["asm_va"]
            if r.get("memory_offset") is not None and (
                cur.get("memory_offset") is None or cur["memory_offset"] > 0x1000
            ):
                if r["memory_offset"] < 0x1000:
                    cur["memory_offset"] = r["memory_offset"]
    return [out[k] for k in sorted(out)]


def main() -> None:
    result = {t: {"reader": hex(ea), "columns": extract_from_decompile(ea)} for t, ea in READERS.items()}
    out = Path(r"F:\9ymsgo\9you\db_design\schema\_meta\ida_cfg_batch2_extract.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    for t, info in result.items():
        print(t, len(info["columns"]))


if __name__ == "__main__":
    main()

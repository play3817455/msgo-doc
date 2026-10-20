#!/usr/bin/env python3
import json
import re
from pathlib import Path

META = Path(__file__).resolve().parents[1] / "schema" / "_meta"


def parse_decomp_with_va(code: str) -> dict[int, dict]:
    out: dict[int, dict] = {}
    patterns = [
        (r"sub_BBB370\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "u32"),
        (r"sub_BBB470\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "float"),
        (r"sub_BBB3F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "i64"),
        (r"sub_BBB4F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "enum"),
        (r"sub_5976F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "str"),
        (r"sub_BBB920\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/", "str"),
    ]
    for pat, kind in patterns:
        for m in re.finditer(pat, code):
            col = int(m.group(1), 0)
            out.setdefault(col, {"csv_index": col, "type": kind, "asm_va": m.group(2)})

    for m in re.finditer(
        r"sub_BBB4F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/\s*[^;]*sub_(5968A0|596990|596A80|596B70|596510|596C60|5965F0|5964A0|596D50|596E40)\(",
        code,
    ):
        col = int(m.group(1), 0)
        out.setdefault(col, {"csv_index": col, "type": "enum", "asm_va": m.group(2)})

    for m in re.finditer(
        r"\*\(_(?:DWORD|BYTE|WORD|float)\s*\*\)\(v7 \+ (0x[0-9a-fA-F]+|\d+)\)\s*=[^;]*;\s*/\*(0x[0-9a-fA-F]+)\*/",
        code,
    ):
        off = int(m.group(1), 0)
        if off >= 0x800:
            continue
        va = m.group(2)
        # attach offset to col with same va if exists
        for col, info in out.items():
            if info.get("asm_va") == va:
                info["memory_offset"] = off
                break
    return out


def main() -> None:
    ws_path = Path(
        r"C:\Users\xxm38\.cursor\projects\f-9ymsgo-9you\agent-tools\8061adb7-9b69-40b1-a300-88f57a558959.txt"
    )
    ws_code = json.loads(ws_path.read_text(encoding="utf-8"))["code"]
    ws = parse_decomp_with_va(ws_code)
    disasm = json.loads((META / "ida_cfg_batch2_disasm.json").read_text(encoding="utf-8"))
    merged = {"WEAPON_SETTING": ws}
    for t, cols in disasm.items():
        if t != "WEAPON_SETTING":
            merged[t] = {c["csv_index"]: c for c in cols}
    (META / "ida_cfg_batch2_asm_merged.json").write_text(
        json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"WEAPON_SETTING {len(ws)} cols")


if __name__ == "__main__":
    main()

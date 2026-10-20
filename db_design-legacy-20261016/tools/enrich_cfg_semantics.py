#!/usr/bin/env python3
"""Bootstrap enum_values + MD-derived meanings into schema/cfg/tables/*.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_CONV = ROOT / "reverse-login-chain" / "formats" / "_enum_conv.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"
DATATABLES = ROOT / "datatables" / "01-列注释"

GENERIC = re.compile(
    r"^(整型参数|数值|u32\s*参数|float\s*参数|浮点参数|枚举/类别|ASM已映射)(（待定）|\(待定\)|（启发）)?",
    re.I,
)
STAR_LINE = re.compile(r"★+([^★（\n]+?)(?:（|`sub_([^`]+)`)?")


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def build_conv_map(conv: dict) -> dict[tuple[str, int], str]:
    out: dict[tuple[str, int], str] = {}
    for fn, uses in conv.items():
        for u in uses:
            try:
                col = int(str(u["col"]).rstrip("u"))
            except ValueError:
                continue
            out[(u["file"], col)] = fn
    return out


def enum_values_from_fn(enums: dict, fn: str) -> list[dict] | None:
    r = enums.get(fn)
    if not r:
        return None
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": name, "value": val} for name, val in r["table"]]
    lits = r.get("lits") or []
    consts = r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    if lits:
        return [{"name": n, "value": i} for i, n in enumerate(lits)]
    return None


def parse_md_columns(md_path: Path) -> dict[int, dict]:
    """Parse csv_index -> {meaning, enum_converter hint} from MD table."""
    if not md_path.is_file():
        return {}
    text = md_path.read_text(encoding="utf-8")
    out: dict[int, dict] = {}
    for line in text.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        m_col = re.search(r"`(\d+)`", parts[2])
        if not m_col:
            continue
        csv_idx = int(m_col.group(1))
        cell = parts[4]
        info: dict = {}
        if "★" in cell or "确证" in cell or len(cell) > 20:
            info["meaning"] = re.sub(r"\*+", "", cell).strip()
        m_fn = re.search(r"`(sub_[0-9A-Fa-f]+)`", cell)
        if m_fn:
            info["enum_converter"] = m_fn.group(1)
        m_title = re.search(r"★+\*\*([^*]+)\*\*", cell)
        if m_title:
            slug = re.sub(r"[^\w]+", "_", m_title.group(1).strip()).strip("_").lower()
            if slug and slug not in ("enum", "u32"):
                info["suggested_name"] = slug[:48]
        out[csv_idx] = info
    return out


def is_generic_meaning(m: str) -> bool:
    m = re.sub(r"\*+", "", m or "").strip()
    m = re.sub(r"（待定）|\(待定\)", "", m).strip()
    return not m or bool(GENERIC.match(m)) or "系数/倍率" in m or m.startswith("ASM已映射")


def enrich_table(data: dict, conv_map: dict, enums: dict, md_info: dict) -> int:
    changed = 0
    csv_path = data.get("csv_path", "")
    for c in data.get("columns", []):
        idx = c.get("csv_index")
        if idx is None:
            continue
        mi = md_info.get(idx, {})

        fn = c.get("enum_converter") or mi.get("enum_converter")
        if not fn:
            fn = conv_map.get((csv_path, idx))
        if fn and fn != "?":
            if c.get("enum_converter") != fn:
                c["enum_converter"] = fn
                changed += 1
            vals = enum_values_from_fn(enums, fn)
            if vals and not c.get("enum_values"):
                c["enum_values"] = vals
                c["enum_doc"] = ENUM_DOC
                changed += 1

        md_mean = mi.get("meaning")
        if md_mean and is_generic_meaning(c.get("meaning", "")):
            clean = re.sub(r"<br>.*", "", md_mean, flags=re.I).strip()
            if len(clean) > 8:
                c["meaning"] = clean[:500]
                changed += 1

        sug = mi.get("suggested_name")
        cur = c.get("name", "")
        if sug and (cur.startswith("field_") or cur.startswith("unknown_") or cur == "name" or cur.startswith("col")):
            c["name"] = sug
            c["db_column"] = sug
            changed += 1

        if c.get("display_name") and is_generic_meaning(c.get("display_name", "")):
            if c.get("meaning") and not is_generic_meaning(c["meaning"]):
                c["display_name"] = c["meaning"][:80].split("（")[0].split("(")[0].strip()
                changed += 1

    return changed


def main() -> None:
    enums = load_json(ENUMS_JSON)
    conv = load_json(ENUM_CONV)
    conv_map = build_conv_map(conv)
    total = 0
    for path in sorted(TABLES_DIR.glob("*.json")):
        data = load_json(path)
        md_path = ROOT / data.get("source_md", "")
        if not md_path.is_file() and data.get("source_md"):
            md_path = DATATABLES / Path(data["source_md"]).name
        n = enrich_table(data, conv_map, enums, parse_md_columns(md_path))
        if n:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            total += n
            print(f"  {data['id']}: {n} fields")
    print(f"enriched {total} field updates")


if __name__ == "__main__":
    main()

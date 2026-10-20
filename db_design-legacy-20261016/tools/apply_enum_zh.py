#!/usr/bin/env python3
"""Apply enum_translate to enums_ida.json + enum_glossary_zh.json (+ enums.json names)."""

from __future__ import annotations

import json
from pathlib import Path

from enum_translate import MANUAL_ZH, exact_zh, is_rough, translate

ROOT = Path(__file__).resolve().parents[2]
ENUMS_IDA = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enums_ida.json"
GLOSSARY = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enum_glossary_zh.json"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
TABLES_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"


def all_names_from_schema() -> set[str]:
    names: set[str] = set()
    for p in TABLES_DIR.glob("*.json"):
        tbl = json.loads(p.read_text(encoding="utf-8"))
        for c in tbl.get("columns", []):
            for ev in c.get("enum_values") or []:
                if ev.get("name"):
                    names.add(str(ev["name"]))
    return names


def all_names_from_enums_json(ej: dict) -> set[str]:
    names: set[str] = set()
    for entry in ej.values():
        for row in entry.get("table") or []:
            if row and row[0]:
                names.add(str(row[0]))
        for lit in entry.get("lits") or []:
            if lit:
                names.add(str(lit))
    return names


def best_zh(name: str, gv: dict) -> str:
    hit = exact_zh(name)
    if hit:
        return hit
    cur = gv.get(name, "")
    if cur and not is_rough(cur, name):
        return cur
    return translate(name)


def main() -> None:
    ida = json.loads(ENUMS_IDA.read_text(encoding="utf-8"))
    gloss = json.loads(GLOSSARY.read_text(encoding="utf-8")) if GLOSSARY.is_file() else {}
    gv = gloss.setdefault("global_values", {})
    cv = gloss.setdefault("converters", {})

    all_names: set[str] = set()
    if ENUMS_JSON.is_file():
        ej = json.loads(ENUMS_JSON.read_text(encoding="utf-8"))
        all_names |= all_names_from_enums_json(ej)
    all_names |= all_names_from_schema()
    all_names |= set(MANUAL_ZH.keys())
    for nm in sorted(all_names):
        gv[nm] = best_zh(nm, gv)

    updated = 0
    for conv, meta in ida.get("converters", {}).items():
        cvals = cv.setdefault(conv, {}).setdefault("values", {})
        for v in meta.get("values") or []:
            nm = v.get("name", "")
            if not nm:
                continue
            old = v.get("label_zh", "")
            zh = best_zh(nm, gv)
            if zh != old:
                v["label_zh"] = zh
                updated += 1
            gv[nm] = zh
            cvals[nm] = zh

    ENUMS_IDA.write_text(json.dumps(ida, ensure_ascii=False, indent=2), encoding="utf-8")
    GLOSSARY.write_text(json.dumps(gloss, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {updated} label_zh; glossary global_values={len(gv)}")


if __name__ == "__main__":
    main()

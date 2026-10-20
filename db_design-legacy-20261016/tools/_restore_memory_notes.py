#!/usr/bin/env python3
"""一次性修复：把 `asm_audit.memory` 里被 audit_memory_chain.py 整体替换抹掉的手写键找回。

背景：`audit_memory_chain.py` 原先用 `comp["asm_audit"]["memory"] = {...}` 覆盖，
2026-09-24 一次全量重跑抹掉了 113 个复合体手写的 `note` / `memory_claim` /
`manual_batch` / `wire_eq_mem_prefix`。工具已改为就地 `update()`（只拥有 6 个键）；
本脚本按 backup 目录把非工具键补回去（live 里有更新值的以 live 为准）。

    python tools/_restore_memory_notes.py [--apply]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
BACKUP = ROOT.parent / "_backup_before_modelregen_20260923-074704" / "schema" / "composites"

# audit_memory_chain.py 生成并拥有的键
TOOL_KEYS = {"verified", "status", "mem_fields", "fields_ok", "fields_fail", "issues"}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正写回（默认只报告）")
    args = ap.parse_args()

    restored = 0
    for old_path in sorted(BACKUP.glob("*.json")):
        new_path = COMP / old_path.name
        if not new_path.exists():
            continue
        old = load(old_path)
        old_mem = (old.get("asm_audit") or {}).get("memory")
        if not isinstance(old_mem, dict):
            continue
        keep = {k: v for k, v in old_mem.items() if k not in TOOL_KEYS}
        if not keep:
            continue
        new = load(new_path)
        mem = (new.get("asm_audit") or {}).get("memory")
        if mem is None:
            continue
        missing = [k for k in keep if k not in mem]
        if not missing:
            continue
        print(f"{old_path.stem:<28} 补回 {missing}")
        if args.apply:
            for k in missing:
                mem[k] = keep[k]
            save(new_path, new)
        restored += 1

    print(f"\n{'已写回' if args.apply else '待补'} {restored} 个复合体")
    if not args.apply:
        print("加 --apply 生效")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

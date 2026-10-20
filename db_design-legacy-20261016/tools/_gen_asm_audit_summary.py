#!/usr/bin/env python3
"""Generate ASM audit summary markdown from table/composite JSON."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
QUEUE = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
OUT = ROOT / "schema" / "_meta" / "asm_audit_summary.md"


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def composite_for_table(tbl: dict) -> tuple[str, dict | None]:
    ent = tbl.get("entity_ref") or tbl.get("asm_audit", {}).get("composite_ref")
    if not ent:
        for col in tbl.get("columns", []):
            if col.get("composite_ref"):
                ent = col["composite_ref"]
                break
    if not ent:
        ent = tbl["id"].removeprefix("tbl_")
    path = COMP / f"{ent}.json"
    if path.exists():
        return ent, load(path)
    return ent, None


def main() -> None:
    queue = load(QUEUE)
    rows: list[tuple[str, str, str, int, int, str, str]] = []
    pass_n = fail_n = 0
    mem_n = mem_pass = mem_fail = mem_skip = 0

    for p in sorted(TABLES.glob("tbl_*.json")):
        tbl = load(p)
        if tbl.get("status") != "complete":
            continue
        tid = tbl["id"]
        ent, comp = composite_for_table(tbl)
        audit = (comp or {}).get("asm_audit") or tbl.get("asm_audit", {})
        status = audit.get("status", "?")
        if status == "pass":
            pass_n += 1
        elif status == "fail":
            fail_n += 1
        members = (comp or {}).get("members", [])
        if comp and comp.get("layout_same_as"):
            src = load(COMP / f"{comp['layout_same_as']}.json")
            members = src.get("members", [])
        mem_fields = sum(
            1
            for m in members
            if m.get("memory_offset") is not None or m.get("memory_only")
        )
        mem_n += mem_fields
        mem_audit = audit.get("memory") or {}
        if mem_audit.get("status") == "pass":
            mem_pass += 1
        elif mem_audit.get("status") == "fail":
            mem_fail += 1
        elif comp and comp.get("memory_claim") == comp.get("length") and mem_fields == 0:
            mem_skip += 1
        reader = audit.get("reader") or (comp or {}).get("reader", "—")
        length = audit.get("total_bytes") or (comp or {}).get("length", "—")
        rows.append((tid, ent, status, len(members), mem_fields, str(reader), str(length)))

    lines = [
        "# ASM 审计总览",
        "",
        f"> 生成：{date.today()} · 工具：`_gen_asm_audit_summary.py`",
        "",
        "## 结论",
        "",
        f"| 指标 | 值 |",
        f"|---|---|",
        f"| 表（complete） | {len(rows)} |",
        f"| wire 链 pass | **{pass_n}/{len(rows)}** |",
        f"| wire 链 fail | {fail_n} |",
        f"| memory_offset / memory_only 字段 | {mem_n} |",
        f"| memory 链 pass | **{mem_pass}/{mem_pass + mem_fail}**（{mem_skip} 无槽差跳过） |",
        f"| 审计批次 | #1–#8 complete |",
        "",
        "## 逐表",
        "",
        "| 表 | composite | ASM | 成员 | mem≠wire | reader | 线长 |",
        "|---|---|---|---:|---:|---|---:|",
    ]
    for tid, ent, status, nmem, memf, reader, length in rows:
        mark = "✓" if status == "pass" else "✗"
        lines.append(
            f"| `{tid}` | `{ent}` | {mark} {status} | {nmem} | {memf} | `{reader}` | {length} |"
        )

    lines.extend(
        [
            "",
            "## 批次队列",
            "",
        ]
    )
    for b in queue.get("batches", []):
        s = b.get("summary", {})
        lines.append(
            f"- **Batch #{b['id']}** · {b.get('audited', '?')} · "
            f"pass {s.get('pass', '?')}/{len(b.get('tables', []))}"
        )

    lines.extend(
        [
            "",
            "## 相关文档",
            "",
            "- `asm_chain_remediation.md` — wire vs memory 修法",
            "- `asm_audit_batch01.md` … `asm_audit_batch08.md` — 分批取证记录",
            "",
        ]
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({pass_n}/{len(rows)} pass)")


if __name__ == "__main__":
    main()

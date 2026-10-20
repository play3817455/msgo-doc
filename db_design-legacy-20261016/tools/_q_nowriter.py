#!/usr/bin/env python3
"""临时探查：no_writer 批次工作清单（用完即删）。"""
from __future__ import annotations

import json
from pathlib import Path

DB = Path(__file__).resolve().parent.parent
OBJ = DB / "schema" / "homing" / "objects"

ov = json.loads((DB / "schema" / "homing" / "_overrides.json").read_text(encoding="utf-8"))
nw = [k for k in (ov.get("no_writer") or {}) if k != "_note"]

objects = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in OBJ.glob("*.json")}

sig: dict[tuple, list[str]] = {}
for oid in nw:
    obj = objects[oid]
    names = tuple(m["name"] for m in obj.get("members", []))
    sig.setdefault(names, []).append(oid)


def writer_of(oid: str) -> int:
    return len(objects[oid].get("writes") or [])


print(f"{'对象':<22}{'PK 类别':<12}{'成员':>4}  {'旧表':<18}{'读方':<44}成员序（前 10）")
print("-" * 170)
for oid in nw:
    o = objects[oid]
    ms = o.get("members", [])
    names = ",".join(m["name"] for m in ms[:10])
    reads = ",".join(r.get("command", "").split("-")[1] if "-" in r.get("command", "") else r.get("command", "")
                     for r in (o.get("reads") or []))
    print(f"{oid:<22}{o.get('pk_kind',''):<12}{len(ms):>4}  {str(o.get('legacy_table') or '-'):<18}{reads:<44}{names}")

print("\n同形成员序分组（>1 才算）:")
for names, ids in sig.items():
    if len(ids) > 1:
        print("  ", ids, f"({len(names)} 成员)")

print("\n身份候选（成员名里带 id/uniq/ent/npc/no 且 role 不是 scope）:")
for oid in nw:
    o = objects[oid]
    cand = [m["name"] for m in o.get("members", [])
            if m.get("role") not in ("scope",) and any(t in m["name"] for t in ("_id", "uniq", "ent_", "npc", "_no"))]
    if cand:
        print(f"  {oid:<22}{cand}")

print("\n旧表实况（legacy_evidence live 段）:")
ev = json.loads((DB / "schema" / "_meta" / "legacy_evidence.json").read_text(encoding="utf-8"))
tabs = ev.get("tables") or {}
for oid in nw:
    o = objects[oid]
    lt = o.get("legacy_table")
    if not lt:
        print(f"  {oid:<22}无旧表（纯新增）")
        continue
    e = tabs.get(str(lt).replace("tbl_", "")) or tabs.get(str(lt)) or {}
    live = e.get("live") or {}
    cols = live.get("columns") or []
    uq = live.get("unique") or []
    print(f"  {oid:<22}{lt:<18}列 {len(cols):<3} UNIQUE {uq}")

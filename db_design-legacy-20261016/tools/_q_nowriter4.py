#!/usr/bin/env python3
"""临时探查 4：为 35 个 no_writer 对象找双胞胎 / 宿主 / 子集（用完即删）。"""
from __future__ import annotations

import json
import re
from pathlib import Path

DB = Path(__file__).resolve().parent.parent
OBJ = DB / "schema" / "homing" / "objects"
CMD = DB / "schema" / "commands"
objects = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in OBJ.glob("*.json")}
ov = json.loads((DB / "schema" / "homing" / "_overrides.json").read_text(encoding="utf-8"))
nw = [k for k in (ov.get("no_writer") or {}) if k != "_note"]


def names(oid: str) -> list[str]:
    return [m["name"] for m in objects[oid].get("members", [])]


# 1) 每个复合体（对象成员序）→ 谁在用它当成员/数组元素
sig = {oid: tuple(names(oid)) for oid in objects}
users: dict[tuple, list[tuple[str, str]]] = {}
for oid, o in objects.items():
    for m in o.get("members", []):
        t = str(m.get("wire_type") or "")
        mm = re.match(r"(?:array<)?(?:struct<)?([A-Za-z0-9_]+)", t)
        if not mm:
            continue
        ref = mm.group(1)
        if ref in objects and ref != oid:
            users.setdefault(tuple(names(ref)), []).append((oid, m["name"]))

for oid in nw:
    o = objects[oid]
    a = tuple(names(oid))
    same = [x for x in objects if x != oid and tuple(names(x)) == a and x not in nw]
    same_nw = [x for x in nw if x != oid and tuple(names(x)) == a]
    host = users.get(a) or []
    sub_of = []
    for x in objects:
        if x == oid or x in nw:
            continue
        b = names(x)
        if len(a) > 2 and set(a) < set(b):
            sub_of.append((x, len(b)))
        elif len(a) > 2 and a[:5] == tuple(b[:5]) and len(a) != len(b):
            sub_of.append((x + "(同前缀)", len(b)))
    print(f"{oid:<22} disp={o.get('disposition')} pk={o.get('pk_kind'):<11} 成员={len(a):<4} "
          f"孪生根={same} 孪生NW={same_nw} 被当作成员={host[:3]} 子集于={sub_of[:3]}")

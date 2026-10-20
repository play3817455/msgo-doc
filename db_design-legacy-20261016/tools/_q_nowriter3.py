#!/usr/bin/env python3
"""临时探查 3：孪生根对象的写读方 / 行键 / 旧表（用完即删）。"""
from __future__ import annotations

import json
from pathlib import Path

DB = Path(__file__).resolve().parent.parent
OBJ = DB / "schema" / "homing" / "objects"
objects = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in OBJ.glob("*.json")}

twins = ["clan_member_card", "item_list", "roominfo", "dc_point", "xwar_ext_rule", "funnelss",
         "wave_res", "pilot", "precord", "unlockw"]
for oid in twins:
    o = objects.get(oid)
    if not o:
        print(f"{oid}: 不存在")
        continue
    w = o.get("writes") or []
    r = [(x.get("command"), x.get("via"), x.get("op")) for x in (o.get("reads") or [])]
    print(f"-- {oid} pk={o.get('pk_kind')} pk_members={(o.get('keys') or {}).get('primary_key')} "
          f"legacy={o.get('legacy_table')} 成员={len(o.get('members') or [])}")
    print(f"   写: {[x.get('command') for x in w]}")
    print(f"   读: {r}")

print("\n6 张他人卡的读取命令（命令 → 顶层数组）:")
import re
CMD = DB / "schema" / "commands"
for cid in ("SC-0x7051", "SC-0x8E92", "SC-0x4F43", "SC-0x9F94", "SC-0xDB3F", "SC-0x7587", "SC-0xB985", "SC-0xE13A", "SC-0xB4B6", "SC-0xDBDB", "SC-0x6B15", "SC-0xB43F"):
    hits = list(CMD.glob(f"{cid}-*.json"))
    if not hits:
        print(f"  {cid}: 找不到命令文件")
        continue
    for h in hits:
        d = json.loads(h.read_text(encoding="utf-8"))
        arrays = []
        for f in d.get("fields") or []:
            t = str(f.get("wire_type") or "")
            if "array<" in t or (f.get("count") and f.get("count") != 1):
                arrays.append((f.get("name"), t, f.get("count")))
        print(f"  {h.stem}")
        print(f"     arrays: {arrays}")

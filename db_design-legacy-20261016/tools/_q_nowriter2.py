#!/usr/bin/env python3
"""临时探查 2：no_writer 形状与已建根对象的包含关系（用完即删）。"""
from __future__ import annotations

import json
from pathlib import Path

DB = Path(__file__).resolve().parent.parent
OBJ = DB / "schema" / "homing" / "objects"
objects = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in OBJ.glob("*.json")}


def names(oid: str) -> list[str]:
    return [m["name"] for m in objects[oid].get("members", [])]


groups = {
    "他人卡 20": ["lpcard", "member_info", "friend_detail", "friend_histories", "mshipbid_card", "block_detail"],
    "58 机师卡": ["pcard", "pilots_list"],
    "队伍条目 7": ["leaders", "member"],
    "排行 12": ["ranking", "toppilots"],
    "单件": ["pbadge", "lvjudge_hist", "comment", "activity", "invite", "bmgpack", "bonus_event",
             "coop_room", "dcpoint_detail", "extrarule_xwar_info", "favms_add"],
}
for g, ids in groups.items():
    print("=" * 30, g)
    for oid in ids:
        print(f"-- {oid} ({len(names(oid))})")
        print("   " + ",".join(names(oid)))

print("\n\n候选「宿主」根对象的成员（找包含关系）:")
for oid in ("pilot", "pilot_detail", "precord", "roominfo", "clan_member_card", "cinfo", "unlockw", "ms_rokaku"):
    if oid in objects:
        print(f"-- {oid} ({len(names(oid))})")
        print("   " + ",".join(names(oid)))

print("\n\n自动包含关系（no_writer 成员集 ⊆ 某根对象成员集 / 同序前缀）:")
ov = json.loads((DB / "schema" / "homing" / "_overrides.json").read_text(encoding="utf-8"))
nw = [k for k in (ov.get("no_writer") or {}) if k != "_note"]
roots = [oid for oid, o in objects.items() if o.get("shape") == "root" and oid not in nw]
for oid in nw:
    a = names(oid)
    sa = set(a)
    for r in roots:
        b = names(r)
        sb = set(b)
        if len(a) > 2 and sa and sa <= sb:
            print(f"  {oid} ({len(a)}) ⊆ {r} ({len(b)})")
            break
        if len(a) > 2 and a[:6] == b[:6]:
            print(f"  {oid} 与 {r} 同前缀（{len(a)} vs {len(b)}）")
            break

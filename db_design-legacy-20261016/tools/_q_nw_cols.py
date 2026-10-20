#!/usr/bin/env python3
"""no_writer 裁决的安全检查：判 `DERIVED` 前，成员名必须能在**别处**找到娘家。

输出：每个待裁对象 → 成员名 → 出现在哪些「本轮保留表的对象」上（同名才算；
名字变体不算，留给 colname 订正）。一个成员名若在所有保留对象上都找不到，
那它一退表就**没人接**——该对象就不能判 DERIVED（要么 `fold` 并列，要么留表）。
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OBJDIR = ROOT / "schema" / "homing" / "objects"

BATCH = [
    "activity", "block_detail", "bmgpack", "bonus_event", "comment", "coop_room",
    "dcpoint_detail", "extrarule_xwar_info", "favms_add", "friend_detail",
    "friend_histories", "funnel_snapshot_entry", "invite", "leaders", "lpcard",
    "lvjudge_hist", "mapgimmick_entry", "member", "member_info", "mshipbid_card",
    "parts_exec_entry", "pbadge", "pcard", "pilots_list", "rank_pilot",
    "rank_pilot_light", "ranking", "respawn_post", "respawn_post_entry",
    "result_detail", "result_wave", "score_ranking", "support_spot",
    "team_pilot", "toppilots",
]
TWINS = ["clan_member_card", "item_list", "roominfo", "dc_point", "xwar_ext_rule",
         "favms", "precord", "pilot", "pilot_detail", "wave_res", "funnelss"]


def main() -> int:
    objs: dict[str, dict] = {}
    for p in sorted(OBJDIR.glob("*.json")):
        o = json.loads(p.read_text(encoding="utf-8"))
        objs[o["id"]] = o

    def mems(oid: str) -> list[str]:
        return [m["name"] for m in objs[oid].get("members") or []]

    # 宿主 = 本轮**不进这批**的 PERSIST 根：它们的成员才是「退表后真的有人接」的列。
    # 同批对象互相包含不算数（两张表一起退，列就一起没了）。
    keep = [oid for oid, o in objs.items()
            if o.get("disposition") == "PERSIST" and o.get("is_root")
            and oid not in BATCH]
    host: dict[str, list[str]] = {}
    for oid in keep:
        for n in mems(oid):
            host.setdefault(n, []).append(oid)

    for oid in BATCH + TWINS:
        if oid not in objs:
            print(f"### {oid}  MISSING")
            continue
        o = objs[oid]
        ms = mems(oid)
        orphans = [n for n in ms if n not in host and n not in BATCH]
        print(f"### {oid}  ({len(ms)} 成员, {o.get('disposition')}, pk={o.get('pk_kind')})")
        if orphans:
            print("   无娘家:", ", ".join(orphans))
        else:
            print("   全部成员名都有娘家")
    return 0


if __name__ == "__main__":
    sys.exit(main())

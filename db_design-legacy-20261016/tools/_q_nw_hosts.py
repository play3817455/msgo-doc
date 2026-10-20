#!/usr/bin/env python3
"""给 no_writer 的裁决对象打印「每个成员名 → 娘家对象」明细（只列非本批 PERSIST 宿主）。"""

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
    "team_pilot", "toppilots", "clan_member_card", "item_list",
]


def main(argv: list[str]) -> int:
    objs: dict[str, dict] = {}
    for p in sorted(OBJDIR.glob("*.json")):
        o = json.loads(p.read_text(encoding="utf-8"))
        objs[o["id"]] = o
    host: dict[str, list[str]] = {}
    for oid, o in objs.items():
        if oid in BATCH or o.get("disposition") != "PERSIST" or not o.get("is_root"):
            continue
        for m in o.get("members") or []:
            host.setdefault(m["name"], []).append(oid)

    for oid in argv[1:]:
        o = objs[oid]
        print(f"### {oid}")
        for m in o.get("members") or []:
            n = m["name"]
            print(f"   {n:28s} -> {', '.join(host.get(n) or ['—'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

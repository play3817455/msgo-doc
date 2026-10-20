# -*- coding: utf-8 -*-
"""ガンダムエクシア / エクシアリペアⅡ 的所有 wiki 武器行原样，用于观察 効果時間 与 威力 的对应。只读。"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = os.path.join(os.path.dirname(HERE), "gow_wiki", "data", "units.json")

WANT = {"1132032", "1132242"}
units = json.load(open(UNITS, encoding="utf-8"))

KEYS = ["名称", "icon_id", "弾数", "重量", "ダウンポイント", "威力", "効果時間",
        "射程距離", "リロード時間", "ロックオン", "集弾性能", "連射速度"]

for u in units:
    if not isinstance(u, dict) or str(u.get("dev_id")) not in WANT:
        continue
    print("==== %s dev_id=%s" % (u.get("name"), u.get("dev_id")))
    for g in u.get("weapons") or []:
        for r in g.get("rows") or []:
            if not (r.get("名称") or "").strip() or r.get("名称") == "~":
                continue
            print("  -- %s (icon_id=%s)" % (r.get("名称"), r.get("icon_id")))
            for k in KEYS:
                if k in r:
                    print("       %-12s %s" % (k, r[k]))
    print()

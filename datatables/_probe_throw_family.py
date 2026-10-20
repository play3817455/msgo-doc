# -*- coding: utf-8 -*-
"""全 wiki 里「投擲 / ダガー」类武器行的 威力 vs 効果時間 统计。只读。"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = os.path.join(os.path.dirname(HERE), "gow_wiki", "data", "units.json")
units = json.load(open(UNITS, encoding="utf-8"))

rows = []
for u in units:
    if not isinstance(u, dict):
        continue
    for g in u.get("weapons") or []:
        for r in g.get("rows") or []:
            nm = (r.get("名称") or "").strip()
            if not nm or nm == "~":
                continue
            rows.append((nm, r, str(u.get("name")), str(u.get("dev_id"))))

print("全 wiki 武器行 %d" % len(rows))


def show(tag, pred, limit=25):
    hit = [x for x in rows if pred(x[0])]
    print("\n== %s 命中 %d 行" % (tag, len(hit)))
    for nm, r, page, did in hit[:limit]:
        print("   %-30s %-16s dev=%-9s icon=%-9s 威力=%-16s 効果時間=%-14s DP=%-6s 弾数=%s"
              % (nm[:30], page[:16], did, r.get("icon_id"), r.get("威力", "-"),
                 r.get("効果時間", "-"), r.get("ダウンポイント", "-"), r.get("弾数", "-")))
    if len(hit) > limit:
        print("   ... 余 %d" % (len(hit) - limit))


show("名称含 (投擲)", lambda n: "投擲" in n)
show("名称含 ダガー", lambda n: "ダガー" in n)

print("\n== 有 効果時間 字段的全部行 ==")
eff = [(nm, r, page, did) for nm, r, page, did in rows if r.get("効果時間")]
print("   共 %d 行" % len(eff))
for nm, r, page, did in eff[:40]:
    print("   %-30s %-16s icon=%-9s 効果時間=%-14s 威力=%-16s DP=%s"
          % (nm[:30], page[:16], r.get("icon_id"), r.get("効果時間"), r.get("威力", "-"),
             r.get("ダウンポイント", "-")))

cnt = collections.Counter(str(r.get("効果時間")) for _, r, _, _ in eff)
print("\n   効果時間 取值分布(前20): %s" % cnt.most_common(20))

# -*- coding: utf-8 -*-
"""按「武器 ID 位数」切开 #36/#37，看数值分布 —— 这是判孤儿族最锐利的一刀。

判据：合法 9 位族来自 wiki 面板经 `weapon_client_raw` 换算，POWER 原值应落在
      20–7500（面板 200–75000）、STABILITY 落在 [0,1] 的 (500-原值)/100 量级。
      旧轮转抓取的错列会把短号整族打成 1–2 位数 POWER、或把 RELOAD/STABILITY 写成负数。
"""
import collections
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
CLIENT = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings")


def rd(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


MELEE = {r[0].strip().lstrip("\ufeff") for r in rd(os.path.join(CLIENT, "weapon_wrestle.csv"))
         if r and r[0].strip().lstrip("\ufeff").isdigit()}
print("客户端近战短号（合法短号）:", sorted(MELEE))


def num(x):
    try:
        return float(x)
    except Exception:
        return None


rows = [r for r in rd(os.path.join(DF, "weapon_battle_detail.csv"))
        if not r[0].lstrip("\ufeff").startswith("#") and len(r) > 2]
byattr = collections.defaultdict(lambda: collections.defaultdict(list))
for attr, wid, val in ((r[0].strip(), r[1].strip(), r[2].strip()) for r in rows):
    grp = "9位" if len(wid) == 9 else ("近战8" if wid in MELEE else "短号孤儿")
    v = num(val)
    if v is not None:
        byattr[attr][grp].append((wid, v))

print()
for attr in ("POWER", "STABILITY", "RELOAD", "RAPIDDELAY", "COOLTIME", "LOCKON_CAM", "RANGE"):
    if attr not in byattr:
        continue
    line = "%-11s" % attr
    for grp in ("9位", "近战8", "短号孤儿"):
        xs = byattr[attr].get(grp, [])
        if not xs:
            line += "  %-8s --" % grp
            continue
        vs = sorted(v for _, v in xs)
        line += "  %-8s n=%-5d min=%-9.3f 中位=%-9.3f max=%-9.3f" % (
            grp, len(vs), vs[0], vs[len(vs) // 2], vs[-1])
    print(line)

print()
print("--- 短号孤儿的 POWER 原值分布（若整族落在 1–20，就是错列抓取）---")
allv = [(w, v) for grp in byattr["POWER"].values() for w, v in grp]
short = sorted(v for w, v in allv if len(w) < 9 and w not in MELEE)
print("短号孤儿 POWER 取值 top:", collections.Counter(short).most_common(20))
print("合法 9 位 POWER 取值 top:", collections.Counter(
    v for w, v in allv if len(w) == 9).most_common(8))
print()
print("--- 短号孤儿的 RELOAD / STABILITY 是否出负 ---")
for attr in ("RELOAD", "STABILITY", "COOLTIME"):
    xs = [(w, v) for grp in byattr.get(attr, {}).values() for w, v in grp]
    neg = [(w, v) for w, v in xs if len(w) < 9 and w not in MELEE and v < 0]
    pos = [(w, v) for w, v in xs if len(w) == 9 and v < 0]
    print("%-11s 短号孤儿负数 %4d 条；9 位负数 %4d 条；短号负数例 %s"
          % (attr, len(neg), len(pos), neg[:3]))

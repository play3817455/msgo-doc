# -*- coding: utf-8 -*-
"""MSMA_MODULE placeholder 均一性 + 与 CHARA_PARAM 的 32 缺口明细。只读。"""
import os
from collections import Counter

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")


def data(rel):
    with open(os.path.join(SEED, rel), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return [l.rstrip() for l in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
            if l.strip() and not l.lstrip().startswith("#")]


mod = data("msma_module.csv")
bodies = Counter(l.split(",", 1)[1] for l in mod)
print("MSMA_MODULE 行 %d ／ 不同 payload 形态 %d" % (len(mod), len(bodies)))
for b, n in bodies.most_common(5):
    print("   x%-4d %r" % (n, b))

cp = {l.split(",", 1)[0].strip() for l in data("msma_settings.csv")}
mm = {l.split(",", 1)[0].strip() for l in mod}
miss = sorted(cp - mm)
extra = sorted(mm - cp)
print()
print("缺（CHARA_PARAM 有、MSMA_MODULE 无）%d 台:" % len(miss))
# 附上名字
name = {l.split(",", 1)[0].strip(): (l.split(",")[5] if len(l.split(",")) > 5 else "") for l in data("msma_settings.csv")}
for k in miss:
    print("   %-9s %s" % (k, name.get(k, "")))
print()
print("反向多（MSMA_MODULE 有、CHARA_PARAM 无）%d 台: %s" % (len(extra), extra))

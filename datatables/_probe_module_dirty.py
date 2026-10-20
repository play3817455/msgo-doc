# -*- coding: utf-8 -*-
"""MSMA_MODULE 脏行核查：col0 == 0 / col0 == 101286001 是否与 1124102 行 payload 相同。只读。"""
import io
import os

P = os.path.join(r"f:\9ymsgo\9you",
                 "server/datafiles/lounge/msma/msma_module.csv")

rows = []
with io.open(P, encoding="utf-8", errors="replace") as f:
    for line in f:
        s = line.rstrip("\r\n")
        if not s.strip() or s.lstrip().startswith("#"):
            continue
        rows.append(s)

print("数据行数:", len(rows))
by = {}
for r in rows:
    k = r.split(",")[0].strip()
    by.setdefault(k, []).append(r)

print("col0 唯一键:", len(by))
for k in ("0", "101286001", "1124102"):
    print("--- col0 = %s  命中 %d 行 ---" % (k, len(by.get(k, []))))
    for r in by.get(k, [])[:3]:
        print("   ", r)

ref = by.get("1124102", [""])[0].split(",", 1)
for k in ("0", "101286001"):
    for r in by.get(k, []):
        p = r.split(",", 1)
        same = len(p) > 1 and len(ref) > 1 and p[1] == ref[1]
        print("col0=%-10s payload(去掉col0) 与 1124102 相同? %s" % (k, same))

# 是否为 668 个键里的杂键
allk = sorted(by.keys())
print("前 6 键:", allk[:6], "  含 0?", "0" in by, "  含 101286001?", "101286001" in by)

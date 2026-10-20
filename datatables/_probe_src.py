# -*- coding: utf-8 -*-
"""4 个非名册 練度ID（1123021/1164022/1147052/1155051）在各 msma_*.csv 的出现情况。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")
KEYS = ["1123021", "1164022", "1147052", "1155051"]

files = sorted(f for f in os.listdir(SEED) if f.endswith(".csv"))
print("%-32s %s" % ("file", " ".join("%9s" % k for k in KEYS)))
for fn in files:
    with open(os.path.join(SEED, fn), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8", "replace").replace("\r\n", "\n")
    cols = []
    for k in KEYS:
        n = 0
        for ln in text.split("\n"):
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            if ln.split(",", 1)[0].strip() == k:
                n += 1
        cols.append(n)
    if any(cols):
        print("%-32s %s" % (fn, " ".join("%9d" % c for c in cols)))

print()
# 名册（favms_ok_list 源）
SRC = os.path.join(ROOT, "unpacked", "shell", "settings_extract", "settings", "favms_ok_list.csv")
with open(SRC, "rb") as f:
    raw = f.read()
ids = set()
for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
    ln = ln.lstrip("\ufeff")
    if not ln.strip() or ln.lstrip().startswith("#"):
        continue
    p = ln.split(",")
    head = p[0].strip() if len(p) >= 2 and p[0].strip().isdigit() else ""
    if not head:
        for ch in ln:
            if ch.isdigit():
                head += ch
            else:
                break
    if head:
        ids.add(head)
print("favms_ok_list 名册命中:", {k: (k in ids) for k in KEYS})

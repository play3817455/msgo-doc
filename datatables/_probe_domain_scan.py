# -*- coding: utf-8 -*-
"""全 lounge 种子 CSV 首列域体检：哪些表首列像練度ID，以及相对 CHARA_PARAM 的孤儿。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")


def first_col(rel):
    with open(os.path.join(SEED, rel), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    vals = []
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        vals.append(ln.split(",", 1)[0].strip())
    return vals


def walk():
    for dirpath, _, files in os.walk(SEED):
        if "_bak" in dirpath or "_stub_keep" in dirpath:
            continue
        for fn in sorted(files):
            if fn.endswith(".csv"):
                rel = os.path.relpath(os.path.join(dirpath, fn), SEED).replace(os.sep, "/")
                yield rel


param = set(first_col("msma/msma_settings.csv"))
print("CHARA_PARAM 键数:", len(param))
print()
print("%-42s %6s %6s %8s %8s" % ("csv", "rows", "uniq", "全数字", "孤儿"))
for rel in walk():
    vals = first_col(rel)
    uniq = set(vals)
    if not vals:
        continue
    numeric = all(v.isdigit() for v in vals)
    # 疑似練度ID：7 位且以 '11' 开头
    looks = sum(1 for v in uniq if v.isdigit() and len(v) == 7 and v.startswith("1"))
    orphan = ""
    if looks >= max(1, len(uniq) * 0.9):
        o = uniq - param
        if o:
            orphan = "%d" % len(o)
    print("%-42s %6d %6d %8s %8s" % (rel, len(vals), len(uniq), "Y" if numeric else "-", orphan))

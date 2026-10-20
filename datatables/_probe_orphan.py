# -*- coding: utf-8 -*-
"""对比 msma_settings.csv 各历史副本的键集合，定位被删掉的 698 vs 700。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

COPIES = {
    "current":  "server/datafiles/lounge/msma/msma_settings.csv",
    "col38bak": "server/datafiles/lounge/msma/_bak_col38_20260928/msma_settings.csv",
    "stubkeep": "server/datafiles/_stub_keep/msma/msma_settings.csv",
    "shipbak":  "_bak_ship_20260928-134748/msma/msma_settings.csv",
}


def load(rel):
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    if not os.path.exists(p):
        return None
    with open(p, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    hdr, d = None, {}
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip():
            continue
        if ln.lstrip().startswith("#"):
            if hdr is None:
                hdr = ln.rstrip()
            continue
        k = ln.split(",", 1)[0].strip()
        d[k] = ln.rstrip("\n")
    return hdr, d


sets = {}
for name, rel in COPIES.items():
    r = load(rel)
    if r is None:
        print("%-10s MISSING" % name)
        continue
    hdr, d = r
    sets[name] = d
    print("%-10s rows=%4d" % (name, len(d)))

print()
base = "shipbak"
for name in sets:
    if name == base:
        continue
    only_base = sorted(set(sets[base]) - set(sets[name]))
    only_this = sorted(set(sets[name]) - set(sets[base]))
    print("shipbak vs %-9s: shipbak 独有=%s  %s 独有=%s"
          % (name, only_base, name, only_this))

print()
print("== shipbak 独有的行内容 ==")
for k in sorted(set(sets[base]) - set(sets["current"])):
    print("  %s -> %s" % (k, sets[base][k][:140]))

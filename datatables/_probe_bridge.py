# -*- coding: utf-8 -*-
"""名桥（练度ID-モデルID-全集.csv）与 CHARA_PARAM 键域的覆盖关系。只读。"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")
BRIDGE = os.path.join(ROOT, "datatables", "names", "练度ID-モデルID-全集.csv")


def data_rows(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        yield ln.rstrip()


def keys(rel):
    return {r.split(",", 1)[0].strip() for r in data_rows(os.path.join(SEED, rel))}


bridge = {}
for r in data_rows(BRIDGE):
    c = r.split(",")
    bridge[c[0].strip()] = c[1].strip() if len(c) > 1 else ""

cur = keys("msma/msma_settings.csv")
print("bridge 键数        :", len(bridge))
print("CHARA_PARAM 当前键 :", len(cur))
print("交集               :", len(cur & set(bridge)))
print("PARAM 不在桥里的    :", len(cur - set(bridge)))
print("桥不在 PARAM 里的    :", len(set(bridge) - cur))

print()
for k in ("1123021", "1164022", "1147052", "1155051"):
    print("  %s  in_bridge=%-5s model=%s" % (k, k in bridge, bridge.get(k, "-")))

print()
print("PARAM 不在桥里（前 40）:")
for k in sorted(cur - set(bridge))[:40]:
    print("   ", k)

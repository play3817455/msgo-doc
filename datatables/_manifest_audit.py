# -*- coding: utf-8 -*-
"""精确刻画 cfgsync 前后差异：
   - 数据行（非 # 行）是否变化（只有我改的 5 张表应变化）
   - 表头注释块（# 行）是否变化，以及旧表头是否 == 种子文件表头
"""
import io
import os
import pickle
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
old = pickle.load(open(os.path.join(HERE, "_out_manifest_snapshot.pkl"), "rb"))
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TARGET = {"PLAY_BONUS_REWARD", "PLAYER_NAVI", "BUFF", "MODULE_DEVELOP", "MISSION_EXTRULE"}


def split(raw):
    txt = (raw or b"").decode("utf-8", "replace")
    head, data = [], []
    for line in txt.split("\n"):
        s = line.rstrip("\r")
        if not s.strip():
            continue
        (head if s.lstrip().startswith("#") else data).append(s)
    return head, data


with psycopg.connect(DSN) as c, c.cursor() as cur:
    cur.execute("SELECT file, raw_csv, header_text FROM meta.cfg_manifest")
    new = {r[0]: (r[1], r[2]) for r in cur.fetchall()}

oh, od = {}, {}
nh, nd = {}, {}
for t, row in old.items():
    oh[t], od[t] = split(row[3])
for t, (raw, htxt) in new.items():
    nh[t], nd[t] = split(raw)

data_changed = [t for t in old if t in new and od[t] != nd[t]]
head_changed = [t for t in old if t in new and oh[t] != nh[t]]
print(f"表数 {len(old)}；数据行变化: {len(data_changed)} → {sorted(data_changed)}")
print(f"表头变化: {len(head_changed)}")
print(f"  其中非目标表: {len([t for t in head_changed if t not in TARGET])}")

# 旧表头 vs 种子文件表头
same_as_seed = diff_from_seed = missing_seed = 0
odd = []
for t in head_changed:
    spec_path = os.path.join(SCHEMA, t + ".json")
    if not os.path.isfile(spec_path):
        continue
    import json
    spec = json.load(open(spec_path, encoding="utf-8"))
    seed = os.path.join(SEED_ROOT, *spec["csv_path"].split("/"))
    if not os.path.isfile(seed):
        missing_seed += 1
        odd.append((t, "no-seed"))
        continue
    sh, _ = split(open(seed, "rb").read())
    if sh == oh[t]:
        same_as_seed += 1
    else:
        diff_from_seed += 1
        odd.append((t, f"seed_header_lines={len(sh)} old_header_lines={len(oh[t])}"))
print(f"  旧表头 == 种子表头: {same_as_seed}；不等: {diff_from_seed}；无种子: {missing_seed}")
for t, why in odd[:15]:
    print(f"     {t}: {why}")

print()
print("目标 5 表数据行数 old/new:")
for t in sorted(TARGET):
    print(f"   {t:20s} old={len(od.get(t,[]))} new={len(nd.get(t,[]))} 表头 old={len(oh.get(t,[]))} new={len(nh.get(t,[]))}")
json_ok = len(oh) == len(nh)
print("表头行数对比（抽样）:")
for t in ["BYWORD", "MISSION_GROUP", "WEAPON_SETTING", "CHARACTER", "ITEM"]:
    if t in oh:
        print(f"   {t:16s} old={len(oh[t])} new={len(nh[t])}")

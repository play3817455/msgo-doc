# -*- coding: utf-8 -*-
"""n2 深挖：成长/等级类表的"值"是不是真值。

重点回答三个可证伪的问题：
  Q1 `#11 LVUP_PILOT`.reward_id / `#13 LVUP_PILOT_CLASS`.reward_item_id 的取值
     落在 `cfg."ITEM"` 的键域里吗？（写的是奖励物品 ID，就必须能在 ITEM 表里找到）
  Q2 `#13` 的 rank_point_threshold 是不是严格 = class_id*10000（Go 注释声称的"客户端投影"）？
  Q3 `#12 LVUP_PILOT_EXAM` 的 22 行枚举名全集是什么？是否与 schema 枚举域自洽？

只读。
"""
import io
import json
import os
import re

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def cells(lines, i):
    """第 i 格（去空白）"""
    out = []
    for ln in lines:
        f = ln.split(",")
        out.append(f[i].strip() if i < len(f) else "")
    return out


def data_lines(path):
    t = open(path, "rb").read().decode("utf-8", "replace")
    if t.startswith("\ufeff"):
        t = t[1:]
    return [ln.rstrip() for ln in t.replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()

    # ---- ITEM 键域（权威：cfg."ITEM"）----
    cur.execute('select btrim(item_id::text) from cfg."ITEM"')
    item_keys = set(r[0] for r in cur.fetchall())
    print("cfg.ITEM 键域 %d 个；样例 %s" % (len(item_keys), sorted(item_keys)[:5]))
    # 去掉前导零后的同形集（ITEM 里 8 位带前导零，练度ID 系是 7/9 位）
    item_norm = set(k.lstrip("0") for k in item_keys)

    # ---- #11 LVUP_PILOT ----
    p11 = os.path.join(ROOT, "server/datafiles/lounge/growth/lvup_pilot.csv")
    L11 = data_lines(p11)
    lv = cells(L11, 0)
    reward_id = cells(L11, 41)
    gp = cells(L11, 42)
    sp = cells(L11, 44)
    print("\n== #11 LVUP_PILOT ==")
    print("  行 %d；col41 reward_id 样例 %s" % (len(L11), reward_id[:6]))
    print("  col42 bonus_gp 样例 %s / col44 skill_point 样例 %s" % (gp[:6], sp[:6]))
    hit = [v for v in reward_id if v and v in item_keys]
    hitn = [v for v in reward_id if v and v.lstrip("0") in item_norm and v not in item_keys]
    print("  reward_id ∈ ITEM(原样) %d / %d ；去前导零后命中 %d" % (len(hit), len(reward_id), len(hitn)))
    bad = sorted(set(v for v in reward_id if v and v not in item_keys and v.lstrip("0") not in item_norm))
    print("  ★既非原样也非去零命中的取值 %d 个：%s" % (len(bad), bad[:15]))
    # formula check
    f41 = all(reward_id[i] == str(int(lv[i]) * 100) for i in range(len(lv)) if lv[i].isdigit())
    f42 = all(gp[i] == str(int(lv[i]) * 100) for i in range(len(lv)) if lv[i].isdigit())
    f44 = all(sp[i] == str(int(lv[i]) * 100) for i in range(len(lv)) if lv[i].isdigit())
    print("  公式判定：col41==lv*100? %s ; col42==lv*100? %s ; col44==lv*100? %s" % (f41, f42, f44))
    print("  col35 唯一值 %s" % sorted(set(cells(L11, 35)))[:5])

    # ---- #13 LVUP_PILOT_CLASS ----
    p13 = os.path.join(ROOT, "server/datafiles/lounge/growth/lvup_class.csv")
    L13 = data_lines(p13)
    cl = cells(L13, 0)
    thr = cells(L13, 1)
    ritem = cells(L13, 13)
    print("\n== #13 LVUP_PILOT_CLASS ==")
    print("  行 %d；class_id 域 %s..%s" % (len(L13), cl[0], cl[-1]))
    okthr = all(thr[i] == str(int(cl[i]) * 10000) for i in range(len(cl)) if cl[i].isdigit())
    print("  col1 == class_id*10000 ? %s （样例 %s）" % (okthr, thr[:5]))
    print("  col13 reward_item_id 样例 %s" % ritem[:6])
    hit13 = [v for v in ritem if v and (v in item_keys or v.lstrip("0") in item_norm)]
    print("  reward_item_id ∈ ITEM %d / %d" % (len(hit13), len(ritem)))
    bad13 = sorted(set(v for v in ritem if v and v not in item_keys and v.lstrip("0") not in item_norm))
    print("  ★未命中取值 %d 个：%s" % (len(bad13), bad13[:15]))
    print("  col3 rank_name 唯一值 %s" % sorted(set(cells(L13, 3)))[:6])

    # ---- #12 LVUP_PILOT_EXAM ----
    p12 = os.path.join(ROOT, "server/datafiles/lounge/growth/lvup_exam.csv")
    L12 = data_lines(p12)
    print("\n== #12 LVUP_PILOT_EXAM ==")
    print("  行 %d" % len(L12))
    for ln in L12:
        f = ln.split(",")
        print("   ", " | ".join(x.strip() for x in f))

    # ---- #15 LVUP_CLAN ----
    p15 = os.path.join(ROOT, "server/datafiles/lounge/growth/lvup_clan.csv")
    L15 = data_lines(p15)
    clv = cells(L15, 0)
    need = cells(L15, 1)
    print("\n== #15 LVUP_CLAN ==")
    print("  行 %d；level %s..%s" % (len(L15), clv[0], clv[-1]))
    f15 = all(need[i] == str(10 * int(clv[i]) * (int(clv[i]) + 10)) for i in range(len(clv)) if clv[i].isdigit())
    print("  col1 == 10*L*(L+10) ? %s （样例 %s）" % (f15, need[:5]))
    filled = {}
    for i in range(13):
        vals = [v for v in cells(L15, i) if v]
        filled[i] = len(set(vals))
    print("  各列唯一值数：%s" % filled)

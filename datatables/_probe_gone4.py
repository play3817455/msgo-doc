# -*- coding: utf-8 -*-
"""P2-2 删掉的 4 个 8 位号：在 ITEM 里到底是什么？在 unlockw 里被谁用？只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
GONE = ["12010101", "12840101", "13200151", "13200251"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("== cfg.ITEM ==")
    for k in GONE:
        cur.execute("select btrim(item_id), btrim(name), btrim(item_type) from cfg.\"ITEM\""
                    " where btrim(item_id)=%s", (k,))
        print("   %-10s %s" % (k, cur.fetchall() or "（ITEM 无此号）"))
    print()
    print("== cfg.ITEM 里 120101xx / 128401xx 一片 ==")
    for pat in ("120101%", "128401%", "132001%", "132002%"):
        cur.execute("select btrim(item_id), btrim(name), btrim(item_type) from cfg.\"ITEM\""
                    " where btrim(item_id) like %s order by 1 limit 8", (pat,))
        print("   %-10s %s" % (pat, cur.fetchall()))
    print()
    print("== unlockw 里这 4 个的上下文 ==")
    cur.execute("select item_id, pilot_id, uniqid_ms, world_id from game.unlockw"
                " where item_id::text = any(%s)", (GONE,))
    print("   %s" % cur.fetchall())
    print()
    print("== unlockw 全部 distinct item_id 的号长分布 ==")
    cur.execute("select item_id::text from game.unlockw")
    ks = [r[0] for r in cur.fetchall()]
    d = {}
    for k in set(ks):
        d[len(k)] = d.get(len(k), 0) + 1
    print("   %s  （总 %d 行 / %d 去重）" % (d, len(ks), len(set(ks))))
    print()
    print("== 其中不带 '2' 前缀（= 非 9 位新号）的 ==")
    print("   %s" % sorted(k for k in set(ks) if not k.startswith("2")))

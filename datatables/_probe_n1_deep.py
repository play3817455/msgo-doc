# -*- coding: utf-8 -*-
"""n1 深挖（只读）：
 ① MSMA_BREAKUP / CHARA_MODEL 的"库非空"是真值还是空串（占位判定）；
 ② MSMA_RENTAL 与 CHARA_PARAM 的键集是否逐键相同、值差异落在哪些列；
 ③ CHARA_PARAM 的 battle_detail_key_* 覆盖集 vs #34 MSMA_BATTLE_DETAIL 覆盖集（配套性）。
"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def cols_of(cur, t):
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name=%s order by ordinal_position",
        (t,),
    )
    return [r[0] for r in cur.fetchall()]


def nonempty(cur, t, c):
    """返回该列"非空串"的行数。"""
    cur.execute('select count(*) from cfg."%s" where coalesce(%s::text,\'\') <> \'\'' % (t, c))
    return cur.fetchone()[0]


with psycopg.connect(DSN) as c:
    cur = c.cursor()

    print("=" * 78)
    print("① 占位判定：库非空列里，真正有值的有多少")
    for t in ("MSMA_BREAKUP", "CHARA_MODEL"):
        cs = [x for x in cols_of(cur, t) if x != "_row_id"]
        print("## %s（%d 个数据列）" % (t, len(cs)))
        for c_ in cs:
            n = nonempty(cur, t, c_)
            print("   %-34s 非空串 %3d" % (c_, n))

    print()
    print("=" * 78)
    print("② MSMA_RENTAL vs CHARA_PARAM")
    cur.execute('select msma_id from cfg."CHARA_PARAM" order by 1')
    a = [r[0] for r in cur.fetchall()]
    cur.execute('select msma_id from cfg."MSMA_RENTAL" order by 1')
    b = [r[0] for r in cur.fetchall()]
    print("   CHARA_PARAM %d 键 / MSMA_RENTAL %d 键" % (len(a), len(b)))
    print("   键集相同:", set(a) == set(b), "／ 顺序相同:", a == b)
    ca = [x for x in cols_of(cur, "CHARA_PARAM") if x != "_row_id"]
    cb = [x for x in cols_of(cur, "MSMA_RENTAL") if x != "_row_id"]
    print("   列名差异: 仅 CHARA_PARAM 有 =", sorted(set(ca) - set(cb)),
          "／ 仅 MSMA_RENTAL 有 =", sorted(set(cb) - set(ca)))
    # 对齐默认列名后逐列比值（列名已按 ordinal 一一对应）
    diff_cols = []
    if len(ca) == len(cb):
        for i, (x, y) in enumerate(zip(ca, cb)):
            cur.execute(
                'select count(*) from cfg."CHARA_PARAM" p join cfg."MSMA_RENTAL" r '
                'on p.msma_id=r.msma_id where coalesce(p.%s::text,\'\') is distinct from '
                'coalesce(r.%s::text,\'\')' % (x, y))
            n = cur.fetchone()[0]
            if n:
                diff_cols.append((i, x, y, n))
        print("   逐列（按 ordinal 对齐）值不同的列 %d 个：" % len(diff_cols))
        for i, x, y, n in diff_cols:
            print("     col%-3d %-30s / %-30s 不同 %d 行" % (i, x, y, n))
    else:
        print("   列数不等 %d vs %d，跳过逐列比对" % (len(ca), len(cb)))

    print()
    print("=" * 78)
    print("③ CHARA_PARAM 的 battle_detail_key_* 覆盖 vs #34 覆盖")
    for key in ("battle_detail_key_warp", "battle_detail_key_max_hp",
                "battle_detail_key_energy", "battle_detail_key_jump"):
        n = nonempty(cur, "CHARA_PARAM", key)
        print("   #4  %-30s 非空串 %3d" % (key, n))
    cur.execute(
        "select count(distinct entry_key) from cfg.\"MSMA_BATTLE_DETAIL\"")
    print("   #34 覆盖机体数 =", cur.fetchone()[0])
    cur.execute(
        "select count(distinct msma_id) from cfg.\"CHARA_PARAM\" "
        "where coalesce(battle_detail_key_warp::text,'') <> ''")
    print("   #4  填了 warp 键的机体数 =", cur.fetchone()[0])
    cur.execute(
        'select count(*) from (select distinct entry_key from cfg."MSMA_BATTLE_DETAIL") d '
        'where not exists (select 1 from cfg."CHARA_PARAM" p where p.msma_id = d.entry_key '
        "  and coalesce(p.battle_detail_key_warp::text,'') <> '')")
    print("   #34 有、但 #4 没填键的机体数 =", cur.fetchone()[0])
    cur.execute(
        'select count(*) from (select distinct msma_id from cfg."CHARA_PARAM" '
        "  where coalesce(battle_detail_key_warp::text,'') <> '') p "
        'where not exists (select 1 from cfg."MSMA_BATTLE_DETAIL" d where d.entry_key = p.msma_id)')
    print("   #4 填了键、但 #34 无覆盖的机体数 =", cur.fetchone()[0])
    cur.execute(
        'select entry_key from (select distinct entry_key from cfg."MSMA_BATTLE_DETAIL") d '
        'where not exists (select 1 from cfg."CHARA_PARAM" p where p.msma_id = d.entry_key '
        "  and coalesce(p.battle_detail_key_warp::text,'') <> '') order by 1")
    rs = [r[0] for r in cur.fetchall()]
    print("   明细(%d): %s" % (len(rs), rs))
    print()
    print("   #4 里没填 warp 键的机体（应是 #4 有而 #34 无)样例：")
    cur.execute(
        'select msma_id, name from cfg."CHARA_PARAM" '
        "where coalesce(battle_detail_key_warp::text,'') = '' order by msma_id limit 15")
    for k, n in cur.fetchall():
        print("     %-9s %s" % (k, n))

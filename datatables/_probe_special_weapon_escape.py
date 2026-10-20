# -*- coding: utf-8 -*-
"""查证「特殊机体/特殊武器」的 FX 逃生口：
① 客户端本地 settings/weapon_visual_customize.csv 里的特殊武器 ID 是否落在我们下发的键空间（#37 / #1 / ITEM）
② #DAMAGE_FIELD_PARAM 唯一的显式 fx_resource 列现状 + 该表 19 列取值形态
只读。
"""
import csv
import io
import os

import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "unpacked", "shell", "settings_extract", "settings")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

rows = []
for fn in ("weapon_visual_customize.csv", "weapon_wrestle.csv"):
    with io.open(os.path.join(S, fn), encoding="utf-8", errors="replace", newline="") as f:
        r = [x for x in csv.reader(f) if x and not x[0].lstrip().startswith("#")]
    rows.append((fn, r))

with psycopg.connect(DSN) as c:
    cur = c.cursor()

    fn, r = rows[0]
    ids = [x[0].strip() for x in r if x and x[0].strip()]
    print("=== ① %s：%d 条特殊武器覆盖 ===" % (fn, len(ids)))
    for tbl, col in (('WEAPON_SETTING', 'weapon_setting_id'),
                     ('MSMA_WEAPONSET', None),
                     ('ITEM', None)):
        if col:
            cur.execute('select count(*) from cfg."%s" where btrim(%s) = any(%%s)'
                        % (tbl, col), (ids,))
        else:
            cur.execute("select column_name from information_schema.columns"
                        " where table_schema='cfg' and table_name=%s"
                        "   and column_name <> '_row_id' order by ordinal_position",
                        (tbl,))
            c0 = cur.fetchall()[0][0]
            cur.execute('select count(*) from cfg."%s" where btrim("%s"::text) = any(%%s)'
                        % (tbl, c0), (ids,))
        print("   命中 cfg.%-16s : %d / %d" % (tbl, cur.fetchone()[0], len(ids)))

    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"'
                ' where btrim(weapon_setting_id) = any(%s)', (ids,))
    hit = {x[0] for x in cur.fetchall()}
    print("   #37 命中：%s" % sorted(hit))
    print("   #37 未命中的 %d 条：%s" % (len(set(ids) - hit), sorted(set(ids) - hit)))
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category)'
                ' from cfg."WEAPON_SETTING" where btrim(weapon_setting_id) = any(%s)'
                ' order by 1', (sorted(hit),))
    for a, b in cur.fetchall():
        print("      %s  %s" % (a, b))

    fn, r = rows[1]
    ids2 = sorted({x[0].strip() for x in r if x and x[0].strip()})
    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING" where'
                ' btrim(weapon_setting_id) = any(%s)', (ids2,))
    hit = {x[0] for x in cur.fetchall()}
    print()
    print("=== ① %s：%d 条近接武器显式 FX（ヒット/刀身/剣影エフェクト）===" % (fn, len(ids2)))
    print("   命中 #37：%d / %d ；未命中：%s"
          % (len(hit), len(ids2), sorted(set(ids2) - hit)))

    print()
    print("=== ② #DAMAGE_FIELD_PARAM（19 列）取值形态 ===")
    cur.execute("select column_name from information_schema.columns"
                " where table_schema='cfg' and table_name='DAMAGE_FIELD_PARAM'"
                " order by ordinal_position")
    cols = [x[0] for x in cur.fetchall()]
    cur.execute('select count(*) from cfg."DAMAGE_FIELD_PARAM"')
    print("   行数 %d ／ 列 %s" % (cur.fetchone()[0], cols))
    for cc in cols:
        if cc == "_row_id":
            continue
        cur.execute('select count(*) from cfg."DAMAGE_FIELD_PARAM"'
                    ' where "%s" is not null and btrim("%s"::text) <> \'\'' % (cc, cc))
        nz = cur.fetchone()[0]
        cur.execute('select btrim(coalesce("%s"::text,\'\')), count(*) from cfg."DAMAGE_FIELD_PARAM"'
                    ' group by 1 order by 2 desc limit 3' % cc)
        top = cur.fetchall()
        print("   %-22s 非空 %3d  取值 %s" % (cc, nz, top))

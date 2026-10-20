# -*- coding: utf-8 -*-
"""MODULE(#50) / MODULE_RENTAL(#71) / MODULE_DEVELOP(#51) / MODULE_BONUS(#52) / MODULE_BONUS_LOT(#70)
的结构与内容体检（07-模块与能量攻关 §4.3 说 module/module.csv 是空的）。只读。"""
import io
import json
import os

import psycopg

ROOT = r"f:\9ymsgo\9you"
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

T = ["MODULE", "MODULE_RENTAL", "MODULE_DEVELOP", "MODULE_BONUS", "MODULE_BONUS_LOT"]


def main():
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        for name in T:
            print("=" * 60)
            print("## %s" % name)
            sp = os.path.join(ROOT, "db_design/schema/cfg/tables/%s.json" % name)
            if os.path.exists(sp):
                d = json.load(io.open(sp, encoding="utf-8"))
                cols = d.get("columns") or []
                print("  csv_path=%s 列数=%d reader=%s"
                      % (d.get("csv_path"), len(cols), d.get("asm_reader")))
                print("  purpose=%s" % (d.get("purpose") or "")[:70])
            try:
                cur.execute('select count(*) from cfg."%s"' % name)
                n = cur.fetchone()[0]
                print("  db.cfg 行数=%d" % n)
                if n:
                    cur.execute(
                        "select column_name from information_schema.columns "
                        "where table_schema='cfg' and table_name=%s "
                        "and column_name<>'_row_id' order by ordinal_position",
                        (name,),
                    )
                    dbcols = [r[0] for r in cur.fetchall()]
                    sel = ", ".join(
                        "count(*) filter (where nullif(%s,'') is not null) " % ('"%s"' % cc)
                        for cc in dbcols
                    )
                    cur.execute('select %s from cfg."%s"' % (sel, name))
                    cnts = cur.fetchone()
                    nz = [(dbcols[i], cnts[i]) for i in range(len(dbcols)) if cnts[i]]
                    print("  非空(*非空串*)列 %d 个:" % len(nz))
                    for cc, k in nz:
                        print("     %-32s %5d" % (cc, k))
                    cur.execute('select * from cfg."%s" limit 3' % name)
                else:
                    print("  ⚠ 空表")
            except Exception as e:  # noqa: BLE001
                print("  ERR %s" % e)


if __name__ == "__main__":
    main()

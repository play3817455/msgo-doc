# -*- coding: utf-8 -*-
"""收尾取证：DAMAGE_FIELD_PARAM.col13（真 FX 路径列）+ cfg.BUILDUP_WEAPON 内容。

只报告，不写。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        for t in ("DAMAGE_FIELD_PARAM", "BUILDUP_WEAPON", "MECHANIC_WEAPON"):
            cur.execute("""select column_name from information_schema.columns
                            where table_schema='cfg' and table_name=%s
                            order by ordinal_position""", (t,))
            cols = [r[0] for r in cur.fetchall()]
            cur.execute('select count(*) from cfg."%s"' % t)
            n = cur.fetchone()[0]
            print("== cfg.%-22s 列 %d 行 %d" % (t, len(cols), n))
            if t == "BUILDUP_WEAPON":
                cur.execute('select * from cfg."BUILDUP_WEAPON" order by buildup_id limit 5')
                for r in cur.fetchall():
                    print("   ", r)
                cur.execute('''select count(*) from cfg."BUILDUP_WEAPON"
                                where %s''' % " or ".join(
                    '"%s" is not null and btrim("%s"::text) <> \'\' and btrim("%s"::text) <> \'0\''
                    % (c, c, c) for c in cols[1:]))
                print("   非零格行数:", cur.fetchone()[0])
            if t == "DAMAGE_FIELD_PARAM":
                # 找 col13
                cur.execute('''select column_name from information_schema.columns
                                where table_schema='cfg' and table_name='DAMAGE_FIELD_PARAM'
                                order by ordinal_position''')
                names = [r[0] for r in cur.fetchall()]
                c13 = names[14] if len(names) > 14 else names[-1]
                print("   第 14 物理列（含 _row_id 时 = csv 13）:", c13)
                cur.execute('select btrim("%s"::text), count(*) from cfg."DAMAGE_FIELD_PARAM" group by 1 order by 2 desc limit 8' % c13)
                for v, k in cur.fetchall():
                    print("      %-46r x%d" % (v[:44], k))
                cur.execute('select count(*) from cfg."DAMAGE_FIELD_PARAM" where btrim(coalesce("%s"::text,\'\'))<>\'\'' % c13)
                print("   该列非空行数:", cur.fetchone()[0])
            print()


if __name__ == "__main__":
    main()

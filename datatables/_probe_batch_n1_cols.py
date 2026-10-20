# -*- coding: utf-8 -*-
"""n1 体检②：5 张表的「逐列实际覆盖率」（库 vs 种子），核对 docs 的填充现状声明。只读。"""
import io
import os

import psycopg

ROOT = r"f:\9ymsgo\9you"
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

TABLES = {
    "CHARA_PARAM": "server/datafiles/lounge/msma/msma_settings.csv",
    "CHARA_MODEL": "server/datafiles/lounge/msma/msma_model.csv",
    "MSMA_RENTAL": "server/datafiles/lounge/msma/msma_rental.csv",
    "MSMA_MODULE": "server/datafiles/lounge/msma/msma_module.csv",
    "MSMA_BREAKUP": "server/datafiles/lounge/msma/msma_breakup.csv",
}


def seed_cov(rel):
    """返回 (行数, {列号: 非空行数}, {列号: 取值样例})。"""
    p = os.path.join(ROOT, rel)
    rows = []
    with io.open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.rstrip("\r\n")
            if not s.strip() or s.lstrip().startswith("#"):
                continue
            rows.append(s.split(","))
    if not rows:
        return 0, {}, {}
    ncol = max(len(r) for r in rows)
    cov, samp = {}, {}
    for i in range(ncol):
        k = 0
        first = ""
        for r in rows:
            v = r[i] if i < len(r) else ""
            if v.strip() != "":
                k += 1
                if not first:
                    first = v
        cov[i] = k
        samp[i] = first
    return len(rows), cov, samp


def main():
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        for name, rel in TABLES.items():
            print("=" * 72)
            print("## %s" % name)
            n, cov, samp = seed_cov(rel)
            print("  种子 %d 行，列数 %d" % (n, len(cov)))
            filled = [(i, cov[i]) for i in cov if cov[i] > 0]
            print("  种子非空列 %d 个（列号:行数）:" % len(filled))
            for i, k in filled:
                print("     col%-3d %5d 行  样例=%s" % (i, k, samp[i][:40]))
            # 库侧：取一行的列名，按列统计非空
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema='cfg' and table_name=%s order by ordinal_position",
                (name,),
            )
            dbcols = [r[0] for r in cur.fetchall()]
            print("  库列 %d 个" % len(dbcols))
            if dbcols:
                sel = ", ".join(
                    'count(*) filter (where %s is not null) ' % ('"%s"' % cc) for cc in dbcols
                )
                cur.execute('select count(*), %s from cfg."%s"' % (sel, name))
                row = cur.fetchone()
                total, counts = row[0], row[1:]
                nonempty = [
                    (dbcols[i], counts[i]) for i in range(len(dbcols)) if counts[i] > 0
                ]
                print("  库 %d 行，非空列 %d 个:" % (total, len(nonempty)))
                for cc, k in nonempty:
                    print("     %-28s %5d" % (cc, k))


if __name__ == "__main__":
    main()

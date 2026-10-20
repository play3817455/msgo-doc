# -*- coding: utf-8 -*-
"""_probe_fxid_source.py —— 7 位 FX ID（CC NNN II）到底由哪张表哪列产出？

判据（数据侧、可复跑）：
  ① 从真实资源树 `unpackdat/fx/CC/PP_CC_NNN_II.vra` 反解出**合法 a2 集合**
     （a2 = CC*100000 + NNN*100 + II，与 `sub_4828B0` 的展开式逐位一致）。
  ② 扫全库 `cfg.*` 的每个文本列，统计有多少值**落在合法 a2 集合里**。
     真产出列必然高命中；巧合列（如普通 id）几乎 0 命中。
只报告，不写。
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

FXDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "机动战士敢达Online", "GundamOnline", "unpackdat", "fx")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
PAT = re.compile(r"^PP_(\d{2})_(\d{3})_(\d{2})\.vra$", re.I)


def valid_ids():
    """资源树 → 合法 a2 集合（只取 .vra，图像帧 PP_*_*.png 不算：格式串要求 .vra）"""
    ids = set()
    for d in sorted(os.listdir(FXDIR)):
        p = os.path.join(FXDIR, d)
        if not os.path.isdir(p) or not d.isdigit():
            continue
        for f in os.listdir(p):
            m = PAT.match(f)
            if m:
                cc, nnn, ii = (int(x) for x in m.groups())
                if cc == int(d):          # 目录号 == 文件名首段（格式串传了两次同一个值）
                    ids.add(cc * 100000 + nnn * 100 + ii)
    return ids


def main():
    ids = valid_ids()
    print("资源树合法 a2（7 位打包 FX ID）：%d 个，范围 %d..%d"
          % (len(ids), min(ids), max(ids)))
    print("CC 分布：%s" % dict(sorted(collections.Counter(i // 100000 for i in ids).items())))
    print()

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("select table_name from information_schema.tables where table_schema='cfg' order by 1")
        tables = [r[0] for r in cur.fetchall()]
        cur.execute("select table_name, column_name from information_schema.columns"
                    " where table_schema='cfg' and data_type in ('text','character varying')"
                    " order by table_name, ordinal_position")
        cols = cur.fetchall()

        print("扫 %d 张表 / %d 个文本列 …" % (len(tables), len(cols)))
        hits = []
        for t, c in cols:
            try:
                cur.execute('select "%s" from cfg."%s" where "%s" ~ \'^[0-9]{4,7}$\''
                            % (c, t, c))
            except Exception:
                conn.rollback()
                continue
            vals = [r[0].strip() for r in cur.fetchall() if r[0]]
            if not vals:
                continue
            inids = [v for v in vals if int(v) in ids]
            if inids:
                hits.append((len(inids), len(vals), t, c, inids[:4]))
        conn.rollback()

    hits.sort(reverse=True)
    print()
    print("%-26s %-22s %8s %8s %s" % ("表", "列", "命中a2", "该列数", "样例"))
    for n, tot, t, c, ex in hits[:25]:
        print("%-26s %-22s %8d %8d %s" % (t, c, n, tot, ex))
    if not hits:
        print("（没有任何 cfg 列的取值落在合法 a2 集合里）")


if __name__ == "__main__":
    main()

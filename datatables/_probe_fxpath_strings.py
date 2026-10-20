# -*- coding: utf-8 -*-
"""_probe_fxpath_strings.py —— 资源特效到底跟不跟 ID 绑定？

用户的直觉：特效资源应该是"跟 ID 绑定"（ID 一确定，资源就确定），不该由表再指定。
检验方式：把 cfg 全部 80 张表的**每一个文本列**扫一遍，找有没有任何单元格
  · 长得像 VRA 路径（含 .vra / fx/ 前缀）
  · 长得像 PP_ 前缀的贴图名
并对照资源树里真实的 fx/ 目录形态。

只读，不写。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
UNPACK = os.path.join(ROOT, "unpackdat")

PATHISH = re.compile(r"\.vra|\.dxg|fx/|\bPP_[A-Z0-9_]+", re.IGNORECASE)


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name, data_type
              FROM information_schema.columns
             WHERE table_schema = 'cfg'
             ORDER BY table_name, ordinal_position
        """)
        cols = cur.fetchall()
        cur.execute("""
            SELECT table_name FROM information_schema.tables
             WHERE table_schema = 'cfg' ORDER BY table_name
        """)
        tables = [r[0] for r in cur.fetchall()]

    by_table = {}
    for t, c, dt in cols:
        by_table.setdefault(t, []).append((c, dt))

    print("cfg 表数 %d ／ 列数 %d" % (len(tables), len(cols)))
    hits = []
    text_cols = 0
    for t in tables:
        for c, dt in by_table[t]:
            if dt not in ("text", "character varying", "character"):
                continue
            text_cols += 1
            q = 'SELECT DISTINCT btrim("%s") FROM cfg."%s" WHERE btrim("%s") %%s' % (c, t, c)
            try:
                with psycopg.connect(DSN) as conn:
                    cur = conn.cursor()
                    cur.execute(
                        'SELECT DISTINCT btrim("' + c + '") FROM cfg."' + t + '"'
                    )
                    for (v,) in cur.fetchall():
                        if v and PATHISH.search(v):
                            hits.append((t, c, v))
            except Exception as e:  # noqa: BLE001
                print("  ERR %s.%s %s" % (t, c, e))

    print("文本列 %d 个" % text_cols)
    print()
    print("=== 含 路径/VRA/PP_ 形态的单元格：%d 个 ===" % len(hits))
    seen = {}
    for t, c, v in hits:
        seen.setdefault((t, c), []).append(v)
    for (t, c), vs in sorted(seen.items()):
        print("  %-22s %-22s %d 种，例：%s" % (t, c, len(vs), vs[:3]))

    print()
    print("=== 资源树实况：fx/ 目录形态 ===")
    fxdir = None
    for base, dirs, files in os.walk(ROOT):
        if os.path.basename(base) == "fx" and "unpackdat" in base:
            fxdir = base
            break
    if not fxdir:
        print("  未找到 unpackdat 下的 fx/ 目录")
    else:
        sub = sorted(os.listdir(fxdir))
        print("  %s → %d 个子目录：%s" % (fxdir, len(sub), sub[:12]))
        for d in sub[:3]:
            p = os.path.join(fxdir, d)
            fs = sorted(os.listdir(p)) if os.path.isdir(p) else []
            print("    %s/ %d 个文件，例：%s" % (d, len(fs), fs[:4]))


if __name__ == "__main__":
    main()

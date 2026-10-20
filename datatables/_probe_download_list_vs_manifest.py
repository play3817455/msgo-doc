# -*- coding: utf-8 -*-
"""拿客户端本地 settings/download_list.csv（客户端"我要下哪些表"的权威清单）
   对账服务端 meta.cfg_manifest —— 看有没有多下发/少下发。
只读。
"""
import csv
import io
import os

import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(ROOT, "unpacked", "shell", "settings_extract", "settings",
                  "download_list.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

want = {}
with io.open(DL, encoding="utf-8", errors="replace", newline="") as f:
    for row in csv.reader(f):
        if not row or row[0].lstrip().startswith("#"):
            continue
        want[row[0].strip()] = (row[1].strip() if len(row) > 1 else "")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select column_name from information_schema.columns"
                " where table_schema='meta' and table_name='cfg_manifest'"
                " order by ordinal_position")
    mcols = [r[0] for r in cur.fetchall()]
    cur.execute('select * from meta.cfg_manifest')
    rows = cur.fetchall()

print("download_list.csv 条目 %d ／ meta.cfg_manifest 行 %d" % (len(want), len(rows)))
print("manifest 列：%s" % mcols)
print()

# 找出哪个列像表名 / 哪个像下发文件名 / 哪个像下载序
idx = {n: i for i, n in enumerate(mcols)}
name_i = next((idx[n] for n in ("table_name", "name", "table", "cfg_name") if n in idx), None)
file_i = next((idx[n] for n in ("file_path", "file", "download_path", "path",
                                "csv_path", "download_name") if n in idx), None)
ord_i = next((idx[n] for n in ("download_order", "order_no", "order", "sort_order")
              if n in idx), None)
print("判定：表名列=%r 文件名列=%r 序列=%r"
      % (mcols[name_i] if name_i is not None else None,
         mcols[file_i] if file_i is not None else None,
         mcols[ord_i] if ord_i is not None else None))
print()

# manifest 的 `file` 列存的其实是**表 slug**（`weapon_setting` 这种小写名），
# 不是下发路径 ⇒ 与 download_list 的 col0（`WEAPON_SETTING`）按 slug 规范化对账。
def slug(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


mfiles = {}
for r in rows:
    nm = (r[name_i] or "").strip() if name_i is not None else ""
    fp = (r[file_i] or "").strip() if file_i is not None else ""
    mfiles[slug(fp or nm)] = (fp or nm)

wantp = {slug(k): k for k in want}

only_dl = sorted(set(wantp) - set(mfiles))
only_mf = sorted(set(mfiles) - set(wantp))
print("只在 download_list（客户端要、服务端 manifest 里没有）：%d" % len(only_dl))
for n in only_dl:
    print("   %-30s (%s)" % (wantp[n], n))
print()
print("只在 manifest（服务端有、客户端不要）：%d" % len(only_mf))
for n in only_mf:
    print("   %-30s (%s)" % (mfiles[n], n))
print()
print("交集 %d" % len(set(wantp) & set(mfiles)))

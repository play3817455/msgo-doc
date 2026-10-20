# -*- coding: utf-8 -*-
"""跨表外键体检：所有名字像"物品 ID"的列，取值必须落在 cfg."ITEM" 键域里。

为什么值得扫：`ITEM` 是**唯一**的物品注册表（名称/图标）。任何 `*_item_id` /
`reward_item*` 列写了个不在 ITEM 里的数，客户端查表就落空（奖励发不出来/图标空白），
而这类错**行数与列名审计都看不出来**（值域错 ≠ 结构错）。

口径：
  - 列名正则：`item_id|reward_item|^item|_item$|item_`（大小写不敏感），
    再排除明显不是物品号的（`item_num`/`item_count`/`item_level`/`item_type`/`item_rank`...）。
  - 取值来源 = `meta.cfg_manifest.raw_csv`（= 库的导出），**逐列**取值（列号 = schema csv_index）。
  - 命中判定：① 原样 ∈ ITEM 键域；② 或去前导零后 ∈ ITEM 键域（ITEM 是 8 位带前导零的号）。
  - **空串与 `0` 视为"无奖励"**，不算违规（但单独计数，好知道有多少行是空的）。

输出 datatables/_out_itemid_fk.txt
"""
import io
import json
import os
import re

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_itemid_fk.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

COL_RE = re.compile(r"(item_id|item$|reward_item|reward_id|^item|_item$|item_)", re.I)
# 明显不是"物品号"的列名（是数量/等级/类型/概率/槽位等，值域是自由整数）
NOT_ID = re.compile(r"(num|count|count_|cnt|level|lv|type|rank|rate|prob|slot|max|min|"
                    r"flag|chance|ratio|percent|cost|price|exp|point|value|param|"
                    r"index|idx|order|group|kind|class|category|cat|id2|_id_map)",
                    re.I)


def data_lines(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    return [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


rep = io.StringIO()
with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute('select btrim(item_id::text) from cfg."ITEM"')
    item_raw = set(r[0] for r in cur.fetchall())
    item_norm = set(k.lstrip("0") or "0" for k in item_raw)

    cur.execute("select file, raw_csv from meta.cfg_manifest")
    man = {}
    for f_, raw in cur.fetchall():
        man[f_] = raw if isinstance(raw, str) else (raw.decode("utf-8", "replace") if raw else "")

    checked = 0
    offenders = []
    clean = []
    for fn in sorted(os.listdir(SCHEMA)):
        if not fn.endswith(".json"):
            continue
        spec = json.load(io.open(os.path.join(SCHEMA, fn), encoding="utf-8"))
        t = spec["id"]
        if t not in man:
            continue
        lines = data_lines(man[t])
        if not lines:
            continue
        for col in spec.get("columns") or []:
            nm = col.get("name") or ""
            if not COL_RE.search(nm) or NOT_ID.search(nm):
                continue
            i = col.get("csv_index")
            vals = []
            for ln in lines:
                f = ln.split(",")
                v = f[i].strip() if i < len(f) else ""
                if v:
                    vals.append(v)
            if not vals:
                continue
            checked += 1
            uniq = sorted(set(vals))
            zero = sum(1 for v in vals if v in ("0", "0.0"))
            miss = [v for v in uniq if v not in item_raw and (v.lstrip("0") or "0") not in item_norm]
            rec = (t, col.get("name"), i, len(vals), zero, len(uniq), miss[:6], len(miss))
            (offenders if miss else clean).append(rec)

    rep.write("== 物品ID 列外键体检（值必须 ∈ cfg.ITEM 键域；0/空 = 无奖励，不计违规）==\n")
    rep.write("ITEM 键域 %d 个（8 位带前导零）\n" % len(item_raw))
    rep.write("受检列 %d 个；**未命中 %d 个**\n\n" % (checked, len(offenders)))

    rep.write("---- ★未命中（值域不在 ITEM 里）----\n")
    rep.write("%-26s %-26s %5s %7s %7s %7s %6s  %s\n"
              % ("表", "列名", "csv#", "有值行", "其中0", "唯一值", "未命中", "未命中样例"))
    for t, nm, i, n, z, u, miss, nmiss in offenders:
        rep.write("%-26s %-26s %5d %7d %7d %7d %6d  %s\n" % (t, nm, i, n, z, u, nmiss, miss))

    rep.write("\n---- 命中（合规）----\n")
    rep.write("%-26s %-26s %5s %7s %7s\n" % ("表", "列名", "csv#", "有值行", "唯一值"))
    for t, nm, i, n, z, u, miss, nmiss in clean:
        rep.write("%-26s %-26s %5d %7d %7d\n" % (t, nm, i, n, u))

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print(rep.getvalue())
print("wrote", OUT)

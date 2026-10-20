# -*- coding: utf-8 -*-
"""n2 批次体检：成长/等级类表（#11 LVUP_PILOT / #12 LVUP_PILOT_EXAM / #13 LVUP_PILOT_CLASS
/ #15 LVUP_CLAN / #16 LVUP_FAVMS）。

只读。逐表输出：
  ① schema（列数 / csv_index 域 / 空洞 / 重复 / csv_path / asm_reader）
  ② 三方行数：cfg."<表>" / 种子 CSV / meta.cfg_manifest.raw_csv
  ③ 逐列填充画像：csv_index -> (种子有值行数, manifest 有值行数, 唯一值个数, 样例)
     —— 这一列是本次体检的重点：占位表 vs 真值表的差别全在这里。
  ④ 行键域：种子键集 vs manifest 键集（键差 = 键域漂移）

输出 datatables/_out_batch_n2.txt
"""
import io
import json
import os
from collections import Counter

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_batch_n2.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

TABLES = ["LVUP_PILOT", "LVUP_PILOT_EXAM", "LVUP_PILOT_CLASS", "LVUP_CLAN", "LVUP_FAVMS"]


def data_lines(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    out = []
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        out.append(ln.rstrip())
    return out


def fill_profile(lines, ncol):
    """col -> [非空数, 唯一值集合]"""
    prof = {}
    for i in range(ncol):
        prof[i] = [0, set()]
    for ln in lines:
        f = ln.split(",")
        for i in range(min(ncol, len(f))):
            v = f[i].strip()
            if v != "":
                prof[i][0] += 1
                if len(prof[i][1]) < 400:
                    prof[i][1].add(v)
    return prof


def keys_of(lines):
    return set(ln.split(",")[0].strip() for ln in lines)


rep = io.StringIO()
with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("select file, raw_csv from meta.cfg_manifest")
    man = {}
    for f_, raw in cur.fetchall():
        man[f_] = raw if isinstance(raw, str) else (raw.decode("utf-8", "replace") if raw else "")

    for name in TABLES:
        spec = json.load(io.open(os.path.join(SCHEMA, name + ".json"), encoding="utf-8"))
        cols = spec.get("columns") or []
        idxs = sorted(c_.get("csv_index") for c_ in cols)
        seen = Counter(idxs)
        holes = [i for i in range(min(idxs), max(idxs) + 1) if i not in seen] if idxs else []
        dup = [k for k, v in seen.items() if v > 1]

        rep.write("=" * 96 + "\n")
        rep.write("## #%s %s   (%s)\n" % (spec.get("table_id"), name, spec.get("csv_path")))
        rep.write("   asm_reader=%s  purpose=%s\n"
                  % (spec.get("asm_reader"), (spec.get("purpose") or "")[:70]))
        rep.write("   schema: 列数=%d  csv_index %s..%s  空洞=%s  重复=%s\n"
                  % (len(cols), min(idxs) if idxs else "-", max(idxs) if idxs else "-",
                     holes[:20], dup[:10]))

        cur.execute('select count(*) from cfg."%s"' % name)
        nrow_db = cur.fetchone()[0]

        csvp = (spec.get("csv_path") or "")
        p = os.path.join(LOUNGE, csvp.replace("/", os.sep))
        seed_lines = data_lines(open(p, "rb").read().decode("utf-8", "replace")) if os.path.exists(p) else []
        mf_lines = data_lines(man.get(name, ""))

        rep.write("   行数：db=%d  种子=%d  manifest=%d\n" % (nrow_db, len(seed_lines), len(mf_lines)))

        sk, mk = keys_of(seed_lines), keys_of(mf_lines)
        if sk != mk:
            rep.write("   ★键域漂移：只种子 %d  只manifest %d  例:%s\n"
                      % (len(sk - mk), len(mk - sk),
                         sorted(list(sk - mk) + list(mk - sk))[:12]))
        else:
            rep.write("   键域：一致（%d 键）\n" % len(sk))
        rep.write("   键域样例（前 8 键，升序按数值）: %s\n"
                  % sorted(sk, key=lambda x: (len(x), x))[:8])

        sp = fill_profile(seed_lines, len(idxs))
        mp = fill_profile(mf_lines, len(idxs))
        rep.write("   %-6s %-22s %8s %8s %6s  %s\n"
                  % ("csv#", "schema 订案名", "种子有值", "mf有值", "唯一值", "样例"))
        for c_ in cols:
            i = c_.get("csv_index")
            a = sp.get(i, [0, set()])
            b = mp.get(i, [0, set()])
            if a[0] == 0 and b[0] == 0:
                continue
            samp = sorted(a[1], key=lambda x: (len(x), x))[:4] if a[1] else sorted(b[1])[:4]
            flag = "" if a[0] == b[0] and a[1] == b[1] else "  ★种子/mf 不同"
            rep.write("   %-6s %-22s %8d %8d %6d  %s%s\n"
                      % (i, (c_.get("name") or "")[:22], a[0], b[0], len(a[1]), samp, flag))
        # 全空列统计
        empty_cols = [c_.get("csv_index") for c_ in cols
                      if sp.get(c_.get("csv_index"), [0, set()])[0] == 0]
        rep.write("   全空列（种子侧）%d 个 / %d\n" % (len(empty_cols), len(cols)))
        rep.write("\n")

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print(rep.getvalue())
print("wrote", OUT)

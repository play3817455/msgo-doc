# -*- coding: utf-8 -*-
"""三方对账（种子 CSV / cfg 表 / manifest）总表 -> datatables/_out_threeway.txt（UTF-8）。"""
import io
import json
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCHEMA_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_out_threeway.txt")


def csv_rows(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        raw = f.read()
    n = 0
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if ln.strip() and not ln.lstrip().startswith("#"):
            n += 1
    return n


specs = []
for fn in sorted(os.listdir(SCHEMA_DIR)):
    if fn.endswith(".json"):
        specs.append(json.load(open(os.path.join(SCHEMA_DIR, fn), encoding="utf-8")))

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("select file, row_count, octet_length(raw_csv) from meta.cfg_manifest")
    man = {f: (rc, ln) for f, rc, ln in cur.fetchall()}
    rep = io.StringIO()
    rep.write("%-28s %-8s %-5s %8s %8s %8s  %s\n" %
              ("表", "disposition", "tid", "种子行", "库行", "manifest", "状态"))
    rep.write("-" * 110 + "\n")
    bad = []
    same64 = []
    for s in specs:
        tid = s.get("table_id")
        disp = str(s.get("disposition", "?"))
        csvp = s.get("csv_path", "")
        seed = None
        if csvp and not csvp.startswith("本地"):
            seed = csv_rows(os.path.join(LOUNGE, csvp.replace("/", os.sep)))
        t = s["id"]
        dbn = None
        try:
            cur.execute('select count(*) from cfg."%s"' % t)
            dbn = cur.fetchone()[0]
        except Exception:
            dbn = None
        mrc = man.get(t, (None, None))[0]
        if seed is None and dbn is None:
            st = "库无表"
        elif dbn is None:
            st = "库无表(有CSV)"
        elif seed is None and csvp.startswith("本地"):
            st = "本地表(无CSV)"
        elif seed == dbn:
            st = "OK"
        else:
            st = "**种子≠库 %+d**" % (dbn - seed)
            bad.append((t, tid, seed, dbn))
        if dbn == 64:
            same64.append(t)
        if seed is not None or dbn is not None:
            rep.write("%-28s %-8s %-5s %8s %8s %8s  %s\n" %
                      (t, disp, tid, seed, dbn, mrc, st))
    rep.write("\n== 种子≠库 %d 张 ==\n" % len(bad))
    for t, tid, s, d in bad:
        rep.write("  #%-3s %-26s 种子%d 库%d (%+d)\n" % (tid, t, s, d, d - s))
    rep.write("\n== 库行数恰为 64 的表 %d 张 ==\n" % len(same64))
    rep.write("  " + ", ".join(same64) + "\n")

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)

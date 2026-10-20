# -*- coding: utf-8 -*-
"""格值级三方对账（种子 CSV 行 vs manifest raw_csv 行）-> datatables/_out_cells.txt

行数对账（_scan_threeway.py）看不出"行数相同但格子不同"。本脚本直接比**文本行集合**：
  manifest.raw_csv 是 exportManifest 从库拼的（= 客户端实际收到的字节），
  所以「种子行集合 ≠ manifest 行集合」= ① 与线上真的不一致（哪怕行数相同）。

归一：去 BOM、CRLF->LF、去行尾空白、丢空行与 # 注释行、**丢掉每行末尾的连续空字段**（尾逗号差异）。
输出：逐表 只种子/只manifest 的行数与样例。
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 白名单：这些列**故意**只在一侧有值，不计入漂移（见 16-配置表三方对账总表.md §6.2 P1）。
# #4 CHARA_PARAM 的 csv_index=89 是历史测试导入残留（{10,20,30,40,50}），真实速度取自
# #34 MSMA_BATTLE_DETAIL 的 MOVE，`serverv/internal/store/battle_params.go` 明确忽略该列，
# 故种子回导时刻意留空 —— 判据是"库该清"，不是"种子该补"。
INTENTIONAL_BLANK = {"CHARA_PARAM": (89,)}

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_cells.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def norm_line(ln):
    s = ln.rstrip()
    while s.endswith(","):
        s = s[:-1]
    return s


def lines_of(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    out = []
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        out.append(norm_line(ln))
    return out


def raw_lines(text):
    """未归一：保留尾逗号，用于数"格子宽度"。"""
    if text.startswith("\ufeff"):
        text = text[1:]
    out = []
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        out.append(ln.rstrip())
    return out


def widths(raw):
    """原始字段数分布（含尾逗号产生的空尾格）。"""
    c = {}
    for ln in raw:
        n = len(ln.split(","))
        c[n] = c.get(n, 0) + 1
    return dict(sorted(c.items()))


def blank_cols(lines, idxs):
    """把指定列号置空后再做尾逗号归一（白名单列不参与比对）。"""
    hi = max(idxs)
    out = []
    for ln in lines:
        f = ln.split(",")
        if len(f) <= hi:
            out.append(ln)
            continue
        for i in idxs:
            f[i] = ""
        out.append(norm_line(",".join(f)))
    return out


specs = []
for fn in sorted(os.listdir(SCHEMA)):
    if fn.endswith(".json"):
        specs.append(json.load(io.open(os.path.join(SCHEMA, fn), encoding="utf-8")))

rep = io.StringIO()
with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("select file, raw_csv from meta.cfg_manifest")
    man = {}
    for f_, raw in cur.fetchall():
        man[f_] = raw if isinstance(raw, str) else (raw.decode("utf-8", "replace") if raw else "")

    rep.write("%-30s %-5s %7s %7s %8s %8s %10s %8s  %s\n"
              % ("表", "tid", "种子行", "mf行", "只种子", "只mf", "种子宽", "schema列", "判定"))
    rep.write("-" * 112 + "\n")
    drift = []
    narrow = []
    for s in specs:
        tid = s.get("table_id")
        csvp = s.get("csv_path", "")
        t = s["id"]
        if t not in man:
            continue
        if not csvp or csvp.startswith("本地"):
            continue
        p = os.path.join(LOUNGE, csvp.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        raw = open(p, "rb").read().decode("utf-8", "replace")
        seed = lines_of(raw)
        w = widths(raw_lines(raw))
        ws = max(w) if w else 0
        nsch = len(s.get("columns") or [])
        mfl = lines_of(man[t])
        idxs = INTENTIONAL_BLANK.get(t)
        if idxs:
            seed = blank_cols(seed, idxs)
            mfl = blank_cols(mfl, idxs)
        ss, ms = set(seed), set(mfl)
        only_seed = ss - ms
        only_mf = ms - ss
        ok = not only_seed and not only_mf and len(seed) == len(mfl)
        # schema 比种子宽 ≥2 格 ⇒ 种子无法在 -recreate 时复现该表的全部列
        is_narrow = nsch - ws >= 2
        if not ok:
            drift.append((t, tid, seed, mfl, only_seed, only_mf, csvp))
        if is_narrow:
            narrow.append((t, tid, ws, nsch, list(w.items()), csvp))
        rep.write("%-30s %-5s %7d %7d %8d %8d %10s %8d  %s%s\n"
                  % (t, tid, len(seed), len(mfl), len(only_seed), len(only_mf),
                     ws, nsch, "OK" if ok else "★值不一致",
                     ("  ⚠宽度窄 %d" % (nsch - ws) if is_narrow else "")
                     + ("  (白名单:空 col%s)" % ",".join(str(i) for i in idxs) if idxs else "")))
    rep.write("\n== 格值级不一致 %d 张 ==\n" % len(drift))
    for t, tid, seed, mfl, only_seed, only_mf, csvp in drift:
        rep.write("\n### #%s %s  (种子 %s)\n" % (tid, t, csvp))
        rep.write("    种子 %d 行 ／ mf %d 行 ／ 只种子 %d ／ 只mf %d\n"
                  % (len(seed), len(mfl), len(only_seed), len(only_mf)))
        for x in sorted(only_seed)[:8]:
            rep.write("    [只种子] %s\n" % x[:200])
        if len(only_seed) > 8:
            rep.write("    [只种子] …另 %d 行\n" % (len(only_seed) - 8))
        for x in sorted(only_mf)[:8]:
            rep.write("    [只 mf ] %s\n" % x[:200])
        if len(only_mf) > 8:
            rep.write("    [只 mf ] …另 %d 行\n" % (len(only_mf) - 8))

    rep.write("\n== 种子宽度窄于 schema 的表（`-recreate` 无法复现库列）%d 张 ==\n" % len(narrow))
    rep.write("%-30s %-5s %8s %8s %-28s %s\n" % ("表", "tid", "种子宽", "schema列", "种子字段数分布", "csv"))
    for t, tid, ws, nsch, dist, csvp in narrow:
        rep.write("%-30s %-5s %8d %8d %-28s %s\n"
                  % (t, tid, ws, nsch, str(dist)[:27], csvp))

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print(rep.getvalue())
print("wrote", OUT)

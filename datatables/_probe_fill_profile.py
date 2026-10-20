# -*- coding: utf-8 -*-
"""通用填充画像探针：给定表名清单，一次性回答"这张表有没有内容、内容是不是真值"。

用法：
    python _probe_fill_profile.py MODULE MSMA_FAVMS MECHANIC_MSMA ...
    python _probe_fill_profile.py --all          # 全 79 张（只打摘要行）

对每张表输出：
  ① 三方行数（cfg / 种子 / manifest）+ 键域差；
  ② 逐列填充：有值行数 / 唯一值数 / 样例（种子侧，manifest 侧不一致会标 ★）；
  ③ **列簇**：值向量完全相同的列（一次批量填充的痕迹）；
  ④ **公式命中**：常量 / =id / =id*10 / =id*100 / =id*10000 / =10n(n+10)；
  ⑤ 摘要行：`有值列/总列`、`全空列`、`列簇数`、`公式列数`、`判定`。

判定口径：
  · 有值列 ≤ 1        -> `纯键占位`
  · 全空列 ≥ 半数      -> `内容缺失`
  · 存在 ≥2 列同向量、或有 3+ 列命中同一公式 -> `批量公式占位`
  · 否则               -> `需人工看`
只读。
"""
import io
import json
import os
import sys
from collections import Counter

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_fill_profile.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

FORMULAS = [
    ("const", None),  # 常量列单独判
    ("=id", lambda k: str(int(k))),
    ("=id*10", lambda k: str(int(k) * 10)),
    ("=id*100", lambda k: str(int(k) * 100)),
    ("=id*1000", lambda k: str(int(k) * 1000)),
    ("=id*10000", lambda k: str(int(k) * 10000)),
    ("=10n(n+10)", lambda k: str(10 * int(k) * (int(k) + 10))),
]


def data_lines(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    return [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


def seed_path(csv_path):
    return os.path.join(LOUNGE, (csv_path or "").replace("/", os.sep))


def profile(lines, ncol):
    """col -> 值向量（原始串，去首尾空白）"""
    out = {}
    for ln in lines:
        f = ln.split(",")
        for i in range(min(ncol, len(f))):
            out.setdefault(i, []).append(f[i].strip())
    return out


def main():
    args = [a for a in sys.argv[1:]]
    all_mode = "--all" in args
    names = [a for a in args if not a.startswith("--")]
    if not names:
        names = sorted(json.load(io.open(os.path.join(SCHEMA, f), encoding="utf-8"))["id"]
                       for f in os.listdir(SCHEMA) if f.endswith(".json")) if all_mode else []
    if not names:
        print("用法：python _probe_fill_profile.py <表名...> | --all")
        return

    rep = io.StringIO()
    summary = []
    with psycopg.connect(DSN, autocommit=True) as c:
        cur = c.cursor()
        cur.execute("select file, raw_csv from meta.cfg_manifest")
        man = {}
        for f_, raw in cur.fetchall():
            man[f_] = raw if isinstance(raw, str) else (raw.decode("utf-8", "replace") if raw else "")

        for name in names:
            sp = os.path.join(SCHEMA, name + ".json")
            if not os.path.exists(sp):
                continue
            spec = json.load(io.open(sp, encoding="utf-8"))
            cols = spec.get("columns") or []
            idxs = sorted((x.get("csv_index") if x.get("csv_index") is not None else -1) for x in cols)
            seen = Counter(idxs)
            dup = [k for k, v in seen.items() if v > 1]
            holes = ([i for i in range(min(idxs), max(idxs) + 1) if i not in seen]
                     if idxs and min(idxs) >= 0 else [])

            cur.execute('select count(*) from cfg."%s"' % name)
            n_db = cur.fetchone()[0]
            p = seed_path(spec.get("csv_path"))
            sl = data_lines(open(p, "rb").read().decode("utf-8", "replace")) if os.path.exists(p) else []
            ml = data_lines(man.get(name, ""))

            sk = set(l.split(",")[0].strip() for l in sl)
            mk = set(l.split(",")[0].strip() for l in ml)
            nmax = (max(idxs) + 1) if idxs else 0
            ps, pm = profile(sl, nmax), profile(ml, nmax)
            keys_s = [l.split(",")[0].strip() for l in sl]

            lines_out = []
            cluster = {}
            for i in range(nmax):
                vs = ps.get(i, [])
                if not any(vs):
                    continue
                vm = pm.get(i, [])
                if vs != vm:
                    lines_out.append((i, "★种子/mf 不同"))
                for j in range(i + 1, nmax):
                    if vs and ps.get(j) and vs == ps[j]:
                        cluster.setdefault(min(i, j), []).append(max(i, j))

            formula_cols = {}
            for i in range(nmax):
                vs = ps.get(i, [])
                if not any(vs) or len(set(vs)) == 1:
                    continue
                hits = []
                for nm, f in FORMULAS[1:]:
                    try:
                        if all(vs[k] == f(keys_s[k]) for k in range(len(vs)) if keys_s[k].isdigit()):
                            hits.append(nm)
                    except Exception:
                        pass
                if hits:
                    formula_cols[i] = hits[0]

            filled = [i for i in range(nmax) if any(ps.get(i, []))]
            empty = [i for i in range(nmax) if i not in filled]

            if len(filled) <= 1:
                verdict = "纯键占位"
            elif len(empty) * 2 >= nmax:
                verdict = "内容缺失"
            elif cluster or len(formula_cols) >= 3:
                verdict = "批量公式占位"
            else:
                verdict = "需人工看"

            if not all_mode:
                rep.write("=" * 100 + "\n")
                rep.write("## #%s %s   (%s)   reader=%s\n"
                          % (spec.get("table_id"), name, spec.get("csv_path"), spec.get("asm_reader")))
                rep.write("   schema: 列数=%d  csv_index %s..%s 空洞=%s 重复=%s\n"
                          % (len(cols), min(idxs) if idxs else "-", max(idxs) if idxs else "-",
                             holes[:12], dup[:6]))
                rep.write("   行数：db=%d 种子=%d manifest=%d   键域：%s\n"
                          % (n_db, len(sl), len(ml),
                             "一致(%d)" % len(sk) if sk == mk
                             else "★差 只种子%d 只mf%d" % (len(sk - mk), len(mk - sk))))
                rep.write("   %-6s %-26s %7s %7s %6s  %s\n"
                          % ("csv#", "订案名", "有值", "唯一", "种子/mf", "样例"))
                for i in filled:
                    vs = ps[i]
                    u = sorted(set(vs))
                    samp = u[:5] if len(u) <= 5 else (sorted(u)[:2] + ["..."] + sorted(u)[-2:])
                    rep.write("   %-6d %-26s %7d %7d %6s  %s%s\n"
                              % (i, (next((x.get("name") for x in cols if x.get("csv_index") == i), "") or "")[:26],
                                 sum(1 for v in vs if v), len(u),
                                 "同" if ps.get(i) == pm.get(i) else "★异", samp,
                                 "  " + formula_cols[i] if i in formula_cols else ""))
                rep.write("   全空列 %d 个: %s\n" % (len(empty), empty[:30]))
                rep.write("   列簇: %s\n" % (dict(sorted(cluster.items())) if cluster else "（无）"))
                rep.write("   判定: %s\n\n" % verdict)

            summary.append((name, len(idxs), len(filled), len(empty), len(cluster),
                            len(formula_cols), verdict))

    if all_mode or len(names) > 3:
        rep.write("=" * 100 + "\n")
        rep.write("%-30s %5s %6s %6s %6s %6s  %s\n"
                  % ("表", "列数", "有值列", "全空列", "列簇", "公式列", "判定"))
        for t in summary:
            rep.write("%-30s %5d %6d %6d %6d %6d  %s\n" % t)

    open(OUT, "w", encoding="utf-8").write(rep.getvalue())
    print(rep.getvalue())
    print("wrote", OUT)


if __name__ == "__main__":
    main()

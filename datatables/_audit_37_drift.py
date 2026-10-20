# -*- coding: utf-8 -*-
"""_audit_37_drift.py —— #37 `WEAPON_SETTING` 的「CSV（下发件）↔ 真库」逐列建账。

背景：`#36` 已经收敛到零漂移，但同一批 `item/weapon_settings.csv` 与库从没对过账。
`#37` 是客户端要下载的表（`download_list.csv` 第 37 行），所以两边不一致 = 客户端拿到的
和服务器读到的**不是同一张表**。

判据（口径唯一出处）：`serverv/static/cfg_schema.json` 的 `WEAPON_SETTING.columns[*].csv_index`
= IDA 实测的「CSV 位置 → 库列名」映射（148 列有 csv_index）。逐列逐键比较。

分族：sidecar 族（`names/武器分配明细.csv` col1，9 位） vs 8 位 icon-id 族（其余，`可达武器号域.csv` 标
`现役引用`/`客户端近战`）。两族权威不同（见 `36-36-WEAPON_BATTLE_DETAIL.md` §6.4），必须拆开看。

只报告，不写。
"""
import csv
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
T37 = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
SCH = os.path.join(ROOT, "serverv", "static", "cfg_schema.json")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def norm(k):
    """物品号规范形 —— 与 `store.FormatItemKey` / `gen_weapon_tables_wiki.norm_key` 逐字一致。"""
    k = str(k).strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


def main():
    spec = json.load(open(SCH, encoding="utf-8"))["WEAPON_SETTING"]
    idx2col = {c["csv_index"]: n for n, c in spec["columns"].items()
               if c.get("csv_index") is not None}
    cols = list(spec["columns"])

    side_raw = set()
    for r in csv.reader(open(SIDE, encoding="utf-8-sig", errors="replace")):
        if len(r) > 1 and r[1].strip() and not r[0].startswith("#"):
            side_raw.add(r[1].strip())

    csvrows = {}
    for r in csv.reader(open(T37, encoding="utf-8", errors="replace")):
        if len(r) > 2 and r[0].strip().isdigit():
            csvrows[r[0].strip()] = r

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select %s from cfg."WEAPON_SETTING"'
                    % ",".join('btrim(coalesce("%s",\'\'))' % c for c in cols))
        dbrows = {}
        for row in cur.fetchall():
            d = dict(zip(cols, row))
            dbrows[d["weapon_setting_id"].strip()] = d

    def fam(k):
        return "sidecar" if (k in side_raw or norm(k) in {norm(x) for x in side_raw}) else "icon8"

    print("=== ⓪ 规模 ===")
    print("  CSV（下发件）%d 键 / 库 %d 键 / 共有 %d" % (len(csvrows), len(dbrows), len(set(csvrows) & set(dbrows))))
    oc = sorted(set(csvrows) - set(dbrows))
    od = sorted(set(dbrows) - set(csvrows))
    print("  只在 CSV（库里整行没有）%d：%s" % (len(oc), [(k, fam(k)) for k in oc]))
    print("  只在库（CSV 里整行没有）%d：%s" % (len(od), [(k, fam(k)) for k in od[:20]]))
    print("  CSV 列数 %d / 库列数 %d / 有 csv_index 的列 %d"
          % (max(len(r) for r in csvrows.values()), len(cols), len(idx2col)))

    common = sorted(set(csvrows) & set(dbrows))
    diffs = {}
    for k in common:
        r, d = csvrows[k], dbrows[k]
        for i, col in idx2col.items():
            cv = r[i].strip() if len(r) > i else ""
            if cv != d[col].strip():
                diffs.setdefault(i, []).append((k, fam(k), cv, d[col].strip()))

    print()
    print("=== ① 逐列漂移（只在共有键上比；按族拆）===")
    print("  %-4s %-26s %6s %8s %8s   %s" % ("csv", "库列", "差数", "sidecar", "icon8", "样例"))
    for i in sorted(diffs):
        v = diffs[i]
        ns = sum(1 for x in v if x[1] == "sidecar")
        ni = len(v) - ns
        ex = v[0]
        print("  [%3d] %-26s %6d %8d %8d   %s"
              % (i, idx2col[i], len(v), ns, ni,
                 "%s csv=%r 库=%r" % (ex[0], ex[2], ex[3])))
    nod = sorted(set(idx2col) - set(diffs))
    print()
    print("=== ② 完全一致的列（%d 个）===" % len(nod))
    print("  " + ", ".join("%d:%s" % (i, idx2col[i]) for i in nod))

    # ---- ③ 「库值 == 键本身」自证：占位嫌疑 ----
    print()
    print("=== ③ 库值 == 键本身（占位自证）===")
    for i in sorted(diffs):
        col = idx2col[i]
        same = sum(1 for k in common if dbrows[k][col].strip() in (k, norm(k), k.lstrip("0")))
        filled = sum(1 for k in common if dbrows[k][col].strip())
        if filled and same == filled:
            print("  [%3d] %-26s 库非空 %4d 行，其中 **%d 行 == 键本身** ⇒ 占位" % (i, col, filled, same))
        else:
            print("  [%3d] %-26s 库非空 %4d 行，== 键 %d 行" % (i, col, filled, same))

    # ---- ④ 内容分歧（非占位列）看值对 ----
    print()
    print("=== ④ 值对分布（每列 top 值对）===")
    for i in sorted(diffs):
        col = idx2col[i]
        v = diffs[i]
        pairs = {}
        for k, f, cv, dv in v:
            pairs[(cv, dv, f)] = pairs.get((cv, dv, f), 0) + 1
        top = sorted(pairs.items(), key=lambda x: -x[1])[:4]
        print("  [%3d] %-26s" % (i, col))
        for (cv, dv, f), n in top:
            print("        %-6s csv=%-14r 库=%-14r ×%d" % (f, cv, dv, n))


if __name__ == "__main__":
    main()

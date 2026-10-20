# -*- coding: utf-8 -*-
"""_probe_msma_src.py —— 库 MSMA_WEAPONSET 到底该是什么？

复刻 `load_paired_ms_db.py` 的口径（`fully_paired` / `weapon_rows` / `canon_item`），
在**不改库**的前提下算出"wiki 口径应写的 (dev_id, item_id) 全表"，再与真库对账。

只报告，不写。
"""
import collections
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UNITS = os.path.join(ROOT, "gow_wiki", "data", "units.json")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def weapon_rows(u):
    out = []
    for g in u.get("weapons") or []:
        for r in g.get("rows") or []:
            name = (r.get("名称") or "").strip()
            if name and name != "~":
                out.append(r)
    return out


def fully_paired(u):
    rs = weapon_rows(u)
    did = (u.get("dev_id") or "").strip()
    if not rs or not (len(did) == 7 and did.isdigit()):
        return False
    return all(len(str(r.get("icon_id") or "")) == 8 and str(r["icon_id"]).isdigit() for r in rs)


def canon_item(icon_id):
    n = int(icon_id)
    if 0 < n < 100_000_000:
        return "%08d" % n
    return str(n)


def lens(vals):
    d = {}
    for v in vals:
        d[len(v)] = d.get(len(v), 0) + 1
    return dict(sorted(d.items()))


def main():
    units = json.load(open(UNITS, encoding="utf-8"))
    print("units.json 机体 %d 台" % len(units))
    chosen = [u for u in units if fully_paired(u)]
    print("fully_paired（全 8 位 icon_id + 7 位 dev_id）= %d 台" % len(chosen))

    wiki = collections.defaultdict(list)
    for u in chosen:
        did = u["dev_id"].strip()
        seen = set()
        for r in weapon_rows(u):
            iid = canon_item(r["icon_id"])
            if iid in seen:
                continue
            seen.add(iid)
            wiki[did].append(iid)

    wpairs = {(d, i) for d, v in wiki.items() for i in v}
    wids = {i for v in wiki.values() for i in v}
    print("wiki 口径：组 %d ／ 行 %d ／ 去重武器ID %d（长度 %s）"
          % (len(wiki), len(wpairs), len(wids), lens(wids)))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select btrim(weapon_group_id), btrim(weapon_item_id) from cfg."MSMA_WEAPONSET"')
        rows = cur.fetchall()
        db = collections.defaultdict(list)
        for g, i in rows:
            db[g].append(i)
        dpairs = {(g, i) for g, i in rows}
        dids = {i for _, i in rows}
        print("真库     ：组 %d ／ 行 %d ／ 去重武器ID %d（长度 %s）"
              % (len(db), len(dpairs), len(dids), lens(dids)))

        print()
        print("=== (组, 武器) 对账 ===")
        print("  ∩             %d" % len(wpairs & dpairs))
        print("  wiki 有库没有 %d" % len(wpairs - dpairs))
        print("  库有 wiki 没有 %d" % len(dpairs - wpairs))
        print("  ⇒ wiki 口径覆盖率 %.1f%%" % (100.0 * len(wpairs & dpairs) / max(1, len(wpairs))))
        print("  库独有样例:", sorted(dpairs - wpairs)[:8])

        print()
        print("=== 组口径 ===")
        print("  组 ID：wiki∩库 %d ／ 只在 wiki %d ／ 只在库 %d"
              % (len(set(wiki) & set(db)), len(set(wiki) - set(db)), len(set(db) - set(wiki))))
        print("  只在库的组样例:", sorted(set(db) - set(wiki))[:10])

        print()
        print("=== 库独有行的号形（判断是不是历史脚本残留）===")
        only = sorted(dpairs - wpairs)
        print("  前 10:", only[:10])
        print("  ⇒ 其中 9 位 %d 个 / 8 位 %d 个"
              % (sum(1 for _, i in only if len(i) == 9), sum(1 for _, i in only if len(i) == 8)))

        # 与 #37 的关系
        cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
        d37 = {r[0] for r in cur.fetchall()}
        cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_SETTING'")
        raw = cur.fetchone()[0]
        raw = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
        m37 = {l.split(",")[0].strip() for l in raw.replace("\r\n", "\n").split("\n")
               if l.strip() and not l.startswith("#")}
        print()
        print("=== 引用是否都有 #37 行 ===")
        print("  wiki 口径引用、真库 #37 没有的 = %d" % len(wids - d37))
        print("  wiki 口径引用、manifest #37 有的 = %d / %d" % (len(wids & m37), len(wids)))
        print("  真库引用、真库 #37 没有的      = %d" % len(dids - d37))
        print("  ⇒ 差集样例:", sorted(wids - d37)[:10])


if __name__ == "__main__":
    main()

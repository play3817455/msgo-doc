# -*- coding: utf-8 -*-
"""P0 复核 v6：**只用 raw 字符串**（不做任何补零）看号形与交叠。

只报告，不写。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def lens(vals):
    d = {}
    for v in vals:
        d[len(v)] = d.get(len(v), 0) + 1
    return dict(sorted(d.items()))


def show(tag, vals):
    print("  %-42s n=%-5d 长度分布=%s" % (tag, len(vals), lens(vals)))
    for L in sorted(lens(vals)):
        s = sorted(v for v in vals if len(v) == L)[:5]
        print("      len=%d 样例 %s" % (L, s))


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()

        cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_SETTING'")
        raw = cur.fetchone()[0]
        raw = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
        mf = {l.split(",")[0].strip() for l in raw.replace("\r\n", "\n").split("\n")
              if l.strip() and not l.startswith("#")}

        cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
        db = {r[0] for r in cur.fetchall()}

        cur.execute('select btrim(item_id::text) from cfg."ITEM"')
        it = {r[0] for r in cur.fetchall()}

        cur.execute('select btrim(weapon_item_id::text) from cfg."MSMA_WEAPONSET"')
        mw = {r[0] for r in cur.fetchall()}

        print("=== raw 号形 ===")
        show("manifest #37 键", mf)
        show("真库 #37 键", db)
        show("ITEM item_id", it)
        show("MSMA_WEAPONSET weapon_item_id", mw)

        print()
        print("=== raw 交叠 ===")
        only_mf = mf - db
        print("  manifest-only: %d" % len(only_mf))
        show("  ↳ manifest-only", only_mf)
        print("  manifest-only ∩ ITEM            = %d" % len(only_mf & it))
        print("  manifest-only ∩ MSMA_WEAPONSET  = %d" % len(only_mf & mw))
        print("  db-only: %d" % len(db - mf))
        show("  ↳ db-only", db - mf)

        # 关键：只在 manifest 的键，是不是「8 位但首位是 0」这种？
        z8 = {v for v in only_mf if len(v) == 8 and v.startswith("0")}
        print()
        print("  manifest-only 里『8 位且以 0 开头』= %d（这类在 ITEM 里 %d，被 MSMA 引用 %d）"
              % (len(z8), len(z8 & it), len(z8 & mw)))

        # 这些键的 raw 前缀（前两位）分布，看是不是集中在少数几块
        pref = {}
        for v in only_mf:
            pref[v[:2]] = pref.get(v[:2], 0) + 1
        print("  manifest-only 前两位分布 top20:",
              sorted(pref.items(), key=lambda x: -x[1])[:20])

        print()
        print("=== 真库保留的键，号形对照 ===")
        print("  真库 ∩ MSMA_WEAPONSET = %d / %d" % (len(db & mw), len(db)))
        print("  真库 ∩ ITEM           = %d / %d" % (len(db & it), len(db)))
        print("  真库不在 MSMA 引用里的 = %d" % len(db - mw))


if __name__ == "__main__":
    main()

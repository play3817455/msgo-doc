# -*- coding: utf-8 -*-
"""_probe_dmg_attr_verdict.py —— 判定 col30 `damage_attribute` 到底哪边对（只读）

`#37` col30 有 **386 行**库≠种子，而且**两个方向都有**
（`NONE→GUN_RAPID` 与 `GUN_RAPID→NONE` 并存）⇒ 不能用"种子更全"一句话糊过去。

找**外部判据**：`#36` 里带 `RAPIDDELAY` 行的武器就是"连发武器"，
其 col30 应为 `GUN_RAPID`；没有 `RAPIDDELAY` 的应为 `GUN_SINGLE`/`NONE`
（`WRESTLE` = 格斗、`SHIELD` = 护盾，另算）。

对 386 行里每一行算：库值 / 种子值 各自是否符合该规则。
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
COL30 = 30


def main():
    seed = {}
    with open(SEED, encoding="utf-8", newline="") as fh:
        for l in fh.read().split("\r\n"):
            if not l.strip() or l.startswith("#"):
                continue
            p = l.split(",")
            while len(p) < 34:
                p.append("")
            seed[p[0].strip()] = p

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT btrim(weapon_id_key), btrim(attr_name) FROM cfg."WEAPON_BATTLE_DETAIL" """)
        attrs = collections.defaultdict(set)
        for k, a in cur.fetchall():
            attrs[k].add(a)
        cur.execute('SELECT btrim(weapon_setting_id), btrim(damage_attribute),'
                    ' btrim(weapon_category) FROM cfg."WEAPON_SETTING"')
        db = {k: (d, c) for k, d, c in cur.fetchall()}

    diff = [(k, db[k][0], seed[k][COL30].strip()) for k in db
            if k in seed and db[k][0] != seed[k][COL30].strip()]
    print("col30 库≠种子：%d 行" % len(diff))
    print("转移矩阵（库 → 种子）：")
    mt = collections.Counter((a, b) for _, a, b in diff)
    for (a, b), n in mt.most_common():
        print("  %-12s → %-12s %d" % (a, b, n))

    def rule(k, v):
        """外部判据：有 RAPIDDELAY ⇒ 应 GUN_RAPID；无 ⇒ 不应 GUN_RAPID。"""
        rap = "RAPIDDELAY" in attrs.get(k, set())
        if v == "GUN_RAPID":
            return rap
        if v in ("GUN_SINGLE", "NONE"):
            return not rap
        return None      # WRESTLE / SHIELD / 空 不参与判定

    ok_db = ok_seed = judged = 0
    only_db = []
    only_seed = []
    for k, a, b in diff:
        ra, rb = rule(k, a), rule(k, b)
        if ra is None and rb is None:
            continue
        judged += 1
        if ra is None or rb is None:
            # 一边可判、一边不可判：可判的那边若成立就给它加分
            if ra:
                ok_db += 1
                only_db.append((k, a, b))
            elif rb:
                ok_seed += 1
                only_seed.append((k, a, b))
            continue
        ok_db += 1 if ra else 0
        ok_seed += 1 if rb else 0

    print()
    print("=== 用 `#36` 的 RAPIDDELAY 做外部判据（%d 行可判）===" % judged)
    print("  库值符合：%d" % ok_db)
    print("  种子值符合：%d" % ok_seed)
    if judged:
        print("  ⇒ 结论：%s"
              % ("库对" if ok_db > ok_seed else
                 "种子对" if ok_seed > ok_db else "打平，无法判定"))

    print()
    print("=== 库对而种子错的样本（最多 8）===")
    for x in only_db[:8]:
        print("   %s  库=%s 种子=%s" % x)
    print("=== 种子对而库错的样本（最多 8）===")
    for x in only_seed[:8]:
        print("   %s  库=%s 种子=%s" % x)
    print()
    print("=== 打平/不可判的样本（最多 8）===")
    rest = [d for d in diff if rule(d[0], d[1]) is None and rule(d[0], d[2]) is None]
    for x in rest[:8]:
        print("   %s  库=%s 种子=%s  类别=%s #36=%s"
              % (x[0], x[1], x[2], db[x[0]][1], sorted(attrs.get(x[0], set()))))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""_probe_seed_vs37.py —— 种子 CSV 的 1625 把武器，在 #37/#36/ITEM 里各有多少？

若 562 个"库外种子武器"在 #37 里没有行，全量重载反而会**新增**断引用。
只报告，不写。
"""
import glob
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def main():
    print("=== 文件时间线（msma_weapon_set.csv 世代）===")
    for p in sorted(glob.glob(os.path.join(os.path.dirname(SEED), "msma_weapon_set.csv*"))):
        print("   %s  %s  %d 字节"
              % (time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p))),
                 os.path.basename(p), os.path.getsize(p)))
    print()

    seed_pairs, seed_ids, seed_groups = set(), set(), set()
    with open(SEED, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            c = line.split(",")
            if len(c) < 3:
                continue
            seed_pairs.add((c[0].strip(), c[2].strip()))
            seed_ids.add(c[2].strip())
            seed_groups.add(c[0].strip())

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
        d37 = {r[0] for r in cur.fetchall()}
        cur.execute('select distinct btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
        d36 = {r[0] for r in cur.fetchall()}
        cur.execute('select btrim(item_id) from cfg."ITEM"')
        item = {r[0] for r in cur.fetchall()}
        cur.execute('select btrim(weapon_group_id), btrim(weapon_item_id) from cfg."MSMA_WEAPONSET"')
        mw = {(g, i) for g, i in cur.fetchall()}

        new = seed_ids - {i for _, i in mw}
        print("种子武器 %d ／ 已在库 MSMA_WEAPONSET %d ／ 新增 %d"
              % (len(seed_ids), len({i for _, i in mw}), len(new)))
        miss37 = new - d37
        miss36 = new - d36
        missitem = new - item
        print("  新增武器里：#37 有行 %d ／ **#37 缺行 %d**" % (len(new) - len(miss37), len(miss37)))
        print("              #36 有行 %d ／ #36 缺行 %d" % (len(new) - len(miss36), len(miss36)))
        print("              ITEM 有行 %d ／ ITEM 缺行 %d" % (len(new) - len(missitem), len(missitem)))
        print("  #37 缺行样例:", sorted(miss37)[:10])
        print()

        # 逐组：全量重载后，有多少组会带"无 #37 行"的武器
        bad_groups = {g for g, i in seed_pairs if i in miss37}
        print("  含缺 #37 武器的组：%d / %d" % (len(bad_groups), len(seed_groups)))
        print("  样例:", sorted(bad_groups)[:10])
        print()
        print("=== 对照：现在库里 9 位族的组，是否 100% 干净 ===")
        cur_db9 = {(g, i) for g, i in mw if len(i) == 9}
        bad9 = {g for g, i in cur_db9 if i not in d37}
        print("  现库 9 位族组 %d ／ 含缺 #37 的组 %d" % (len({g for g, _ in cur_db9}), len(bad9)))


if __name__ == "__main__":
    main()

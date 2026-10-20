# -*- coding: utf-8 -*-
"""_probe_msma_cover.py —— 8 位族 / 9 位族 / 种子 CSV 的机体覆盖关系。

决定"删 8 位族换成种子 9 位族"是否无损：235 个 8 位族机体在种子 CSV 里有没有？
只报告，不写。
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def main():
    seed_pairs = set()
    seed_groups = set()
    with open(SEED, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            c = line.split(",")
            if len(c) < 3:
                continue
            seed_pairs.add((c[0].strip(), c[2].strip()))
            seed_groups.add(c[0].strip())

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select btrim(weapon_group_id), btrim(weapon_item_id) from cfg."MSMA_WEAPONSET"')
        rows = [(g, i) for g, i in cur.fetchall()]
        g8 = {g for g, i in rows if len(i) == 8}
        g9 = {g for g, i in rows if len(i) == 9}
        d8 = {(g, i) for g, i in rows if len(i) == 8}
        d9 = {(g, i) for g, i in rows if len(i) == 9}

        cur.execute('select distinct btrim(msma_id) from cfg."CHARA_PARAM"')
        units = {r[0] for r in cur.fetchall()}

        print("=== 机体覆盖 ===")
        print("  cfg.CHARA_PARAM 机体        %d" % len(units))
        print("  种子 CSV 有武器组的机体    %d" % len(seed_groups))
        print("  真库 MSMA_WEAPONSET 组     %d  (纯8位 %d / 纯9位 %d / 混装 %d)"
              % (len(g8 | g9), len(g8 - g9), len(g9 - g8), len(g8 & g9)))
        print("  组 ⊆ MSMA_PARAM ?          %s"
              % ("否，库里多出 " + str(sorted((g8 | g9) - units)[:6]) if (g8 | g9) - units else "是"))

        print()
        print("=== ★关键：235 个 8 位族机体，种子 CSV 有没有 ===")
        print("  8 位族机体 %d ／ 其中在种子 CSV 里 %d ／ 不在 %d"
              % (len(g8), len(g8 & seed_groups), len(g8 - seed_groups)))
        print("  不在种子的样例:", sorted(g8 - seed_groups)[:8])
        print("  种子 ∩ 真库9位组 %d ／ 种子独有组 %d"
              % (len(seed_groups & g9), len(seed_groups - g9)))
        print("  种子独有组样例:", sorted(seed_groups - g9)[:8])

        print()
        print("=== 若按种子 CSV 全量重载 MSMA_WEAPONSET 会怎样 ===")
        print("  行 %d -> %d ／ 组 %d -> %d"
              % (len(rows), len(seed_pairs), len(g8 | g9), len(seed_groups)))
        print("  8 位族机体被种子接管 %d ／ 失去覆盖 %d 个"
              % (len(g8 & seed_groups), len(g8 - seed_groups)))
        print("  新获得覆盖的机体 %d" % len(seed_groups - (g8 | g9)))
        print("  两族都在种子里的组（8 位族被 9 位族替换）样例:",
              sorted(g8 & seed_groups)[:6])

        print()
        print("=== 8 位族机体在种子里的可用武器数 ===")
        cnt = collections.Counter()
        for g, i in seed_pairs:
            cnt[g] += 1
        only8 = sorted(g8 - seed_groups)
        print("  8位族独有 %d 个机体在种子里的槽位: %s"
              % (len(only8), sorted({cnt[g] for g in only8})))
        print("  即这些机体**没有**任何 9 位可用武器 ⇒ 删 8 位族会变成空组")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""_probe_msma_closure.py —— MSMA_WEAPONSET 收敛收口的一次性复核（只读）

打印 §12 需要的全部硬数字：
  ① 种子 CSV 与真库逐行对账（应为 0 差）
  ② 回滚件（收敛前）的 8 位污染规模 + 断引用规模
  ③ 当前库的断引用数（应为 0）
  ④ 收敛中失去武器组的机体（口径：回滚件里该组**只有** 8 位武器）
  ⑤ manifest 里 #1 的 row_count / sha 与真库是否一致
"""
import collections
import csv
import hashlib
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
ROLLBACK = os.path.join(HERE, "_rollback", "20261005_120824_MSMA_WEAPONSET_full.csv")
BRIDGE = os.path.join(HERE, "names", "机体-wiki武器页桥.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def seed_pairs():
    pairs = []
    with open(SEED, encoding="utf-8-sig", newline="") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cells = line.rstrip("\r\n").split(",")
            if cells and cells[-1] == "":
                cells.pop()
            if len(cells) < 3:
                continue
            pairs.append((cells[0].strip(), cells[2].strip()))
    return pairs


def rollback_pairs():
    pairs = []
    with open(ROLLBACK, encoding="utf-8-sig", newline="") as fh:
        for row in csv.reader(fh):
            if not row or row[0].startswith("#"):
                continue
            if row[0].strip() in ("_row_id", "id", ""):
                continue
            pairs.append((row[1].strip(), row[3].strip()))
    return pairs


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT btrim(weapon_group_id), btrim(weapon_item_id) FROM cfg."MSMA_WEAPONSET"')
        live = [(g, i) for g, i in cur.fetchall()]
        cur.execute('SELECT btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
        d37 = {r[0] for r in cur.fetchall()}
        cur.execute("""SELECT row_count, sha256 FROM meta.cfg_manifest
                        WHERE file = 'MSMA_WEAPONSET'""")
        mf = cur.fetchone()

    seed = seed_pairs()
    print("=== ① 种子 vs 真库 ===")
    print("  种子       行 %d ／ 去重对 %d ／ 去重组 %d" % (len(seed), len(set(seed)), len({g for g, _ in seed})))
    print("  真库       行 %d ／ 去重对 %d ／ 去重组 %d" % (len(live), len(set(live)), len({g for g, _ in live})))
    print("  种子有·库无 %d ／ 库有·种子无 %d" % (len(set(seed) - set(live)), len(set(live) - set(seed))))
    bad = [i for _, i in seed if len(i) != 9]
    print("  种子非 9 位 col2：%d" % len(bad))

    print()
    print("=== ② 回滚件（收敛前）===")
    rb = rollback_pairs()
    d8 = [i for _, i in rb if len(i) == 8]
    d9 = [i for _, i in rb if len(i) == 9]
    print("  行 %d（与库 2244 对照）" % len(rb))
    print("  8 位武器号行 %d ／ 去重 8 位号 %d" % (len(d8), len(set(d8))))
    print("  9 位武器号行 %d ／ 去重 9 位号 %d" % (len(d9), len(set(d9))))
    print("  其中 8 位号在 #37 有行的：%d ／ 无行的（=断引用）：%d"
          % (sum(1 for i in d8 if i in d37), sum(1 for i in d8 if i not in d37)))

    print()
    print("=== ③ 当前库断引用 ===")
    dang = [i for _, i in live if i not in d37]
    print("  MSMA_WEAPONSET 引用不到 #37 的行：%d" % len(dang))

    print()
    print("=== ④ 失去武器组的机体 ===")
    rb_groups = collections.defaultdict(list)
    for g, i in rb:
        rb_groups[g].append(i)
    live_groups = {g for g, _ in live}
    lost = sorted(g for g in rb_groups if g not in live_groups)
    print("  回滚件有组、现在无组的组 ID：%d" % len(lost))
    n8 = sum(1 for g in lost if all(len(i) == 8 for i in rb_groups[g]))
    print("  其中「该组全部是 8 位武器」的：%d" % n8)
    tot = sum(len(rb_groups[g]) for g in lost)
    dgt = sum(1 for g in lost for i in rb_groups[g] if i not in d37)
    print("  这些组在收敛前共 %d 行武器，其中断引用 %d（%.0f%%）"
          % (tot, dgt, 100.0 * dgt / max(1, tot)))

    with open(BRIDGE, encoding="utf-8-sig") as fh:
        br = [r for r in csv.reader(fh) if r and not r[0].lstrip("\ufeff").startswith("#")]
    verd = collections.Counter((r[8].strip() if len(r) > 8 else "") for r in br)
    print("  桥表裁定档：%s（数据行 %d）" % (dict(verd), len(br)))
    vmap = {r[0].strip(): (r[8].strip() if len(r) > 8 else "") for r in br}
    lv = collections.Counter(vmap.get(g, "(桥表无此行)") for g in lost)
    print("  失去组的机体在桥表里：%s" % dict(lv))

    print()
    print("=== ⑤ manifest #1 ===")
    print("  meta.cfg_manifest(file=MSMA_WEAPONSET): row_count=%s sha256=%s" % (mf[0], mf[1][:16] + "…"))
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT count(*) FROM cfg."MSMA_WEAPONSET"')
        n = cur.fetchone()[0]
    print("  真库行数：%d ⇒ row_count 一致：%s" % (n, mf[0] == n))


if __name__ == "__main__":
    main()

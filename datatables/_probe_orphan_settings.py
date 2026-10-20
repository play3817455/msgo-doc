# -*- coding: utf-8 -*-
"""_probe_orphan_settings.py —— #37 里非 9 位的键到底是不是孤儿（只读）

收敛后 #1 MSMA_WEAPONSET 全 1625 键都是 9 位。但 #37 自己还留着
17 个 7 位 + 3 个 8 位键。本脚本逐键查：
  · #1 有没有武器组指向它
  · #36 的 weapon_id_key 有没有属性行
  · #78 ITEM 有没有物品行
⇒ 判定"可删 / 不可删（有 ITEM 行）"。
"""
import collections
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
        keys = sorted({r[0] for r in cur.fetchall()})
        cur.execute('SELECT btrim(weapon_item_id) FROM cfg."MSMA_WEAPONSET"')
        ms = {r[0] for r in cur.fetchall()}
        cur.execute('SELECT DISTINCT btrim(weapon_id_key) FROM cfg."WEAPON_BATTLE_DETAIL"')
        w36 = {r[0] for r in cur.fetchall()}
        cur.execute('SELECT btrim(item_id) FROM cfg."ITEM"')
        it = {r[0] for r in cur.fetchall()}

    odd = [k for k in keys if len(k) != 9]
    print("#37 键 %d 个，非 9 位 %d 个" % (len(keys), len(odd)))
    print()
    print("%-12s %-4s %-10s %-10s %-10s %s" % ("key", "位", "被#1引用", "有#36行", "有ITEM行", "判定"))
    stat = collections.Counter()
    for k in odd:
        a = k in ms
        b = k in w36
        c = k in it
        if c:
            verdict = "保留（有 ITEM 行）"
        elif a or b:
            verdict = "保留（仍被引用）"
        else:
            verdict = "★孤儿，可删"
        stat[verdict] += 1
        print("%-12s %-4d %-10s %-10s %-10s %s"
              % (k, len(k), "是" if a else "—", "是" if b else "—", "是" if c else "—", verdict))
    print()
    for k, v in stat.most_common():
        print("  %-22s %d" % (k, v))


if __name__ == "__main__":
    main()

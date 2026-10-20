# -*- coding: utf-8 -*-
"""_probe_w36_seed.py —— #36 种子里的属性族是否齐（只读）

`#37` 列注释列出 11 个属性族（POWER RANGE HIGH_LOCKON STABILITY RAPIDDELAY
COOLTIME RELOAD LOCKON_CAM RECOIL SWITCHTIME SHIELD），但真库 #36 只有 8 种。
查种子 `item/weapon_battle_detail.csv` 到底有几种 ⇒ 判定"源缺口 vs 库漂移"。
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_battle_detail.csv")

want = {"POWER", "RANGE", "HIGH_LOCKON", "STABILITY", "RAPIDDELAY", "COOLTIME",
        "RELOAD", "LOCKON_CAM", "RECOIL", "SWITCHTIME", "SHIELD"}


def main():
    print("种子 %s  存在=%s" % (os.path.relpath(SEED, ROOT), os.path.exists(SEED)))
    if not os.path.exists(SEED):
        return
    with open(SEED, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    lines = [l for l in raw.split("\r\n") if l.strip() and not l.startswith("#")]
    print("  数据行 %d" % len(lines))
    c = collections.Counter(l.split(",")[0].strip() for l in lines)
    print("  属性族 %d 种：" % len(c))
    for k, v in c.most_common():
        print("    %-14s %d" % (k, v))
    print()
    print("  客户端要的 11 族里，种子里缺：%s" % sorted(want - set(c)))
    for l in lines[:2]:
        print("  %r" % l[:120])


if __name__ == "__main__":
    main()

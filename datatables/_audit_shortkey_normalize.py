# -*- coding: utf-8 -*-
"""判死之二：短号是不是「同一 ID 的另一种写法」（丢前导零 / 少个 '2' 前缀 / 少 4 位 sub）。

对每条归一化规则算命中率。若某规则让短号几乎全中 9 位 sidecar 集，那修法就是**归一化键**
（改写行键），而不是删行 —— 与「逐条修」同解。
"""
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
SIDE = os.path.join(ROOT, "datatables", "names", "武器分配明细.csv")
CLIENT = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings")


def rd(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


sid = [r for r in rd(SIDE) if r and r[0].strip().isdigit()]
WEAPON = {r[1].strip() for r in sid}
MELEE = {r[0].strip().lstrip("\ufeff") for r in rd(os.path.join(CLIENT, "weapon_wrestle.csv"))
         if r and r[0].strip().lstrip("\ufeff").isdigit()}
LEGIT = WEAPON | MELEE

RULES = {
    "2+pad8(k)": lambda k: "2" + k.zfill(8),
    "2+k(原样)": lambda k: "2" + k,
    "2+pad7(k)": lambda k: "2" + k.zfill(7),
    "pad9(k)": lambda k: k.zfill(9),
    "pad8(k)": lambda k: k.zfill(8),
    "k+zfill(8-k)[:4]": lambda k: k + k.zfill(8)[: 8 - len(k)] if len(k) < 8 else k,
}

for fn, kc in (("weapon_battle_detail.csv", 1), ("weapon_settings.csv", 0), ("item.csv", 0)):
    rows = [r for r in rd(os.path.join(DF, fn)) if not r[0].lstrip("\ufeff").startswith("#")]
    keys = {r[kc].strip() for r in rows if len(r) > kc and r[kc].strip().isdigit()}
    short = sorted(k for k in keys if k not in LEGIT and k.lstrip("0") not in LEGIT)
    print("=== %s：%d 个短号 ===" % (fn, len(short)))
    for name, f in RULES.items():
        hit = sum(1 for k in short if f(k) in WEAPON or f(k) in LEGIT)
        if hit:
            print("   %-22s 命中 %4d/%4d (%.0f%%)  例 %s -> %s"
                  % (name, hit, len(short), 100 * hit / max(1, len(short)),
                     short[:2], [f(k) for k in short[:2]]))
    # 反向：短号 = 9 位号去掉若干位？
    for cut in (1, 2):
        for k in short[:0]:
            pass
    print()

# 直接看几个具体样本：1010401 / 10101 / 1010101 在 sidecar 里有没有「近亲」
print("--- 抽样查近亲（sidecar 里以该串结尾/包含的 9 位号）---")
allw = sorted(WEAPON)
for probe in ("1010401", "10101", "1010101", "10102", "10201", "1012201"):
    kin = [w for w in allw if w.endswith(probe) or probe in w]
    print("  %-9s 近亲 %2d: %s" % (probe, len(kin), kin[:6]))

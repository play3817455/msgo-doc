# -*- coding: utf-8 -*-
"""判死： #36/#37/#78 里的「7 位短号」到底是不是 sidecar col0（#練度ID）被写错了列。

若 {短号键} ⊂ {練度ID 全集}，则那些行根本不是武器行 —— 是旧抓取把 col0 当武器号写入，
一行都不是「某个武器的数据」，全族可判死（不是「值写坏」，是「身份错」）。
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


sid = [r for r in rd(SIDE) if r and r[0].lstrip("\ufeff").startswith("#") is False
       and r[0].strip().isdigit()]
RENDO = {r[0].strip() for r in sid}                       # col0 = 練度ID（7 位）
WEAPON = {r[1].strip() for r in sid}                      # col1 = 武器ID（9 位）
MELEE = {r[0].strip().lstrip("\ufeff") for r in rd(os.path.join(CLIENT, "weapon_wrestle.csv"))
         if r and r[0].strip().lstrip("\ufeff").isdigit()}
LEGIT = WEAPON | MELEE
print("sidecar 行 %d：練度ID(7位) %d 个、武器ID(9位) %d 个；客户端近战短号 %d 个"
      % (len(sid), len(RENDO), len(WEAPON), len(MELEE)))
print("練度ID 样例:", sorted(RENDO)[:6])
print("武器ID 样例:", sorted(WEAPON)[:6])
print()

for fn, kc, note in (("weapon_battle_detail.csv", 1, "col1=武器号"),
                     ("weapon_settings.csv", 0, "col0=武器号"),
                     ("item.csv", 0, "col0=ID")):
    rows = [r for r in rd(os.path.join(DF, fn)) if not r[0].lstrip("\ufeff").startswith("#")]
    keys = {r[kc].strip() for r in rows if len(r) > kc and r[kc].strip().isdigit()}
    if fn == "item.csv":
        keys = {k for k in keys}
    short = {k for k in keys if k not in LEGIT and k.lstrip("0") not in LEGIT}
    in_rendo = {k for k in short if k in RENDO or k.lstrip("0") in RENDO}
    not_rendo = short - in_rendo
    print("%-28s (%s) 唯一键 %5d | 非合法 %4d | 属于練度ID列 %4d (%.0f%%) | 仍不明 %3d"
          % (fn, note, len(keys), len(short), len(in_rendo),
             100 * len(in_rendo) / max(1, len(short)), len(not_rendo)))
    if not_rendo:
        print("      仍不明例（前 20）:", sorted(not_rendo)[:20])

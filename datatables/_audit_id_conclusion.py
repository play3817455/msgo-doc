# -*- coding: utf-8 -*-
"""_audit_id_conclusion.py —— 取证收口：钉死「哪一族武器号是客户端真域」，算清要清多少行。

证据链（全部可核，客户端本地文件为证）：
  ① `unpackdat/settings/weapon_visual_customize.csv` 表头 col0 = `#武器ID`，取值 9 位
     （`214801312,1,,,,,,ギラ・ドーガ(袖付き)の武器`）
  ② `unpackdat/settings/msma_mesh_customize.csv` / `msma_visual_customize.csv` col1 = 9 位武器号
  ③ `unpackdat/settings/weapon_wrestle.csv`（近接格闘武器表）col0 = アイテムID，**全表只有 8 行**
     （7×7 位 + 1×8 位）⇒ 短号里唯一的真域只有这 8 个通用近战武器
  ④ 6 把报警号在①②③ 里**一个都不出现**
"""
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings")
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
SIDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names", "武器分配明细.csv")


def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


# ① 客户端三个定制表的武器号
client9, client_short = set(), set()
for fn, col in (("weapon_visual_customize.csv", 0), ("msma_mesh_customize.csv", 1),
                ("msma_visual_customize.csv", 1), ("weapon_wrestle.csv", 0)):
    p = os.path.join(CLIENT, fn)
    n = 0
    for r in rd(p):
        if r[0].lstrip("\ufeff").startswith("#") or len(r) <= col:
            continue
        v = r[col].strip().lstrip("\ufeff")
        if v.isdigit():
            (client9 if len(v) >= 9 else client_short).add(v)
            n += 1
    print("客户端 %-30s col%d 取到 %d 行" % (fn, col, n))
print("客户端武器号：9 位 %d 个；短号 %d 个 → %s"
      % (len(client9), len(client_short), sorted(client_short)))

# ② 客户端 9 位号 ∩ wiki sidecar（独立交叉验证）
side = {r[1].strip() for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
inter = sorted(client9 & side)
print()
print("客户端 9 位号 ∩ sidecar 真武器 = %d 个（例：%s）" % (len(inter), inter[:6]))

# ③ 三个合法集合
legit = set(side) | client_short
print()
print("合法武器号集合 = sidecar 9 位 %d + 客户端近战短号 %d = %d"
      % (len(side), len(client_short), len(legit)))

# ④ 库里现状与待清量
cur = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo").cursor()
for tag, tbl, col in (("#36", '"WEAPON_BATTLE_DETAIL"', "weapon_id_key"),
                      ("#37", '"WEAPON_SETTING"', "weapon_setting_id"),
                      ("#78", '"ITEM"', "item_id")):
    extra = '' if tag != "#78" else " and btrim(item_type)='WEAPON'"
    cur.execute('select btrim(%s) from cfg.%s where btrim(%s) ~ \'^[0-9]+$\'%s'
                % (col, tbl, col, extra))
    raw = [k for (k,) in cur.fetchall()]
    keep = [k for k in raw if k in legit or k.lstrip("0") in legit]
    drop = [k for k in raw if k not in legit and k.lstrip("0") not in legit]
    print("%s 键 %d：合法 %d、**待清 %d**" % (tag, len(raw), len(keep), len(drop)))

# ⑤ 近战 8 号在 #36 里的 POWER
print()
melee = sorted(client_short, key=lambda x: (len(x), x))
cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' and btrim(weapon_id_key) = any(%s)''',
            (melee + ["%08d" % int(m) for m in melee],))
print("近战短号的 #36 POWER：%s" % dict(cur.fetchall()))

# ⑥ 6 把报警号合法性
print()
print("6 把报警号是否属于合法集合：")
for a in ("2600151", "2012401", "2240601", "12520101", "2210351", "2600101"):
    print("   %-10s in 合法集合 = %s" % (a, a in legit))

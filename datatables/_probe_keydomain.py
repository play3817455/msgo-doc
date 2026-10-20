# -*- coding: utf-8 -*-
"""物品/武器键域体检：ITEM 种子 vs 库 vs 号域文件 vs 武器族各表 -> datatables/_out_keydomain.txt"""
import io
import os
from collections import Counter

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
OUT = os.path.join(HERE, "_out_keydomain.txt")


def norm(s):
    return s.lstrip("0") or "0"


def csv_keys(path, col=0):
    with open(path, "rb") as f:
        raw = f.read()
    out = []
    for ln in raw.decode("utf-8-sig", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        p = ln.split(",")
        out.append(p[col].strip())
    return out


rep = io.StringIO()

# 号域文件
dom = csv_keys(os.path.join(HERE, "names", "可达武器号域.csv"))
rep.write("== 可达武器号域.csv ==\n  行 %d 去重 %d 长度分布 %s\n"
          % (len(dom), len(set(dom)), dict(sorted(Counter(len(k) for k in set(dom)).items()))))
rep.write("  样例 %s\n\n" % sorted(set(dom))[:8])

# 物品ID全集
p = os.path.join(HERE, "names", "物品ID全集.csv")
if os.path.exists(p):
    it = csv_keys(p)
    rep.write("== 物品ID全集.csv ==\n  行 %d 去重 %d 长度分布 %s\n"
              % (len(it), len(set(it)), dict(sorted(Counter(len(k) for k in set(it)).items()))))
    rep.write("  样例 %s\n\n" % sorted(set(it))[:8])

# 种子 item.csv
seed = csv_keys(os.path.join(LOUNGE, "item", "item.csv"))
rep.write("== 种子 item/item.csv ==\n  行 %d 去重 %d 长度分布 %s\n\n"
          % (len(seed), len(set(seed)), dict(sorted(Counter(len(k) for k in set(seed)).items()))))

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    fam = [("ITEM", "item_id"), ("WEAPON_SETTING", "weapon_setting_id"),
           ("WEAPON_BATTLE_DETAIL", "weapon_id_key"), ("MSMA_BATTLE_DETAIL", "entry_key"),
           ("MSMA_WEAPONSET", None), ("MSMA_WEAPON_EQUIPCOMB", None),
           ("ITEM_PART", None), ("ITEM_USE", None), ("ITEM_TOKEN", None),
           ("MSMA_COLORSET", None), ("BUILDUP_WEAPON", None)]
    keys = {}
    for t, col in fam:
        cur.execute("""select column_name from information_schema.columns
                       where table_schema='cfg' and table_name=%s and column_name<>'_row_id'
                       order by ordinal_position""", (t,))
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            rep.write("%-24s 库无表\n" % t)
            continue
        k = col or cols[0]
        cur.execute('select btrim("%s") from cfg."%s"' % (k, t))
        vals = [r[0] for r in cur.fetchall()]
        keys[t] = (k, vals)
        rep.write("%-24s 键列 %-20s 行 %-6d 去重 %-6d 长度分布 %s\n"
                  % (t, k, len(vals), len(set(vals)),
                     dict(sorted(Counter(len(v) for v in set(vals)).items()))))
    rep.write("\n")

    # 归一化对账
    domn = {norm(k) for k in dom}
    for t in ("ITEM", "WEAPON_SETTING", "WEAPON_BATTLE_DETAIL"):
        if t not in keys:
            continue
        k, vals = keys[t]
        raw = set(vals)
        nrm = {norm(v) for v in raw}
        rep.write("== %s ==  原始 %d ／ 归一化 %d\n" % (t, len(raw), len(nrm)))
        rep.write("   归一化后仍在号域外: %d  %s\n" % (len(nrm - domn), sorted(nrm - domn)[:15]))
        rep.write("   号域但没有的      : %d  %s\n" % (len(domn - nrm), sorted(domn - nrm)[:15]))
        rep.write("   原始形态在号域里    : %d / %d\n\n" % (len(raw & set(dom)), len(raw)))

    # ITEM 种子 vs 库（归一化）
    if "ITEM" in keys:
        db = set(keys["ITEM"][1])
        dbn = {norm(v) for v in db}
        sn = {norm(v) for v in set(seed)}
        rep.write("== ITEM 种子 vs 库（去前导 0 归一化后）==\n")
        rep.write("   种子归一 %d ／ 库归一 %d ／ 交 %d ／ 只在库 %d ／ 只在种子 %d\n"
                  % (len(sn), len(dbn), len(sn & dbn), len(dbn - sn), len(sn - dbn)))
        rep.write("   只在种子(归一)样例: %s\n" % sorted(sn - dbn)[:20])
        rep.write("   只在库(归一)样例  : %s\n" % sorted(dbn - sn)[:20])
        onlydb_norm = sorted(dbn - sn)
        rep.write("   只在库(归一) 中在号域**: %d / %d\n"
                  % (len([x for x in onlydb_norm if x in domn]), len(onlydb_norm)))
        onlyseed_norm = sorted(sn - dbn)
        rep.write("   只在种子(归一) 中在号域**: %d / %d\n"
                  % (len([x for x in onlyseed_norm if x in domn]), len(onlyseed_norm)))

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)

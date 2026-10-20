# -*- coding: utf-8 -*-
"""对账 v2：真库 POWER（客户端原值） vs sidecar 面板威力。

口径：库 raw 的机库白字 = |raw|×10（读侧 panelPowerFromClientRaw）。
      所以 raw 应该 ≈ 面板威力 / 10。
按**数值**归并（库里有 '02600151' 与 '2600151' 两种写法，一个数）。
"""
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def sidecar():
    ids, panel = {}, {}
    for r in csv.reader(open(SIDE, encoding="utf-8", errors="replace", newline="")
                        .read().replace("\r\n", "\n").split("\n")):
        if not r or r[0].startswith("#") or len(r) < 11 or not r[1].strip().isdigit():
            continue
        try:
            wid = int(r[1].strip())
        except ValueError:
            continue
        ids[wid] = (r[5].strip(), r[3].strip())
        pw = r[10].strip()
        if pw and pw.replace(".", "").lstrip("-").isdigit():
            panel[wid] = int(float(pw))
    return ids, panel


def main():
    ids, panel = sidecar()
    conn = psycopg.connect(DSN)
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value)
                     from cfg."WEAPON_BATTLE_DETAIL"
                    where btrim(attr_name)='POWER' and btrim(weapon_id_key) ~ '^[0-9]+$'""")
    raw = {}
    dupes = 0
    for k, v in cur.fetchall():
        try:
            n = int(k)
        except ValueError:
            continue
        try:
            iv = int(float(v))
        except ValueError:
            continue
        if n in raw and raw[n] != iv:
            dupes += 1
        raw[n] = iv
    conn.close()

    print("sidecar 武器 %d（有面板威力 %d）；库里 POWER 数值 id %d（重复键冲突 %d）"
          % (len(ids), len(panel), len(raw), dupes))

    both = sorted(set(raw) & set(panel))
    mismatch = [(n, raw[n], panel[n]) for n in both if raw[n] != round(panel[n] / 10)]
    print()
    print("=== 库里 POWER 数值 id 与 sidecar 面板威力对不上：%d / %d ===" % (len(mismatch), len(both)))
    for n, rv, pv in sorted(mismatch, key=lambda x: x[1])[:60]:
        nm, cls = ids.get(n, ("?", "?"))
        print("  %-10d 库raw=%-6d 应=%-6d 面板威力=%-7d %s %s" % (n, rv, round(pv / 10), pv, cls, nm))

    only_db = sorted(set(raw) - set(ids))
    print()
    print("=== 库里 POWER 有、sidecar 完全没这把武器：%d ===" % len(only_db))
    import collections
    bucket = collections.Counter()
    for n in only_db:
        bucket[len(str(n))] += 1
    print("  按位数：", dict(sorted(bucket.items())))
    for n in only_db[:60]:
        print("    %-12d raw=%s" % (n, raw[n]))

    only_sc = sorted(set(panel) - set(raw))
    print()
    print("=== sidecar 有面板威力、库里没有 POWER：%d（前 25）===" % len(only_sc))
    for n in only_sc[:25]:
        nm, cls = ids.get(n, ("?", "?"))
        print("    %-10d 面板威力=%-7d %s %s" % (n, panel[n], cls, nm))


if __name__ == "__main__":
    main()

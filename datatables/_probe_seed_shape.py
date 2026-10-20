# -*- coding: utf-8 -*-
"""写种子前的两个检查（只读）：
 ① manifest.raw_csv 的行形态：有没有注释头？行尾有没有逗号？字段数？
 ② 种子文件里，`#` 注释行是否只出现在数据区之前（决定"保留注释头"的写法是否安全）。
"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"f:\9ymsgo\9you"
T = {
    "ITEM": "item/item.csv",
    "MSMA_BATTLE_DETAIL": "msma/msma_battle_detail.csv",
    "CHARA_PARAM": "msma/msma_settings.csv",
    "WEAPON_SETTING": "item/weapon_settings.csv",
    "MECHANIC_WEAPON": "develop/mechanic_weapon.csv",
    "BUILDUP_WEAPON": "develop/buildup_weapon.csv",
}

with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as c:
    cur = c.cursor()
    for t, rel in T.items():
        cur.execute("select raw_csv from meta.cfg_manifest where file=%s", (t,))
        raw = cur.fetchone()[0]
        s = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
        lines = s.split("\n")
        data = [l for l in lines if l.strip() and not l.lstrip().startswith("#")]
        cmt = [l for l in lines if l.lstrip().startswith("#")]
        endc = sum(1 for l in data if l.endswith(","))
        ws = {}
        for l in data:
            n = len(l.split(","))
            ws[n] = ws.get(n, 0) + 1
        print("#%-20s mf 行 %5d ／ 注释行 %d ／ 行尾逗号 %d/%d ／ 字段数分布 %s"
              % (t, len(lines), len(cmt), endc, len(data), dict(sorted(ws.items()))))
        print("     首行 repr = %r" % (lines[0][:120],))

print()
for t, rel in T.items():
    p = os.path.join(ROOT, "server/datafiles/lounge", rel.replace("/", os.sep))
    b = open(p, "rb").read()
    bom = b.startswith(b"\xef\xbb\xbf")
    txt = b[3:].decode("utf-8", "replace") if bom else b.decode("utf-8", "replace")
    ls = txt.replace("\r\n", "\n").split("\n")
    first_data = None
    for i, l in enumerate(ls):
        if l.strip() and not l.lstrip().startswith("#"):
            first_data = i
            break
    after = [i for i, l in enumerate(ls) if i > (first_data or 0) and l.lstrip().startswith("#")]
    blanks = [i for i, l in enumerate(ls) if i > (first_data or 0) and not l.strip()]
    print("%-20s 种子 BOM=%-5s 首数据行 idx=%s ／ 数据区之后的注释行 %d ／ 空行 %d"
          % (t, bom, first_data, len(after), len(blanks)))

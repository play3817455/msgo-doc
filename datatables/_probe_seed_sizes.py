# -*- coding: utf-8 -*-
"""#37 全宽体积（只读）：manifest raw_csv 的字节数 vs 种子文件字节数。"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"f:\9ymsgo\9you"
SEEDS = {
    "WEAPON_SETTING": "item/weapon_settings.csv",
    "CHARA_PARAM": "msma/msma_settings.csv",
    "ITEM": "item/item.csv",
    "MECHANIC_WEAPON": "develop/mechanic_weapon.csv",
    "BUILDUP_WEAPON": "develop/buildup_weapon.csv",
    "MSMA_BATTLE_DETAIL": "msma/msma_battle_detail.csv",
}
with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as c:
    cur = c.cursor()
    for t, rel in SEEDS.items():
        cur.execute("select row_count, octet_length(raw_csv) from meta.cfg_manifest where file=%s", (t,))
        rc, nb = cur.fetchone()
        sp = os.path.join(ROOT, "server/datafiles/lounge", rel.replace("/", os.sep))
        print("%-20s manifest 行 %5d ／ raw_csv %9d 字节 ／ 种子文件 %9d 字节"
              % (t, rc, nb, os.path.getsize(sp)))

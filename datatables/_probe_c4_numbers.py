# -*- coding: utf-8 -*-
"""复核 §6.2 的两个数字（只读）。"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"f:\9ymsgo\9you"
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

raw = open(os.path.join(ROOT, "server/datafiles/lounge/msma/msma_settings.csv"),
           "rb").read().decode("utf-8", "replace")
seed = {}
for ln in raw.replace("\r\n", "\n").split("\n"):
    if not ln.strip() or ln.lstrip().startswith("#"):
        continue
    f = ln.split(",")
    seed[f[0].strip()] = f

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select count(*) from cfg."CHARA_PARAM" where coalesce(btrim(max_speed_base::text),\'\')<>\'\'')
    print("库 max_speed_base 非空行 =", cur.fetchone()[0])
    cur.execute('select msma_id, btrim(max_speed_base::text) from cfg."CHARA_PARAM"')
    n = 0
    ex = []
    for k, v in cur.fetchall():
        fs = seed.get(k) or []
        sv = fs[89].strip() if len(fs) > 89 else ""
        if (v or "") != sv:
            n += 1
            if len(ex) < 3:
                ex.append((k, sv, v))
    print("种子 col89 与库不同的行数 =", n, ex)
    for col in ("battle_detail_key_respawn", "battle_detail_key_warp"):
        cur.execute('select count(distinct msma_id) from cfg."CHARA_PARAM" '
                    'where coalesce(btrim(%s::text),\'\')<>\'\'' % col)
        print("库 %s 非空行 = %d" % (col, cur.fetchone()[0]))
    cur.execute('select count(*) from cfg."CHARA_PARAM"')
    print("库总行 =", cur.fetchone()[0])
    # 10 台残行：种子里 payload_capacity_base 也空？
    cur.execute('select msma_id, btrim(payload_capacity_base::text), btrim(armor_base::text) '
                'from cfg."CHARA_PARAM" where msma_id in '
                "('1105021','1146072','1148082','1201301','1208012','1215201','1244091','1422012','1503021','1507012') order by 1")
    for k, p, a in cur.fetchall():
        fs = seed.get(k) or []
        print("   %s 库 payload=%s armor=%s ／ 种子 payload=%r armor=%r"
              % (k, p, a, fs[52].strip() if len(fs) > 52 else "", fs[90].strip() if len(fs) > 90 else ""))

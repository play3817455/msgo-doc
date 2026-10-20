# -*- coding: utf-8 -*-
"""体检：补列脚本加出来的新列是不是 NULL-able / 有没有残留 NULL（cfg 其余列都是 NOT NULL DEFAULT ''）。"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLES = [
    "WEAPON_BATTLE_DETAIL", "MSMA_BATTLE_DETAIL",     # 本批补列
    "PLAY_BONUS_REWARD", "PLAYER_NAVI", "BUFF", "MODULE_DEVELOP", "MISSION_EXTRULE",  # 第 1 批补列
    "QUEST",                                           # 第 2 批补列
]

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        cur.execute("""SELECT column_name, is_nullable, coalesce(column_default,'')
                       FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        cols = cur.fetchall()
        nullable = [c for c in cols if c[1] == "YES"]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        n = cur.fetchone()[0]
        nulls = []
        for c in cols:
            if c[1] != "YES":
                continue
            cur.execute(f'SELECT count(*) FROM cfg."{t}" WHERE "{c[0]}" IS NULL')
            k = cur.fetchone()[0]
            if k:
                nulls.append((c[0], k))
        print(f"[{t}] 列 {len(cols)}｜行 {n}｜NULL-able 列 {len(nullable)}"
              f"｜带 NULL 值的列 {len(nulls)}")
        if nullable:
            print("   nullable:", ", ".join(f"{c[0]}(default={c[2]!r})" for c in nullable))
        if nulls:
            print("   有 NULL 的行:", ", ".join(f"{c}={k}" for c, k in nulls[:8])
                  + (" …" if len(nulls) > 8 else ""))

# -*- coding: utf-8 -*-
"""#37 枚举列体检：所有格子是否都在客户端已知的字面量集合里。

为什么重要：`01-列注释/37-…` 末尾写明「枚举列写名称字符串（**写错/未知名 ⇒ 该列读作 0**）」。
即**未知字面量不会报错，只会静默变 0** —— 上一轮我把 CSV col0..col33 按种子收敛过，
必须确认种子没引入客户端不认识的字面量。

合法集来源：`reverse-login-chain/formats/枚举表.md`（按转换函数实名，取自 EXE）。
对照两侧：**当前库** vs **收敛前回滚件**（`_rollback/*_WEAPON_SETTING_seed_sync.csv`）。
只读。
"""
import csv
import io
import os
import sys

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# csv_index -> (转换函数, 合法字面量集合)
FLAG = {
    13: ("sub_5968A0", "ONEHAND SHOLDER TWOHAND SHIELD PECULIAR_1 PECULIAR_2 PECULIAR_3"
                      " PECULIAR_4 PECULIAR_5 PECULIAR_6 MODELORIGIN"),
    15: ("sub_596990", "WRESTLE WRESTLE2 SHIELD SHIELD2 ATTACH_SHIELD SHOT_SHIELD SHOTGUN"
                       " ONEHAND_SHOT SHOLDER_SHOT TWOHAND_SHOT TWOHAND_SHOT2 SPECIAL_SHOT"
                       " SPECIAL_SHOT2 SNAIP_SHOT SETUP COMMON"),
    16: ("sub_596A80", "WRESTLE WRESTLE2 SHIELD SHIELD2 ATTACH_SHIELD SHOTGUN"
                       " ONEHAND_SHOT SHOLDER_SHOT TWOHAND_SHOT SPECIAL_SHOT"
                       " SNAIP_SHOT SETUP COMMON"),
    21: ("sub_596B70", "MACHINEGUN SHOTGUN BAZOOKA GRENADE_LAUNCHER MISSILE BEAM WRESTLE"
                       " SNIPE TRENCH_MORTAR LANDMINE HAND_THROW SENTRYGUN REPAIR SHIELD"
                       " RADAR CAMERAGUN TRAP BOMB SOLAR_RAY CARRY_CONTAINER CARRY_STG_ARMS"
                       " CARRY_HAND_THROW CARRY_WALL CARRY_DUMMY_BEACON BULLET_PACK AAG_POD"
                       " WALL SONAR_GUN FREEZY_YARD DOT CARRY_GUIDE_BEACON CARRY_STGARMS2"
                       " CHAIN_MINE STEALTH SEARCH_GRENADE MS_EXCHANGE REPAIR_PACK"
                       " FRONT_RADAR RESURRECT DUMMY_BALLOON BAKUDOSAKU FUNNEL SHIELD_ANY"
                       " WRESTLE_REPAIR ROCK_THROW BUFF_ATTACK_UP DAMAGE_FIELD_ANY BOOMERANG"
                       " BOOMERANG_CHAIN SHOT_LANDMINE HOMING_BEAM REPAIR_THROW"),
    29: ("sub_596510", "NORMAL SCATTERS VERTICAL_WAY SIDE_WAY SIDE_WAY_2 SP_BEAM"
                       " TRENCH_MORTAR PARALLEL"),
    30: ("sub_596C60", "NONE SHIELD GUN_SINGLE GUN_RAPID WRESTLE GRENADE HAND_THROW"
                       " DEPLOY_ARMS TRENCH_MORTAR SNIPE_BEAM BIT DAMAGE_FIELD SNIPE_SINGLE"
                       " THROW_SINGLE BOMB HOMING HOMING_CHAIN HOMING_BEAM BOOMERANG HAMMER"
                       " WHIP FOR_MYSELF FUNNEL GUN_RAPID_HOMING BUFF_RAPID_HOMING"
                       " DAMAGE_FIELD_GUN SENTRY_GUN BOOMERANG_CHAIN SHOT_LANDMINE"),
    31: ("sub_5965F0", "NONE LOCKON SCOPE LOCKON_HOMING LOCKON_BOOMERANG FUNNEL INCOM"
                       " FUNNEL_MK2 SENSING_SCOPE"),
    32: ("sub_5964A0", "SOLID BEAM BLAST DEAD"),
    128: ("sub_596D50", "RADAR_JAMMING SHORT FLASHBANG SC_JAMMING_A SC_JAMMING_B BLAZING"
                        " SLOW DEBUFF DEBUFF_ATK BUFF_DEF GN_FANG_A_SLOW GN_FANG_B_SLOW"
                        " GN_FANG_A_SHORT GN_FANG_B_SHORT PENETRATION"),
    137: ("sub_596990", None),   # 同 15
    146: ("sub_596D50", None),   # 枚举表记 col146 亦 sub_596D50；00-表清单 记 FB_* ⇒ 先看实测
}
FLAG[137] = (FLAG[137][0], FLAG[15][1])
FLAG[146] = (FLAG[146][0], FLAG[128][1])


def legal(csv_i):
    return set(FLAG[csv_i][1].split())


def latest_backup():
    fs = sorted(f for f in os.listdir(RB_DIR)
                if f.endswith("_WEAPON_SETTING_seed_sync.csv"))
    return os.path.join(RB_DIR, fs[-1]) if fs else None


def dist(cur, col, ids=None):
    q = 'SELECT btrim("%s"), count(*) FROM cfg."WEAPON_SETTING"' % col
    if ids is not None:
        q += ' WHERE btrim(weapon_setting_id) = ANY(%s)'
    q += ' GROUP BY 1 ORDER BY 2 DESC'
    cur.execute(q, (ids,) if ids is not None else None)
    return cur.fetchall()


def main():
    rb = latest_backup()
    print("=== 对照物 ===")
    print("  当前库   : cfg.WEAPON_SETTING")
    print("  收敛前快照: %s" % (os.path.relpath(rb, ROOT) if rb else "(缺)"))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                        ORDER BY ordinal_position""")
        by_csv = {pos - 2: n for pos, n in cur.fetchall()}
        cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
        nrows = cur.fetchone()[0]

        # 收敛前快照：整表列值
        old = {}
        if rb:
            with io.open(rb, encoding="utf-8", newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd)
                oi = {}
                for c in FLAG:
                    nm = by_csv.get(c)
                    oi[c] = hdr.index(nm) if nm in hdr else None
                ikey = hdr.index("weapon_setting_id")
                for row in rd:
                    old[row[ikey].strip()] = {c: (row[oi[c]].strip() if oi[c] is not None else "")
                                              for c in FLAG}

        print()
        print("库行 %d ／ 快照行 %d" % (nrows, len(old)))
        print()

        bad_total = 0
        for c in sorted(FLAG):
            fn, _ = FLAG[c]
            nm = by_csv.get(c, "?")
            L = legal(c)
            rows = dist(cur, nm)
            vals = [(v or "", n) for v, n in rows]
            nonempty = [(v, n) for v, n in vals if v != ""]
            unknown = [(v, n) for v, n in nonempty if v not in L]
            empty = sum(n for v, n in vals if v == "")

            # 快照侧同列
            oldvals = {}
            for k, d in old.items():
                v = d.get(c, "")
                if v:
                    oldvals[v] = oldvals.get(v, 0) + 1
            oldunk = {v: n for v, n in oldvals.items() if v not in L}

            mark = "✗" if unknown else "✓"
            print("%s csv%-4d %-22s %-11s 取值 %2d 种（空 %4d 行）"
                  % (mark, c, nm, fn, len(nonempty), empty))
            if unknown:
                bad_total += len(unknown)
                for v, n in sorted(unknown, key=lambda x: -x[1]):
                    print("      ✗ 非法字面量 %-20r × %d 行" % (v, n))
                for v, n in sorted(oldunk.items()):
                    print("        └ 收敛前快照里也有：%r × %d" % (v, n))
            if oldunk and not unknown:
                print("      （快照侧有非法值、现已修正：%s）" % sorted(oldunk))

        print()
        if bad_total == 0:
            print("★ 全部枚举格都在客户端已知字面量集合内 —— 收敛未引入任何'静默变 0'风险")
        else:
            print("✗ 共 %d 种非法字面量，见上" % bad_total)

    # ── 另：col18 / col28 / col146 先做形态观察（合法集未定案） ──────────────
    print()
    print("=== 待定案列的实测取值（col18 / col28 / col146）===")
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                        ORDER BY ordinal_position""")
        by_csv = {pos - 2: n for pos, n in cur.fetchall()}
        for c in (18, 28, 146):
            nm = by_csv.get(c, "?")
            print("  csv%-4d %-28s %s" % (c, nm, dist(cur, nm)[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

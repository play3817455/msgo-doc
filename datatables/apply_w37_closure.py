# -*- coding: utf-8 -*-
"""apply_w37_closure.py —— `#37 WEAPON_SETTING` 收口（15- 文档 §15.3 / §15.5 的施工）

═══════════════════════ 做三件事（都只碰被点名的行）═══════════════════════
A1  15 行「`#36` 属性连接键多一个前导 0」→ 改写成各自 `weapon_setting_id`
    （`1010401` 那行的键现为 `01010401`，在 `#36` 里 **0/15 命中**；
      自身 ID 则 15/15 命中 ⇒ 这 15 把武器取不到 POWER/RANGE/… 任何数值）
A2  补 3 行（**种子 CSV 里本来就有，库里缺**）：
    `212301109` 光束加农 命中强化型 / `212301110` 光束加农 弹夹强化型 /
    `223005102` 头部火神炮 弹夹强化M型
    —— 三者的 `#36` 属性行、`#78 ITEM` 行都已存在，只差 `#37` 这一环。
    34 列取值**逐字取自种子**（不猜）；其余 114 列留空；
    11 个连接键 = 自身 ID（与库内其余 1630 行同惯例）。
B   种子 `item/weapon_settings.csv` 删掉 4 个 8 位头像（15- 文档 §11.3）：
    `12010101` `12840101` `13200151` `13200251`
    —— 它们只出现在 cutin/语音/名字工件里，不是真武器；
    不删的话下次 `bootstrap-csv` 会把它们带回库。

═══════════════════════ 收纳后的账（必须平）═══════════════════════
  种子 1652 行 = 库 1645 + 3（A2 要补） + 4（B 要删）
  ⇒ 做完：库 1648 行 ／ 种子 1648 行

⚠️ 本脚本**不动**其余 1645 行的 34 列（那是另一件事：实测种子与库在这些列上
   还有 492 个单元格不一致，见 `_probe_w37_seed_vs_db.py`，单独决策）。

安全
====
- 默认**干跑**；`--apply` 才写。
- 写前把整张 `#37`（149 列全量）导出成 `_rollback/<stamp>_WEAPON_SETTING_full.csv`，
  种子 CSV 备份成 `weapon_settings.csv.bak_closure<stamp>`。
- 写在一个事务里，写后自检，任一项不过就 ROLLBACK。

用法
====
  python datatables/apply_w37_closure.py            # 干跑
  python datatables/apply_w37_closure.py --apply    # 写库 + 改种子
"""
import csv
import datetime
import io
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

LINKS = ["effect_name_list", "hit_effect_list", "muzzle_effect_list", "trail_effect_list",
         "sound_set_list", "voice_set_list", "camera_shake_list", "screen_flash_list",
         "buff_effect_list", "debuff_effect_list", "spawn_effect_list"]
ADD = ["212301109", "212301110", "223005102"]
DROP = ["12010101", "12840101", "13200151", "13200251"]
SEED_COLS = 34          # 种子只写到 CSV col33


def read_seed():
    with open(SEED, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    lines = raw.split("\r\n")
    head = [l for l in lines if l.startswith("#")]
    data = [l for l in lines if l.strip() and not l.startswith("#")]
    return raw, lines, head, data


def main():
    apply = "--apply" in sys.argv
    raw, lines, head, data = read_seed()
    by_id = {}
    for l in data:
        by_id.setdefault(l.split(",")[0].strip(), l)
    print("=== 种子 CSV ===")
    print("  %s" % os.path.relpath(SEED, ROOT))
    print("  数据行 %d ／ 注释行 %d ／ CRLF %d" % (len(data), len(head), raw.count("\r\n")))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                        ORDER BY ordinal_position""")
        phys = cur.fetchall()
        dbcols = [n for _, n in phys]
        by_csv = {pos - 2: n for pos, n in phys}
        if by_csv.get(0) != "weapon_setting_id" or by_csv.get(64) != "ammo_type_id":
            print("✗ 列映射自检失败（CSV0=%s / CSV64=%s）" % (by_csv.get(0), by_csv.get(64)))
            return 2

        cur.execute('SELECT DISTINCT btrim(weapon_id_key) FROM cfg."WEAPON_BATTLE_DETAIL"')
        d36 = {r[0] for r in cur.fetchall()}
        cur.execute('SELECT btrim(weapon_setting_id), btrim(effect_name_list) FROM cfg."WEAPON_SETTING"')
        dbrows = cur.fetchall()
        cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
        n0 = cur.fetchone()[0]
        cur.execute('SELECT coalesce(max(_row_id), 0) FROM cfg."WEAPON_SETTING"')
        maxrow = cur.fetchone()[0]

    dbids = {w for w, _ in dbrows}
    broken = sorted((w, k) for w, k in dbrows if k != w)
    print()
    print("=== A1：%d 行连接键断链 ===" % len(broken))
    for w, k in broken:
        print("  %s : %s → %s   （%s 在 #36：%s）"
              % (w, k, w, k, k in d36))
    print("  ⇒ 改后这 %d 行的键全部命中 #36：%s"
          % (len(broken), all(w in d36 for w, _ in broken)))

    print()
    print("=== A2：补 %d 行 ===" % len(ADD))
    for k in ADD:
        if k in dbids:
            print("  %s ✗ 库里已有，中止" % k)
            return 2
        ln = by_id.get(k)
        if not ln:
            print("  %s ✗ 种子里没有，中止" % k)
            return 2
        parts = ln.split(",")
        print("  %s  种子 %d 列  非空 %s"
              % (k, len(parts), [(i, v) for i, v in enumerate(parts) if v and i]))
        print("      键在 #36：%s" % (k in d36))

    print()
    print("=== B：种子删 %d 行 ===" % len(DROP))
    for k in DROP:
        print("  %s  命中种子 %s" % (k, k in by_id))

    print()
    print("=== 写后应达到 ===")
    print("  库行数   %d → %d  （+%d 个缺键）" % (n0, n0 + len(ADD), len(ADD)))
    print("  种子行数 %d → %d  （-%d 个 8 位头像；3 个真武器本来就在种子里）"
          % (len(data), len(data) - len(DROP), len(DROP)))
    bal = (n0 + len(ADD)) == (len(data) - len(DROP))
    print("  账平：库 %d == 种子 %d  %s"
          % (n0 + len(ADD), len(data) - len(DROP), "✓" if bal else "✗"))
    if not bal:
        print("  ⚠️ 不平 ⇒ 说明还有别的差异（先别用 --apply）")

    if not apply:
        print()
        print("★ 干跑：加 --apply 写入。")
        return 0

    # ── 备份 ────────────────────────────────────────────────────────────────
    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(RB_DIR, "%s_WEAPON_SETTING_full.csv" % stamp)
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT %s FROM cfg."WEAPON_SETTING" ORDER BY _row_id'
                    % ", ".join('"%s"' % c for c in dbcols))
        allrows = cur.fetchall()
    with open(rb, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(dbcols)
        w.writerows([["" if v is None else str(v) for v in r] for r in allrows])
    seed_bak = SEED + ".bak_closure" + stamp
    shutil.copy2(SEED, seed_bak)
    print()
    print("回滚件 → %s（%d 行 × %d 列）" % (os.path.relpath(rb, ROOT), len(allrows), len(dbcols)))
    print("种子备份 → %s" % os.path.relpath(seed_bak, ROOT))

    # ── 写库 ────────────────────────────────────────────────────────────────
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        try:
            sets = ", ".join('"%s" = btrim(weapon_setting_id)' % c for c in LINKS)
            cur.execute('UPDATE cfg."WEAPON_SETTING" SET ' + sets +
                        ' WHERE btrim(effect_name_list) <> btrim(weapon_setting_id)')
            print("  A1 已改：%d 行（期望 %d）" % (cur.rowcount, len(broken)))
            if cur.rowcount != len(broken):
                raise AssertionError("A1 行数不符")

            for i, k in enumerate(ADD):
                parts = by_id[k].split(",")
                vals = {}
                for csv_i, v in enumerate(parts[:SEED_COLS]):
                    vals[by_csv[csv_i]] = v
                for c in LINKS:
                    vals[c] = k
                colnames = ["_row_id"] + list(vals)
                sql = 'INSERT INTO cfg."WEAPON_SETTING" (%s) VALUES (%s)' % (
                    ", ".join('"%s"' % c for c in colnames),
                    ", ".join(["%s"] * len(colnames)))
                cur.execute(sql, [maxrow + i + 1] + list(vals.values()))
            print("  A2 已插：%d 行" % len(ADD))

            cur.execute("""SELECT count(*) FROM cfg."WEAPON_SETTING"
                            WHERE btrim(effect_name_list) <> btrim(weapon_setting_id)""")
            still = cur.fetchone()[0]
            cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
            n1 = cur.fetchone()[0]
            cur.execute("""SELECT count(*) FROM cfg."WEAPON_SETTING"
                            WHERE btrim(weapon_setting_id) IN ('212301109','212301110','223005102')""")
            got = cur.fetchone()[0]
            if still or n1 != n0 + len(ADD) or got != len(ADD):
                raise AssertionError("写后自检不过：残留断链%d 行%d 新行%d" % (still, n1, got))
            print("  自检：残留断链 %d ／ 行 %d ／ 3 个新键齐 %d  ✓" % (still, n1, got))
            conn.commit()
            print("★ 已提交")
        except Exception as e:
            conn.rollback()
            print("✗ 失败已 ROLLBACK：%s" % e)
            raise

    # ── 写种子 ──────────────────────────────────────────────────────────────
    kept = [l for l in lines if not (l.strip() and not l.startswith("#")
                                     and l.split(",")[0].strip() in DROP)]
    out = "\r\n".join(kept)
    with open(SEED, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    _, _, _, data2 = read_seed()
    print("  B 种子已写：数据行 %d → %d（删了 %d）"
          % (len(data), len(data2), len(data) - len(data2)))

    print()
    print("下一步（否则客户端看不到）：")
    print("  cd serverv; go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables"
          " -export-only -migrate=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())

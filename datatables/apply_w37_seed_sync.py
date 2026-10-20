# -*- coding: utf-8 -*-
"""apply_w37_seed_sync.py —— `#37 WEAPON_SETTING` 的 CSV col0..col33 按种子收敛（15- 文档 §18.4）

═══════════════════════ 为什么 ═══════════════════════
`#37` 的行集合已经和种子对齐（=`apply_w37_closure.py`，1648 = 1648），
但**取值**还差 **492 个单元格**。可判的硬证据指向**种子对、库错**：

  223005101  库=TWOHAND/WRESTLE/WRESTLE/BEAM   种子=ONEHAND/MACHINEGUN/GUN_RAPID/SOLID
             而 `#36` 里它是 `POWER 40` + 有 `RAPIDDELAY`/`COOLTIME`
             （连发枪特征，格斗武器不会有）⇒ 种子对
  214802001/101/102  库=WRESTLE+TWOHAND → 种子=MACHINEGUN+ONEHAND（成对改，同向）

═══════════════════════ 做什么 / 不做什么 ═══════════════════════
✅ 只写 **CSV col0..col33**（种子里存在的 34 列），逐行逐列 = 种子原值。
⛔ **绝不碰**库侧独有的 114 列 —— 尤其那 **11 个 `#36` 连接键**
   （`effect_name_list` … `spawn_effect_list`）、`ammo_type_id`(col64)、
   以及 `parent_setting_id` 之外的其余列。种子里根本没有这些列，
   按"整行替换"会把它们清空 ⇒ **客户端全族属性塌 0**。
⛔ 不动行数、不动 `_row_id`。

安全
====
- 默认**干跑**并打印完整差异清单（按列汇总 + 逐行明细）；`--apply` 才写。
- 写前把整张 `#37`（149 列全量）备份到 `_rollback/<stamp>_WEAPON_SETTING_seed_sync.csv`。
- 一个事务；写后自检（34 列 ≡ 种子、11 键仍全自洽、行数不变），不过就 ROLLBACK。

用法
====
  python datatables/apply_w37_seed_sync.py            # 干跑 + 差异清单
  python datatables/apply_w37_seed_sync.py --apply    # 写库
"""
import csv
import datetime
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

SEED_COLS = 34
LINKS = ["effect_name_list", "hit_effect_list", "muzzle_effect_list", "trail_effect_list",
         "sound_set_list", "voice_set_list", "camera_shake_list", "screen_flash_list",
         "buff_effect_list", "debuff_effect_list", "spawn_effect_list"]


def read_seed():
    with open(SEED, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    out = {}
    for l in raw.split("\r\n"):
        if not l.strip() or l.startswith("#"):
            continue
        parts = l.split(",")
        if len(parts) < SEED_COLS:
            parts += [""] * (SEED_COLS - len(parts))
        out[parts[0].strip()] = [p.strip() for p in parts[:SEED_COLS]]
    return out


def main():
    apply = "--apply" in sys.argv
    seed = read_seed()
    print("=== 种子 ===")
    print("  %s  行 %d" % (os.path.relpath(SEED, ROOT), len(seed)))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                        ORDER BY ordinal_position""")
        phys = cur.fetchall()
        dbcols = [n for _, n in phys]
        by_csv = {pos - 2: n for pos, n in phys}
        if by_csv.get(0) != "weapon_setting_id" or by_csv.get(64) != "ammo_type_id":
            print("✗ 列映射自检失败")
            return 2
        targets = [(c, by_csv[c]) for c in range(SEED_COLS)]
        sel = ", ".join('btrim("%s")' % n for _, n in targets)
        cur.execute('SELECT ' + sel + ', btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
        rows = cur.fetchall()
        cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
        n0 = cur.fetchone()[0]

    db = {}
    for r in rows:
        db[r[-1]] = list(r[:-1])
    print("  库行 %d ／ 交集 %d ／ 只在种子 %s ／ 只在库 %s"
          % (n0, len(set(seed) & set(db)),
             sorted(set(seed) - set(db))[:9], sorted(set(db) - set(seed))[:9]))

    # ── 差异清单 ────────────────────────────────────────────────────────────
    per_row = {}
    per_col = {}
    for k in sorted(set(seed) & set(db)):
        for i, (csv_i, name) in enumerate(targets):
            a = (db[k][i] or "").strip()
            b = (seed[k][csv_i] or "").strip()
            if a != b:
                per_row.setdefault(k, []).append((csv_i, name, a, b))
                per_col.setdefault(csv_i, [0, name])[0] += 1

    print()
    print("=== 差异汇总 ===")
    print("%-5s %-24s %-7s %s" % ("CSV", "库列名", "不同", "样本（库 → 种子）"))
    tot = 0
    for csv_i in sorted(per_col):
        n, name = per_col[csv_i]
        tot += n
        samples = []
        for k in sorted(per_row):
            for c, nm, a, b in per_row[k]:
                if c == csv_i and len(samples) < 3:
                    samples.append("%s:%r→%r" % (k, a, b))
        print("%-5d %-24s %-7d %s" % (csv_i, name, n, " ; ".join(samples)))
    print("%-5s %-24s %-7d" % ("", "合计", tot))
    print()
    print("受影响行数 %d / %d ；最多差异一行 %d 格"
          % (len(per_row), len(db),
             max([len(v) for v in per_row.values()] or [0])))

    print()
    print("=== 逐行明细（最多 40 行）===")
    for k in sorted(per_row)[:40]:
        diffs = " ".join("csv%d:%r→%r" % (c, a, b) for c, _, a, b in per_row[k])
        print("  %-12s %s" % (k, diffs))
    if len(per_row) > 40:
        print("  … 另 %d 行" % (len(per_row) - 40))

    # ── 保护性自检：确认要写的是 34 列，且 11 个键列没被波及 ────────────────
    print()
    print("=== 保护性自检 ===")
    touched = {n for _, n in targets}
    print("  本次写集 %d 列：%s" % (len(touched), sorted(touched)))
    print("  11 个连接键在写集里（必须 False）：%s"
          % sorted(touched & set(LINKS)))
    print("  ammo_type_id 在写集里（必须 False）：%s" % ("ammo_type_id" in touched))
    print("  未触及列数 %d / %d" % (len(dbcols) - 1 - len(touched), len(dbcols) - 1))

    if not apply:
        print()
        print("★ 干跑：加 --apply 写库（只写上面这 34 列，其余 %d 列不动）。"
              % (len(dbcols) - 1 - len(touched)))
        return 0

    # ── 备份 ────────────────────────────────────────────────────────────────
    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(RB_DIR, "%s_WEAPON_SETTING_seed_sync.csv" % stamp)
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT %s FROM cfg."WEAPON_SETTING" ORDER BY _row_id'
                    % ", ".join('"%s"' % c for c in dbcols))
        allrows = cur.fetchall()
    with open(rb, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(dbcols)
        w.writerows([["" if v is None else str(v) for v in r] for r in allrows])
    print()
    print("回滚件 → %s（%d 行 × %d 列）" % (os.path.relpath(rb, ROOT), len(allrows), len(dbcols)))

    # ── 写库 ────────────────────────────────────────────────────────────────
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        try:
            setters = ", ".join('"%s" = %%s' % n for _, n in targets)
            sql = ('UPDATE cfg."WEAPON_SETTING" SET ' + setters +
                   ' WHERE btrim(weapon_setting_id) = %s')
            done = 0
            for k in sorted(set(seed) & set(db)):
                vals = [seed[k][c] for c, _ in targets] + [k]
                cur.execute(sql, vals)
                if cur.rowcount == 1:
                    done += 1
            print("  已写：%d 行" % done)

            # A3：补齐 ammo_type_id（= #BUILDUP_WEAPON 查键，不在种子 34 列里）
            # 库内其余行全是 '1'；`apply_w37_closure.py` 补的 3 行当初没给这列 ⇒ 会取不到强化档。
            cur.execute("""UPDATE cfg."WEAPON_SETTING" SET ammo_type_id = '1'
                            WHERE ammo_type_id IS NULL OR btrim(ammo_type_id) IN ('', '0')""")
            print("  A3 补齐 ammo_type_id：%d 行" % cur.rowcount)

            # 写后自检
            cur.execute('SELECT ' + sel + ', btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
            now = {r[-1]: list(r[:-1]) for r in cur.fetchall()}
            left = 0
            for k in set(seed) & set(now):
                for i, (csv_i, _n) in enumerate(targets):
                    if (now[k][i] or "").strip() != (seed[k][csv_i] or "").strip():
                        left += 1
            cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
            n1 = cur.fetchone()[0]
            linkbad = 0
            for c in LINKS:
                cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"'
                            ' WHERE btrim("%s") <> btrim(weapon_setting_id)' % c)
                linkbad += cur.fetchone()[0]
            cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"'
                        " WHERE ammo_type_id IS NULL OR btrim(ammo_type_id) IN ('', '0')")
            ammo = cur.fetchone()[0]
            print("  写后自检：34 列残留差异 %d ／ 行数 %d（写前 %d）／ 11 键不符 %d ／ ammo 缺 %d"
                  % (left, n1, n0, linkbad, ammo))
            if left or n1 != n0 or linkbad or ammo != 0:
                raise AssertionError("写后自检不过：left=%d n=%d linkbad=%d ammo=%d"
                                     % (left, n1, linkbad, ammo))
            conn.commit()
            print("★ 已提交（34 列 ≡ 种子；11 键未受影响；ammo_type_id %d 行全就位）" % n1)
        except Exception as e:
            conn.rollback()
            print("✗ 失败已 ROLLBACK：%s" % e)
            raise

    print()
    print("下一步（否则客户端看不到）：")
    print("  cd serverv; go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables"
          " -export-only -migrate=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())

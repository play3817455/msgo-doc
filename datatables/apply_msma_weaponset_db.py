# -*- coding: utf-8 -*-
"""apply_msma_weaponset_db.py —— 把 `cfg."MSMA_WEAPONSET"` 收敛到种子 CSV（唯一权威）。

═══════════════════════ 为什么必须做（15- 文档 §11.2 的收口）═══════════════════════
`cfg."MSMA_WEAPONSET"`（#1，`sub_587160` / `CMSMAWeaponSetTable`）里住着**两组互斥的号族**：

| 族 | 组数 | 行数 | 出处 | 现状 |
|---|---|---|---|---|
| 9 位 sidecar 族 | 358 | 1063 | `msma/msma_weapon_set.csv`（`gen_weapon_set_wiki.py` 产物） | 1063/1063 在 `#37`、`#36`、`ITEM` 里都有行 ⇒ **健康** |
| 8 位 icon-id 族 | 235 | 1181 | `load_paired_ms_db.py`（`gow_wiki/data/units.json` 的 `icon_id`） | 792 个号里**只有 3 个**在真库 `#37` 里有行 ⇒ **789 个断引用** |

而 `purge_unreachable_weapon_keys.py` 判「可达号域」时用的**现役引用**正是
`msma_weapon_set.csv` col2（1625 个全 9 位）∪ `game.unlockw` ∪ `game.ms_rokaku` ——
**8 位族不在其中**，所以上一轮净化把 8 位族从 `#36`/`#37` 删了，却没同步 `MSMA_WEAPONSET`。
⇒ 库里出现「MS 武器组引用了没有 `#37` 行的武器」789 处，正是 `#37` col2 门闩=0
「装备组走活体分支崩」的风险面。

**另外**：现库 9 位族只是种子的**部分**快照（1063/1625 行、358/549 组）。
补上剩下的 562 行**零新增断引用**（实测 562/562 在 `#37`/`#36`/`ITEM` 里都有行）。

⇒ 结论：**库 ≡ 种子 CSV**。本脚本做整表替换，不做逐键 upsert（避免残留族）。

⚠️ 已知代价（唯一一条）：8 位族里有 **44 个组**在种子 CSV 里**没有任何行**
（`gen_weapon_set_wiki.py` 对未解析机体一律不生成）。收敛后这 44 台机体**没有武器组**。
它们当前引用的是那 789 个断引用里的一员 ⇒ **现在已经是坏的**；清掉不会更坏。
脚本会把 44 个组名与它们原有的行一起打进回滚件，可随时复原。

安全
====
- 默认**干跑**；`--apply` 才写库。
- 写库前把**整表 29 列全量**导出成 `_rollback/<stamp>_MSMA_WEAPONSET_full.csv`（带表头，
  可直接 `COPY` 重灌），并打印复原命令。
- 写入在一个事务里；写后立刻自检，**任一项不过就 ROLLBACK**。

用法
====
  python datatables/apply_msma_weaponset_db.py            # 干跑 + 报告
  python datatables/apply_msma_weaponset_db.py --apply    # 写库（先留回滚件）
"""
import csv
import datetime
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
BRIDGE = os.path.join(HERE, "names", "机体-wiki武器页桥.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

GROUP_RE = re.compile(r"^\d{7}$")
NCOL = 29          # 库列（除 _row_id）；schema `MSMA_WEAPONSET.json`: column_defined=29, csv col0..col28


def load_seed():
    """读种子 CSV → [(组ID, [29 列])]，顺序即下发顺序。

    方言：`gen_weapon_set_wiki.py:233-235` 写的是 `row = ['']*30` 再 `join + ','`
    ⇒ 裸行有 31 个 split 字段（0..29 是数据、30 是尾逗号空段），其中第 29 段恒空、
    不在 schema 的 col0..col28 内。这里只取前 29 段。
    """
    rows, bad = [], []
    with open(SEED, encoding="utf-8-sig") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            body = line[:-1] if line.endswith(",") else line   # 去掉格式尾逗号
            cols = body.split(",")
            if len(cols) == NCOL + 1 and cols[-1] == "":
                cols = cols[:NCOL]        # 生成器的第 30 段（恒空、schema 外）
            if len(cols) < NCOL:
                cols += [""] * (NCOL - len(cols))
            elif len(cols) > NCOL:
                bad.append((ln, "列数 %d > %d" % (len(cols), NCOL), line[:90]))
                continue
            gid = cols[0].strip()
            if not GROUP_RE.match(gid):
                bad.append((ln, "组ID 不是 7 位: %r" % gid, line[:90]))
                continue
            rows.append((gid, [c.strip() for c in cols]))
    return rows, bad


def main():
    apply = "--apply" in sys.argv
    seed, bad = load_seed()

    seed_pairs = [(g, r[2]) for g, r in seed]
    seed_ids = {r[2] for _, r in seed}
    seed_groups = {g for g, _ in seed}

    print("=== 种子 CSV ===")
    print("  %s" % os.path.relpath(SEED, ROOT))
    print("  数据行 %d ／ 组 %d ／ 去重武器 %d" % (len(seed), len(seed_groups), len(seed_ids)))
    print("  号长   %s" % dict(sorted({len(i): sum(1 for j in seed_ids if len(j) == len(i))
                                      for i in seed_ids}.items())))
    print("  槽位分布 %s" % {k: sum(1 for _, r in seed if r[4] == k) for k in ("MAIN", "EX")})
    print("  col28 取值 %s" % sorted({r[28] for _, r in seed}))
    if bad:
        print("  ✗ 解析异常 %d 行：" % len(bad))
        for x in bad[:5]:
            print("      %s" % (x,))
        return 2
    if not seed:
        print("  ✗ 种子为空，中止")
        return 2

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("select column_name from information_schema.columns where table_schema='cfg'"
                    " and table_name='MSMA_WEAPONSET' order by ordinal_position")
        dbcols = [r[0] for r in cur.fetchall()]
        datacols = [c for c in dbcols if c != "_row_id"]
        if datacols != dbcols[1:] or len(datacols) != NCOL:
            print("✗ 库列不匹配：库 %d 列（除 _row_id）／ 期望 %d" % (len(datacols), NCOL))
            return 2

        cur.execute('select btrim(weapon_group_id), btrim(weapon_item_id) from cfg."MSMA_WEAPONSET"')
        currows = [(g, i) for g, i in cur.fetchall()]
        cur8 = {(g, i) for g, i in currows if len(i) == 8}
        cur9 = {(g, i) for g, i in currows if len(i) == 9}
        cur_groups = {g for g, _ in currows}

        cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
        d37 = {r[0] for r in cur.fetchall()}
        cur.execute('select distinct btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
        d36 = {r[0] for r in cur.fetchall()}
        cur.execute('select btrim(item_id) from cfg."ITEM"')
        item = {r[0] for r in cur.fetchall()}
        cur.execute('select distinct btrim(msma_id) from cfg."CHARA_PARAM"')
        units = {r[0] for r in cur.fetchall()}

    print()
    print("=== 真库现状 ===")
    print("  行 %d ／ 组 %d ／ 纯8位组 %d ／ 纯9位组 %d ／ 混装组 %d"
          % (len(currows), len(cur_groups),
             len({g for g, i in cur8} - {g for g, i in cur9}),
             len({g for g, i in cur9} - {g for g, i in cur8}),
             len({g for g, i in cur8} & {g for g, i in cur9})))

    print()
    print("=== 收敛后（= 种子）===")
    print("  行 %d → %d ／ 组 %d → %d" % (len(currows), len(seed), len(cur_groups), len(seed_groups)))
    print("  新增种子行（真武器被丢掉）      +%d" % len(set(seed_pairs) - set(currows)))
    print("  删除 8 位族行                  -%d" % len(cur8))
    print("  删除 9 位族里种子没有的行        -%d" % len(cur9 - set(seed_pairs)))

    lost = sorted({g for g, _ in cur8} - seed_groups)
    kept = sorted({g for g, _ in cur8} & seed_groups)
    print("  8 位族组：被种子接管 %d ／ ★失去武器组 %d" % (len(kept), len(lost)))
    print("  种子新覆盖的组 %d" % len(seed_groups - cur_groups))

    print()
    print("=== 自检（全部必须 ✓）===")
    checks = [
        ("种子武器全在 #37 有行", len(seed_ids - d37) == 0, "%d 个缺行" % len(seed_ids - d37)),
        ("种子武器全在 #36 有行", len(seed_ids - d36) == 0, "%d 个缺行" % len(seed_ids - d36)),
        ("种子武器全在 ITEM 有行", len(seed_ids - item) == 0, "%d 个缺行" % len(seed_ids - item)),
        ("种子组全在 CHARA_PARAM", len(seed_groups - units) == 0, "%d 个缺" % len(seed_groups - units)),
        ("收敛后 0 断引用",
         len({i for _, i in seed_pairs} - d37) == 0,
         "%d 个" % len({i for _, i in seed_pairs} - d37)),
        ("种子号全 9 位", all(len(i) == 9 for i in seed_ids), ""),
        ("槽位只有 MAIN/EX",
         {r[4] for _, r in seed if r[4]} <= {"MAIN", "EX"}, ""),
        ("col28 只有 CHINA", {r[28] for _, r in seed} <= {"CHINA", ""},
         str(sorted({r[28] for _, r in seed}))),
    ]
    ok = True
    for name, passed, extra in checks:
        print("  %s %-26s %s" % ("✓" if passed else "✗", name, extra))
        ok &= passed

    if lost:
        print()
        print("=== ★将失去武器组的 %d 台机体（种子解析不到 ⇒ 生成器故意留空）===" % len(lost))
        try:
            verdict = {}
            with open(BRIDGE, encoding="utf-8-sig") as fh:
                rd = csv.reader(fh)
                head = next(rd, None)
                gi = 0
                for i, h in enumerate(head or []):
                    if h.strip() in ("練度ID", "练度ID", "dev_id", "ID"):
                        gi = i
                        break
                for r in rd:
                    if len(r) > gi:
                        verdict[r[gi].strip()] = r[-1].strip()[:14]
        except Exception:
            verdict = {}
        for g in lost:
            print("   %s  %s" % (g, verdict.get(g, "(桥表无记录)")))
        print("  （当前这些组引用的武器已在上一轮净化中失去 #37 行 ⇒ 本来就是断引用）")

    if not apply:
        print()
        print("★ 干跑：加 --apply 写库（整表替换，先留全量回滚件）。")
        return 0 if ok else 1

    # ── 写库 ────────────────────────────────────────────────────────────────
    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(RB_DIR, "%s_MSMA_WEAPONSET_full.csv" % stamp)
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select %s from cfg."MSMA_WEAPONSET" order by _row_id'
                    % ", ".join('"%s"' % c for c in dbcols))
        allrows = cur.fetchall()
    with open(rb, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f)
        w.writerow(dbcols)
        w.writerows([["" if v is None else str(v) for v in r] for r in allrows])
    print()
    print("回滚件 → %s（%d 行 × %d 列，含 _row_id）"
          % (os.path.relpath(rb, ROOT), len(allrows), len(dbcols)))
    print("复原：COPY cfg.\"MSMA_WEAPONSET\" (%s) FROM '%s' WITH (FORMAT csv, HEADER true);"
          % (", ".join('"%s"' % c for c in dbcols), rb.replace("\\", "/")))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        try:
            cur.execute('delete from cfg."MSMA_WEAPONSET"')
            print("  已清空：%d 行" % cur.rowcount)
            sql = 'insert into cfg."MSMA_WEAPONSET" (_row_id, %s) values (%%s, %s)' % (
                ", ".join('"%s"' % c for c in datacols),
                ", ".join(["%s"] * NCOL))
            cur.executemany(sql, [(i + 1, *cols) for i, (_, cols) in enumerate(seed)])
            print("  已写入：%d 行（_row_id 1..%d，顺序 = 种子 CSV 顺序）" % (len(seed), len(seed)))

            cur.execute('select count(*), count(distinct btrim(weapon_group_id)),'
                        ' count(distinct btrim(weapon_item_id)) from cfg."MSMA_WEAPONSET"')
            n, ng, nu = cur.fetchone()
            cur.execute('select count(*) from cfg."MSMA_WEAPONSET"'
                        " where btrim(weapon_item_id) !~ '^[0-9]{9}$'")
            non9 = cur.fetchone()[0]
            cur.execute("""select count(*) from cfg."MSMA_WEAPONSET" m
                            where not exists (select 1 from cfg."WEAPON_SETTING" w
                                               where btrim(w.weapon_setting_id) = btrim(m.weapon_item_id))""")
            dangling = cur.fetchone()[0]
            if (n, ng, nu, non9, dangling) != (len(seed), len(seed_groups), len(seed_ids), 0, 0):
                raise AssertionError("写后自检不过：行%d 组%d 武器%d 非9位%d 断引用%d"
                                     % (n, ng, nu, non9, dangling))
            print("  写后自检：行 %d ／ 组 %d ／ 武器 %d ／ 非9位 %d ／ 断引用 %d  ✓"
                  % (n, ng, nu, non9, dangling))
            conn.commit()
            print("★ 已提交")
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

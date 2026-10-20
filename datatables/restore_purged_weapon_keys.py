# -*- coding: utf-8 -*-
"""restore_purged_weapon_keys.py —— 把 `purge_unreachable_weapon_keys.py` **误删**的武器行灌回去。

═══════════════════════════ 为什么会有这一步 ═══════════════════════════
2026-10-04 那次 purge 的键域判定**两侧尺子不一致**：
  · 候选键来自库/CSV，是 `store.FormatItemKey` 的**规范形**（`02840151` / `01010401`）；
  · 可达号域与「现役引用」来自 `game.ms_rokaku.eqweapon_itemid`(int) 与 `msma_weapon_set`
    的**裸数**（`2840151` / `1010401`）；
  · 判定却用了 `k in ok or k.lstrip('0') in ok`：`'02840151'.lstrip('0') = '2840151'` 落在
    可达域**之外**，兜底的 `k in ref` 又因为 `'02840151' != '2840151'` 没兜住
    ⇒ 规范化形整族被判「不可达」删掉（#36 845 键/3575 行、#37 848 键/848 行）。

后果（`serverv/logs/msgoser.log` 实测）：
  `[battle] 武器表就位：1630 把武器（POWER 1628 / RANGE 1477 / RAPIDDELAY 528）`
  1630 = 只有 9 位 sidecar 那族。玩家实际出击的 6 把武器
  （2840151 / 4840201 / 2841701 / 2711603 / 1010401 / 3010101）全不在表里
  ⇒ `LoadWeaponBattleParams` 回 `ok=false` ⇒ `HasPower=false`、`Range=0`、`RapidDelay=0`
  ⇒ 命中不回 HP、T4/T5 全废。

═══════════════════════════ 本脚本做什么 ═══════════════════════════
**只回灌「用修好的尺子（`norm_key`）判为可达」的键**——不是无脑整份还原：
  · 在役/在库武器（`norm_key(k) ∈ 可达号域 ∪ 现役引用`）⇒ 回灌；
  · `10101/10102…` 模板块、`02012401…` 图标号族、错列残渣 ⇒ **继续留在删除状态**
    （它们确实是「身份不是武器」，purge 那一步判断没错，错的是把规范形武器一起删了）。
落点：
  1. `cfg."WEAPON_BATTLE_DETAIL"` / `cfg."WEAPON_SETTING"`（从 `_rollback/*_purge*_rows.csv`）；
  2. `server/datafiles/lounge/item/weapon_battle_detail.csv` / `weapon_settings.csv`
     —— **CSV 是播种输入**，不回补则下次重播种又丢。补的行从回滚件转出（键转源形，
     与表里其它短号 `1040101/1040201` 同一写法），只补「整键缺席」的武器。
幂等：库侧 `WHERE NOT EXISTS(自然键)`，CSV 侧按规范形键去重；重复跑不会加行。

用法：
  python restore_purged_weapon_keys.py            # 干跑（事务内做完所有写入再回滚）
  python restore_purged_weapon_keys.py --apply    # 真写
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import psycopg  # noqa: E402

# ★注：`purge_unreachable_weapon_keys` 在导入时自己会重包 `sys.stdout`（UTF-8）。
#   这里不能再包一层——两个 wrapper 抢同一个 buffer，先建的那个被 GC 时会把 buffer 关掉。
from purge_unreachable_weapon_keys import (  # noqa: E402
    DF, DSN, RB_DIR, TARGETS, norm_key, rd, legit_ids, refs_from_live,
)

STAMP = "20261004_234510"          # 那次误删的时间戳（回滚件/备份同戳）
# ItemKeyExpr 的 SQL 孪生（`serverv/internal/store/itemkey.go`）——读侧同尺子
PAD = ("CASE WHEN btrim((%s)::text) ~ '^[0-9]{1,8}$' "
       "THEN lpad(btrim((%s)::text), 8, '0') ELSE btrim((%s)::text) END")
HAND = {"02840151", "04840201", "02841701", "02711603", "01010401", "03010101",
        "2840151", "4840201", "2841701", "2711603", "1010401", "3010101"}


def pad(expr):
    return PAD % (expr, expr, expr)


def rollback_path(tag):
    return os.path.join(RB_DIR, "%s_purge%s_rows.csv" % (STAMP, tag.lstrip("#")))


def load_rollback(tag):
    """回滚件 -> (可回灌行 list[dict], 判残渣键 set, 全键 set, 键列名)"""
    p = rollback_path(tag)
    if not os.path.exists(p):
        raise SystemExit("缺回滚件：%s" % p)
    with open(p, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    kc = "weapon_id_key" if tag == "#36" else "weapon_setting_id"
    ok, ref = legit_ids(), refs_from_live()
    good, junk = [], set()
    for r in rows:
        k = (r[kc] or "").strip()
        if k.isdigit() and norm_key(k) not in ok and norm_key(k) not in ref:
            junk.add(k)
        else:
            good.append(r)
    return good, junk, {(r[kc] or "").strip() for r in rows}, kc


def raw_key(k):
    """规范形 -> 源形（`02840151` -> `2840151`）。

    为什么要转：库里/CSV 里**短号的通行写法是源形**（同表另有 `1040101`、`1040201`），
    补零形是旧管线留下的孤例。读侧两侧都过 `ItemKeyExpr`/`norm_key`，两种都认；
    统一成源形 ⇒ 一个武器号在库里只有一行，DB 与 CSV 也逐字一致（重播种不会分叉）。
    """
    return str(int(k)) if k.isdigit() and 0 < int(k) < 100_000_000 else k


def db_restore(tag, good, kc, apply_):
    """COPY 进临时表 -> INSERT ... WHERE NOT EXISTS(自然键)。返回 (插入行数, 该键域现存键数)。"""
    tbl = dict((t, tb) for t, tb, _c, _f, _k in TARGETS)[tag]
    cols = [c for c in good[0].keys() if c != "_row_id"]
    keys = sorted({norm_key((r[kc] or "").strip()) for r in good})   # ★入参也要过尺子
    nat_t, nat_s = (("(btrim(t.attr_name), btrim(t.weapon_id_key))",
                     "(btrim(s.attr_name), btrim(s.weapon_id_key))") if tag == "#36"
                    else ("(btrim(t.weapon_setting_id))", "(btrim(s.weapon_setting_id))"))
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TEMP TABLE stg (LIKE cfg.%s) ON COMMIT DROP' % tbl)
        cur.execute("ALTER TABLE stg ALTER COLUMN _row_id DROP NOT NULL")
        with cur.copy("COPY stg (%s) FROM STDIN" % ",".join(cols)) as cp:
            for r in good:
                cp.write_row([raw_key((r[c] or "").strip()) if c == kc else (r.get(c) or "")
                              for c in cols])
        cur.execute('INSERT INTO cfg.%s (%s) SELECT %s FROM stg s '
                    'WHERE NOT EXISTS (SELECT 1 FROM cfg.%s t WHERE %s = %s)'
                    % (tbl, ",".join(cols), ",".join(cols), tbl, nat_t, nat_s))
        ins = cur.rowcount
        # ★两侧同尺子：列侧 pad()，入参侧 norm_key()。只归一一边就是本次误删的成因。
        cur.execute('SELECT count(distinct %s) FROM cfg.%s WHERE %s = ANY(%%s)'
                    % (pad(kc), tbl, pad(kc)), (keys,))
        now = cur.fetchone()[0]
        conn.rollback() if not apply_ else conn.commit()
    return ins, now


def csv_plan(fn, kc, good, kcol):
    """现 CSV 里**整键缺席**的可达武器 -> 用回滚件的行补上（键转源形）。"""
    p = os.path.join(DF, fn)
    cur_rows = rd(p)
    have_norm = {norm_key(r[kc].strip()) for r in cur_rows
                 if len(r) > kc and r[kc].strip().isdigit()}
    cols = [c for c in good[0].keys() if c != "_row_id"]
    want = {norm_key((r[kcol] or "").strip()) for r in good
            if norm_key((r[kcol] or "").strip()) not in have_norm}
    add = [[raw_key((r[c] or "").strip()) if c == kcol else (r.get(c) or "") for c in cols]
           for r in good if norm_key((r[kcol] or "").strip()) in want]
    return add, cur_rows, cols, sorted(want)


def main():
    apply_ = "--apply" in sys.argv
    ok, ref = legit_ids(), refs_from_live()
    print("尺子 norm_key = FormatItemKey（0<n<1e8 ⇒ %%08d）；可达号域 %d + 现役引用 %d；干跑=%s"
          % (len(ok), len(ref), not apply_))
    print()
    for tag, _tbl, _col, fn, kc in TARGETS:
        good, junk, allk, kcol = load_rollback(tag)
        keys = sorted({(r[kcol] or "").strip() for r in good})
        print("%s  回滚件 %d 键 -> 归一化后可达 %d 键 / %d 行；判残渣仍留删 %d 键"
              % (tag, len(allk), len(keys), len(good), len(junk)))
        print("     在役 6 把落在回灌集里：%s" % sorted(k for k in keys if k in HAND))
        ins, now = db_restore(tag, good, kcol, apply_)
        print("     库  INSERT 命中 %d 行；该键域现存 %d 键（唯一的）" % (ins, now))
        add, cur_rows, _cols, want = csv_plan(fn, kc, good, kcol)
        print("     CSV %-26s 现 %5d -> +%-4d = %5d 行（补 %d 个整键缺席的武器）"
              % (fn, len(cur_rows), len(add), len(cur_rows) + len(add), len(want)))
        if want:
            print("       缺席键：%s" % want)
        if apply_ and add:
            p = os.path.join(DF, fn)
            head = [r for r in cur_rows if r and r[0].lstrip("\ufeff").startswith("#")]
            body = [r for r in cur_rows if r and not r[0].lstrip("\ufeff").startswith("#")]
            with open(p, "wb") as f:
                f.write(("\r\n".join(",".join(r) for r in head + body + add) + "\r\n")
                        .encode("utf-8"))
            b = open(p, "rb").read()
            print("       落盘方言%s（%d 行）"
                  % ("OK" if (not b.startswith(b"\xef\xbb\xbf")) and
                     b.replace(b"\r\n", b"").find(b"\n") < 0 else "FAIL",
                     len(head) + len(body) + len(add)))
        print()
    print("★ 干跑结束（未落盘）。加 --apply 执行。" if not apply_ else "★ 完成")


if __name__ == "__main__":
    main()

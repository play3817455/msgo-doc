# -*- coding: utf-8 -*-
"""fix_rapid_delay_units.py —— 把 #36 的 `RAPIDDELAY`/`COOLTIME` 两族收敛到**客户端原值刻度**。

═══════════════════════════ 病（2026-10-05 取证）═══════════════════════════
`#36 RAPIDDELAY`（词表第 4 项，wiki「連射速度」栏）在真库里**混了三种刻度**，1237 行：

| 档 | 行数 | 值域样例 | 真伪 |
|---|---|---|---|
| ① 客户端原值 | 709 | `0.110657 … 0.399457`、`1.391257`、`1.999257` | ★**真值** = `weapon_client_raw.rapid_raw(wiki 連射速度)` **709/709 精确命中** |
| ② 白字刻度 | ~470 | `1480 / 1466 / 1484 / 1421 / 1170 / 1230` | 旧管线把 wiki **显示值**直接写进了原值列 |
| ③ 错列残渣 | ~58 | `200 / 300 / 360 / 600 / 720 / 4167 / 5000`、负数 | 别列串入（射程 col13 / 装填 col14 / 锁定期 col16 / 效果范围 col19） |

`COOLTIME`（词表第 5 项，客户端与 `RAPIDDELAY` **同值**，`sub_59A070` 两个子表）同样混了三种，
且残渣里有 **-4.334086** 这种负数。

═══ 危害（为什么必须修，两个方向都坏）═══
读侧 `serverv/internal/store/battle_params.go` 原先用 `cfgU32` 解析（**四舍五入到整数**）：

  · ①真值 `0.124590` ⇒ `cfgU32` ⇒ **0** ⇒ `RapidDelay == 0` ⇒ §6.3 **T5 冷却完全不校验**
    ——**709 行真值全军覆没**，等于服务端对连射完全放行。
  · ③残渣 `720` ⇒ 白字刻度当成原值 ⇒ `shotIntervalFrames(720)` ⇒ 66 帧 ⇒ 1.1 s 冷却
    ⇒ 一把 0.13 s 间隔的速射武器**每一发都被判 CDEarly**，而 `CDEarly` 是
    **整包判 Miss**（`authority.go::onFireRegister`）⇒ **合法玩家输出被打掉**。

⇒ 一松一紧同时发生：真值不判、脏值误杀。

═══ 口径（权威 + 判据）═══
权威 = `names/武器分配明细.csv` col12「连射速度」（doc §4 明写：数值全部出自这张 sidecar），
换算唯一出口 = `weapon_client_raw.rapid_raw()`；「原值域」判据 = `rapid_is_raw_domain()`。

处理：
  · 键在 sidecar 且 col12 非空 ⇒ **重写** `RAPIDDELAY = COOLTIME = rapid_raw(col12)`（幂等）。
  · 键不在 sidecar 但现值已在原值域内 ⇒ **保留**（现役短号；无来源可查，但不越刻度 ⇒ 不删）。
  · 其余（白字刻度 / 错列 / 负数 / 非数字）⇒ **删除**该行：`冷却未知 ⇒ 不校验 T5`，
    这是 §6.3 的缺省纪律，比"拿脏值误杀"正确。

用法：
  python fix_rapid_delay_units.py            # 干跑
  python fix_rapid_delay_units.py --apply    # 写库 + 改 CSV（各留 .bak_rapid* 与回滚件）

★与生成器同步：`gen_weapon_tables_wiki.py` 已改成对这两族**重写**（先删后并），
  并加了原值域口径哨 ⇒ 本脚本修完不会再被下一次生成污染回去。
"""
import csv
import datetime
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".codebuddy"))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
T36 = os.path.join(DF, "weapon_battle_detail.csv")
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

TBL = '"WEAPON_BATTLE_DETAIL"'
# ★这两族同源（`sub_59A070` 两个子表同值，`weapon_client_raw.COOLTIME_TWIN`）
FAMILY = ("RAPIDDELAY", "COOLTIME")
ATTRS = tuple(FAMILY)


def rd(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


def norm_key(k):
    """物品号规范形 —— 与运行时 `store.FormatItemKey` 逐字一致（`0<n<1e8 ⇒ %08d`）。"""
    k = str(k).strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


def sidecar_rapid():
    """{规范形键: 连射速度(int)} —— #36 该两项的**唯一权威出处**。"""
    out = {}
    for r in rd(SIDE)[1:]:
        if len(r) <= 12 or not r[1].strip():
            continue
        t = RAW.first_tier(r[12])
        if t:
            out[norm_key(r[1])] = int(float(t))
    return out


def read_db():
    """[(键, 属性名, 值, _row_id)] —— 两族的全部现存行。"""
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), _row_id '
                    'from cfg.%s where btrim(attr_name) = any(%%s) order by _row_id' % TBL,
                    (list(ATTRS),))
        return cur.fetchall()


def plan(db_rows, src):
    """→ (set_rows, keep_rows, del_row_ids, pinned_keys, stat)

    set_rows : [(键, 属性名, 新值字符串)]  要写成 `rapid_raw(col12)`
    del_row_ids : [int]                    要删的行（`_row_id`）
    """
    by_key = {}
    for k, attr, val, rid in db_rows:
        by_key.setdefault(norm_key(k), []).append((attr, val, rid))

    set_rows, del_ids, pinned = [], [], set()
    stat = {"rewrite": 0, "insert": 0, "keep": 0, "drop_rows": 0, "dedup": 0, "dup_keys": set()}
    for k, rows in by_key.items():
        if k in src:
            want = RAW.rapid_raw(src[k])
            present = {}
            for attr, val, rid in rows:
                present.setdefault(attr, []).append((val, rid))
            for attr in ATTRS:
                vals = present.get(attr, [])
                if not vals:
                    set_rows.append((k, attr, want))
                    stat["insert"] += 1
                    continue
                first = True
                for val, rid in vals:
                    if first and val == want:
                        first = False
                        continue
                    if first:
                        # 现值不对 ⇒ 用 REPLACE 原地改（见 apply_db），这里只登记
                        set_rows.append((k, attr, want))
                        stat["rewrite"] += 1
                        first = False
                        continue
                    del_ids.append(rid)          # 同键重复行
                    stat["dedup"] += 1
            # 不在两族里的行（理论上没有）不动
            continue
        # 无 sidecar 来源：只看 RAPIDDELAY 现值是否已在原值域内
        rap = [v for a, v, _r in rows if a == "RAPIDDELAY"]
        if rap and all(RAW.rapid_is_raw_domain(v) for v in rap):
            pinned.add(k)
            stat["keep"] += len(rows)
            # COOLTIME 必须与 RAPIDDELAY 同值（客户端两个子表同值）
            cool = [v for a, v, _r in rows if a == "COOLTIME"]
            if not cool:
                set_rows.append((k, "COOLTIME", rap[0]))
                stat["insert"] += 1
            continue
        for _a, _v, rid in rows:
            del_ids.append(rid)
            stat["drop_rows"] += 1
    return set_rows, sorted(by_key), del_ids, pinned, stat


def apply_db(set_rows, del_ids, apply_):
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        n_del = 0
        if del_ids:
            cur.execute('delete from cfg.%s where _row_id = any(%%s)' % TBL, (del_ids,))
            n_del = cur.rowcount
        # 先删同自然键的旧行，再插（= 重写语义；表上没有自然键唯一约束，不能靠 upsert）
        n_set = 0
        for k, attr, val in set_rows:
            cur.execute('delete from cfg.%s where btrim(attr_name) = %%s '
                        'and btrim(weapon_id_key) = %%s' % TBL, (attr, k))
            cur.execute('insert into cfg.%s (attr_name, weapon_id_key, attr_value, attr_value_2) '
                        'values (%%s, %%s, %%s, %s)' % (TBL, "''"), (attr, k, val))
            n_set += 1
        conn.rollback() if not apply_ else conn.commit()
    return n_del, n_set


def fix_csv(src, apply_, pinned_vals):
    """CSV 侧同一规则：这两族**整族重写**，并按 sidecar 补齐缺席的键。

    `pinned_vals` = {键: RAPIDDELAY 现值}：库侧判定「无 sidecar 来源但在原值域」而保留的
    现役短号。**两族都**按这个集合原样保留（`RAPIDDELAY`/`COOLTIME` 同值，不能只留一半），
    缺的族按该值补齐 —— 否则 CSV↔库 会漂。
    """
    rows = rd(T36)
    head = [r for r in rows if r and r[0].lstrip("\ufeff").startswith("#")]
    body = [r for r in rows if r and not r[0].lstrip("\ufeff").startswith("#")]
    out, dropped, kept_pin = [], 0, set()
    have = set()
    for r in body:
        attr = r[0].strip()
        if attr not in ATTRS:
            out.append(r)
            continue
        k = norm_key(r[1].strip() if len(r) > 1 else "")
        have.add((k, attr))
        if k in src:
            out.append([attr, r[1].strip(), RAW.rapid_raw(src[k]), ""])
            continue
        if k in pinned_vals:
            out.append(r)          # 现役短号：两族都原样留（值不可改）
            kept_pin.add(k)
            continue
        dropped += 1
    add = []
    for k, w in sorted(src.items()):
        for attr in ATTRS:
            if (k, attr) not in have:
                add.append([attr, k, RAW.rapid_raw(w), ""])
    # 现役短号：以**库侧保留下来的值**为准，缺哪一族就补哪一族
    for k in sorted(pinned_vals):
        v = pinned_vals[k]
        for attr in ATTRS:
            if (k, attr) not in have:
                add.append([attr, k, v, ""])
    if apply_:
        bak = T36 + ".bak_rapid" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if os.path.exists(T36) and not os.path.exists(bak):
            os.replace(T36, bak)
        with open(T36, "wb") as f:
            f.write(("\r\n".join(",".join(r) for r in head + out + add) + "\r\n").encode("utf-8"))
        b = open(T36, "rb").read()
        dialect = (not b.startswith(b"\xef\xbb\xbf")) and (b.replace(b"\r\n", b"").find(b"\n") < 0)
        print("  CSV 落盘：保留 %d + 新增 %d = %d 行（清掉 %d）方言%s；原件 %s"
              % (len(out), len(add), len(out) + len(add), dropped,
                 "OK" if dialect else "FAIL", os.path.basename(bak)))
    else:
        print("  CSV 计划：保留 %d + 新增 %d = %d 行（清掉 %d）"
              % (len(out), len(add), len(out) + len(add), dropped))
    return len(out), len(add), dropped, sorted(kept_pin)


def main():
    apply_ = "--apply" in sys.argv
    src = sidecar_rapid()
    db_rows = read_db()
    print("权威 sidecar col12「连射速度」：%d 个键（换算唯一出口 weapon_client_raw.rapid_raw）"
          % len(src))
    print("#36 两族现存 %d 行（RAPIDDELAY %d / COOLTIME %d）"
          % (len(db_rows), sum(1 for r in db_rows if r[1] == "RAPIDDELAY"),
             sum(1 for r in db_rows if r[1] == "COOLTIME")))
    print()
    set_rows, all_keys, del_ids, pinned, stat = plan(db_rows, src)
    print("计划：")
    print("  重写为 rapid_raw(col12) : %4d 行" % stat["rewrite"])
    print("  补齐缺席行              : %4d 行" % stat["insert"])
    print("  保留（无来源但在原值域）: %4d 键 -> %s" % (len(pinned), sorted(pinned)))
    print("  删除（白字刻度/错列/负）: %4d 行" % stat["drop_rows"])
    print("  同键重复行清理          : %4d 行" % stat["dedup"])
    print()
    after = {}
    for k, attr, val in set_rows:
        after[(k, attr)] = val
    del_set = set(del_ids)
    kept = {}
    for k, attr, val, rid in db_rows:
        if rid in del_set:          # 已在删除表里 ⇒ 修完不存在，别再把残渣算进来
            continue
        key = (norm_key(k), attr)
        if key not in after:
            kept[key] = val
    allvals = dict(kept)
    allvals.update(after)
    rap_after = {k: v for (k, a), v in allvals.items() if a == "RAPIDDELAY"}
    bad = {k: v for k, v in rap_after.items() if not RAW.rapid_is_raw_domain(v)}
    print("★口径哨：修完 RAPIDDELAY %d 个键，域外 %d 个 %s"
          % (len(rap_after), len(bad), bad if bad else "✓"))
    disp = sorted(RAW.rapid_display(v) for v in rap_after.values() if RAW.rapid_display(v))
    if disp:
        print("  换算后的「連射速度」白字域：%d .. %d（%d 个键；0 = 不校验 T5，另有 %d 个）"
              % (disp[0], disp[-1], len(disp), len(rap_after) - len(disp)))
    if bad:
        raise SystemExit("拒绝写入：还有域外的 RAPIDDELAY")

    print()
    pinned_vals = {norm_key(k): v for k, a, v, _r in db_rows
                   if norm_key(k) in pinned and a == "RAPIDDELAY"}
    if not apply_:
        fix_csv(src, False, pinned_vals)
        print()
        print("★ 干跑结束（未落库/未落盘）。加 --apply 执行。")
        return

    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(RB_DIR, "36_rapid_%s_rows.csv" % stamp)
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('select _row_id, attr_name, weapon_id_key, attr_value, attr_value_2 '
                    'from cfg.%s where btrim(attr_name) = any(%%s)' % TBL, (list(ATTRS),))
        with open(rb, "w", encoding="utf-8", newline="\n") as f:
            w = csv.writer(f)
            w.writerow([d.name for d in cur.description])
            w.writerows(cur.fetchall())
    print("  回滚件 %s（两族全量，表头齐全，可直接 copy 重灌）" % os.path.relpath(rb, ROOT))

    n_del, n_set = apply_db(set_rows, del_ids, True)
    print("  库：删 %d 行 / 重写+补 %d 行" % (n_del, n_set))
    ao, add, dropped, pinned2 = fix_csv(src, True, pinned_vals)
    print("  CSV：保留 %d + 新增 %d（清掉 %d，保留现役短号 %s）" % (ao, add, dropped, pinned2))
    print()
    print("★ 完成。下一步：`python gen_weapon_tables_wiki.py`（口径哨会复查越域键）")
    print("  并重启服务端看 `[battle] 武器表就位` 那行的 RAPIDDELAY 计数。")


if __name__ == "__main__":
    main()

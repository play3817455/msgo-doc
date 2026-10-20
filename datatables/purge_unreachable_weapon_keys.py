# -*- coding: utf-8 -*-
"""purge_unreachable_weapon_keys.py —— 把 #36/#37 收敛到「武器链真正可达的号域」。

═══════════════════════ 证据（取证脚本：_audit_*.py / _probe_*.py）═══════════════════════
可达号域 = 9 位 sidecar 武器号(1625) ∪ 客户端 weapon_wrestle.csv 的 8 个近战短号
  ① 客户端自带 `unpackdat/settings/weapon_visual_customize.csv`，表头第 1 列就是
     `#武器ID`，45 行**全是 9 位**（例 214607001=Vガンダム / 224607001=ガンイージ）；
     客户端 9 位号 ∩ sidecar = 7 命中 ⇒ 9 位族是客户端真域。
  ② 客户端自带 `weapon_wrestle.csv`（表头 `アイテムID`）**只有 8 行**，短号里唯一的真域。
  ③ 现役 `msma_weapon_set.csv`（服务端下发，sub_587160 / CMSMAWeaponSetTable）
     1625 行，**col2 = 武器号，全是 9 位**；短号只出现在 .bak 里。
  ④ **修正（2026-10-04 晚）**：原先「10 条归一化规则对短号 0% 命中 ⇒ 短号不是合法号」
     的结论**是错的**——漏掉了运行时唯一那条规则 `store.FormatItemKey`：`0<n<1e8`
     ⇒ `%08d`。库里的 `02840151`、`1010401` 原本就是 `2840151`、`01010401` 的规范形，
     两边是同一把武器。见 `norm_key()` 的注释。

不可达键的来源（考古结论，不是「值写坏」而是「身份不是武器」）：
  · 图标号族：`gow_wiki/data/weapon_icon_match.json` 的 `icon_id`（8 位，如
    02012401=ビーム・ショット・ライフル、02600151=腹部メガ粒子砲）—— 有正规日文名，
    但 **sidecar 781 个武器名里 0 命中** ⇒ 无真值来源；其中 6 把 POWER 被写成 2/6/9/11/12/13。
    ★注意：8 位图标号与「7 位武器号补零后的规范形」**同形**，不能靠形状区分，只能靠
    `norm_key(k) ∈ 可达号域 ∪ 现役引用` 判定（现役引用兜住了所有真正在用的武器）。
  · 模板块：`10101 / 10102 / 10103 / 10111 …`（5 位，成块递增，同字段全同）。
  · 旧轮转抓取错列残渣。

处理原则：
  · `#36 WEAPON_BATTLE_DETAIL` / `#37 WEAPON_SETTING`：**只保留可达号域** + 现役被引用的键。
    这两张表是「武器战斗数值」，键必须是武器号；不可达键的作用只剩**把 TTK 哨踩响**。
  · `#78 ITEM`：**不动**。它是 名称/图标 注册表，里面那些 8 位图标号行带真名真图
    （本仓库曾专门为武器图标补过 item.csv），删了会丢图标绑定；且不影响任何哨。
  · 遵守 `docs/battle-client-fsm.mdc`：不靠猜补包、不动 `spawn1st_post` 之类；本脚本只动 cfg 数据。

用法：
  python purge_unreachable_weapon_keys.py            # 干跑
  python purge_unreachable_weapon_keys.py --apply    # 写库 + 清 CSV（各留一份 .bak_purge*）
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
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
MSMA = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
CLIENT = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings")
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
KEEP_LIST = os.path.join(HERE, "names", "可达武器号域.csv")
RB_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# (标签, cfg 表名, 键列, CSV 文件名, CSV 键列)
TARGETS = [("#36", '"WEAPON_BATTLE_DETAIL"', "weapon_id_key",
            "weapon_battle_detail.csv", 1),
           ("#37", '"WEAPON_SETTING"', "weapon_setting_id",
            "weapon_settings.csv", 0)]


def rd(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


def norm_key(k):
    """物品号规范形 —— 必须与运行时的 `store.FormatItemKey` 逐字一致。

    `FormatItemKey`（`serverv/internal/store/itemkey.go`）对 `0 < n < 1e8` 一律写成
    `%08d`。库里的 `02840151` 与线上 u32 `2840151` 是**同一把武器**；而现役引用
    （`game.ms_rokaku.eqweapon_itemid` 是 int 列，取出来是 `2840151`）**不带补零**。
    ⇒ 只要两侧不过同一把尺子，`02840151` 就会被判成「不可达」而删掉，
    正是 2026-10-04 那次误删（845 键 / 3575 行，含 6 把在役武器）的成因。
    """
    k = k.strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


def legit_ids():
    """可达号域 = sidecar col1（9 位武器号）∪ 客户端 weapon_wrestle.csv col0（近战短号）

    出口一律是**规范形**（`norm_key`），下游比较也必须先过 `norm_key`。
    """
    ok = {norm_key(r[1]) for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
    for r in rd(os.path.join(CLIENT, "weapon_wrestle.csv")):
        v = r[0].strip().lstrip("\ufeff")
        if v.isdigit():
            ok.add(norm_key(v))
    return ok


def is_legit(k, ok):
    """`ok` 必须是 `legit_ids()` 的规范形出口。"""
    return norm_key(k) in ok


def refs_from_live():
    """现役引用（这些即便不可达也保留，宁留不误删）：msma_weapon_set col2 ∪ unlockw ∪ ms_rokaku

    ★出口过 `norm_key`：`eqweapon_itemid` / `item_id` 是 int 列，取出来是裸数
    （`2840151`），不归一就会和库里的 `02840151` 擦肩而过。
    """
    ref = set()
    for r in rd(MSMA):
        if r[0].lstrip("\ufeff").startswith("#"):
            continue
        if len(r) > 2 and r[2].strip().isdigit():
            ref.add(r[2].strip())
    conn = psycopg.connect(DSN)
    cur = conn.cursor()
    for sql in ("select distinct btrim(item_id::text) from game.unlockw",
                "select distinct btrim(eqweapon_itemid::text) from game.ms_rokaku"):
        try:
            cur.execute(sql)
            ref |= {k for (k,) in cur.fetchall() if k}
        except Exception as e:
            conn.rollback()
            print("  （引用检查跳过：%s）" % str(e).splitlines()[0][:70])
    conn.close()
    return {norm_key(k) for k in ref if k.isdigit()}


def main():
    apply = "--apply" in sys.argv
    ok = legit_ids()
    ref = refs_from_live()
    print("可达武器号域 %d 个（sidecar 9 位 + 客户端近战 8 号）" % len(ok))
    print("现役引用 %d 个（即便不可达也保留）" % len(ref))
    print()

    # ★把「允许键域」落盘：`gen_weapon_tables_wiki.py` 的口径哨读它（两边共用同一份权威）
    #   出口是**规范形**：读侧一律先过 `norm_key` 再比，`02840151` 与 `2840151` 都认。
    os.makedirs(os.path.dirname(KEEP_LIST), exist_ok=True)
    melee = ok - {norm_key(r[1]) for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
    with open(KEEP_LIST, "w", encoding="utf-8", newline="") as f:
        f.write("#允许武器号(规范形),来源  （由 purge_unreachable_weapon_keys.py 生成，勿手改）\r\n")
        for k in sorted(ok):
            f.write("%s,%s\r\n" % (k, "客户端近战" if k in melee else "sidecar9"))
        for k in sorted(ref - ok):
            f.write("%s,现役引用\r\n" % k)
    print("允许键域 %d 个 -> %s"
          % (len(ok) + len(ref - ok), os.path.relpath(KEEP_LIST, ROOT)))
    print()

    conn = psycopg.connect(DSN)
    cur = conn.cursor()
    plan = {}
    for tag, tbl, col, fn, kc in TARGETS:
        cur.execute('select distinct btrim(%s) from cfg.%s where btrim(%s) ~ \'^[0-9]+$\''
                    % (col, tbl, col))
        keys = [k for (k,) in cur.fetchall()]
        bad = [k for k in keys if not is_legit(k, ok)]
        guarded = [k for k in bad if norm_key(k) in ref]
        drop = [k for k in bad if norm_key(k) not in ref]
        plan[tag] = (drop, guarded, keys)
        print("%s 现存键 %5d | 可达 %5d | 不可达 %4d | 其中现役引用保留 %2d | **将删 %4d**"
              % (tag, len(keys), len(keys) - len(bad), len(bad), len(guarded), len(drop)))
        if guarded:
            print("     保留清单: %s" % sorted(guarded))
    print()
    print("#78 ITEM：**不动**（名称/图标注册表；图标号族带真名真图，删了丢图标绑定）")

    if not apply:
        print()
        print("★ 干跑：将删 #36 %d 键 / #37 %d 键（行数见执行时）。加 --apply 执行。"
              % (len(plan["#36"][0]), len(plan["#37"][0])))
        conn.close()
        return

    os.makedirs(RB_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for tag, tbl, col, fn, kc in TARGETS:
        ids = plan[tag][0]
        rb = os.path.join(RB_DIR, "%s_purge%s_rows.csv" % (stamp, tag.lstrip("#")))
        if ids:
            cur.execute('select * from cfg.%s where btrim(%s) = any(%%s)' % (tbl, col), (ids,))
            cols = [d.name for d in cur.description]
            with open(rb, "w", encoding="utf-8", newline="\n") as f:
                w = csv.writer(f)
                w.writerow(cols)
                w.writerows(cur.fetchall())
        print("  回滚件 %s（%d 键，表头齐全，可直接 copy 重灌）"
              % (os.path.relpath(rb, ROOT), len(ids)))

    for tag, tbl, col, fn, kc in TARGETS:
        ids = plan[tag][0]
        if not ids:
            continue
        cur.execute('delete from cfg.%s where btrim(%s) = any(%%s)' % (tbl, col), (ids,))
        print("  删除 %s：%d 个键 / %d 行" % (tag, len(ids), cur.rowcount))
    conn.commit()
    conn.close()

    for tag, tbl, col, fn, kc in TARGETS:
        p = os.path.join(DF, fn)
        rows = rd(p)
        if not rows:
            continue
        # ★CSV 用**同一号域规则**独立判定（CSV 的键集与库不同源，不能拿库的删除集套）
        out, dropped, kept_short = [], 0, []
        for r in rows:
            if r[0].lstrip("\ufeff").startswith("#"):
                out.append(r)
                continue
            k = r[kc].strip() if len(r) > kc else ""
            if k.isdigit() and not is_legit(k, ok):
                if norm_key(k) in ref:
                    kept_short.append(k)
                else:
                    dropped += 1
                    continue
            out.append(r)
        bak = p + ".bak_purge" + stamp
        os.replace(p, bak)
        with open(p, "wb") as f:
            f.write(("\r\n".join(",".join(r) for r in out) + "\r\n").encode("utf-8"))
        b = open(p, "rb").read()
        dialect = (not b.startswith(b"\xef\xbb\xbf")) and (b.replace(b"\r\n", b"").find(b"\n") < 0)
        print("  CSV %-28s 保留 %6d 行（清掉 %5d，保留现役引用 %d）方言%s 原件 %s"
              % (fn, len(out), dropped, len(kept_short), "OK" if dialect else "FAIL",
                 os.path.basename(bak)))
    print("★ 完成")


if __name__ == "__main__":
    main()
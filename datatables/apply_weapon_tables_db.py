# -*- coding: utf-8 -*-
"""apply_weapon_tables_db.py —— 把 `server/datafiles/lounge/item/` 的三张武器表灌进真库。

为什么需要它
============
`cfgsync -bootstrap-csv` 只在**空表**时导入；`-recreate` 会 DROP 整表（连带丢掉库里
其它 id 家族的行）。本脚本做**按键 upsert**：只动「真实武器 id」（= `names/武器分配明细.csv`
里那 1628 个 `2+練度ID[1:5]+sub4`），不碰历史遗留 id 家族的行。

写什么
======
| 表 | 动作 |
|---|---|
| `cfg."WEAPON_BATTLE_DETAIL"`(#36) | 对 CSV 里每个 `(属性名, 武器ID)`：删旧行 + 插新行（含 `attr_value_2`） |
| ↑ 同上 | ★**整族重写**（2026-10-05）：真武器号 × `weapon_client_raw.FAMILIES_36` 里，
|   | CSV 没有的行一律删（= 把生成器那侧的 purge 镜像到库里）。不删的话，"CSV 里已净化、
|   | 库里还留着"的残渣永远存续：C4 实测 STABILITY 150 / RELOAD 22 / HIGH_LOCKON 207 /
|   | RANGE 19 / LOCKON_CAM 13 行是**面板刻度直写或错列映射**（如诱导距离→HIGH_LOCKON） |
| `server/datafiles/.../weapon_battle_detail.csv` | ★**管理域外回灌**（2026-10-05）：见下 §口径 |
| `cfg."WEAPON_SETTING"`(#37)      | 禁用旧col14弹数投影；col14是动作层，弹数由serverv/tools/repair_runtime_ammo.py核对wiki后独立写入col104/105 |
| `cfg."ITEM"`(#78)                | 缺失才插（名称 / `item_type='WEAPON'`） |

口径：两个 id 家族、两个权威（★C4 收尾时定案）
=============================================
`#36` 里同时住着两族键，**各有各的出处**，本脚本按族分别同步，绝不互相覆盖：

1. **sidecar 族**（`names/武器分配明细.csv` col1 的 1628 个 `2+練度ID[1:5]+sub4`，多为 9 位）
   —— 权威 = **那份 CSV**（← 维基模板 + `weapon_client_raw` 的面板→原值换算）。
   方向：**CSV → 库**（本节上面的整族重写）。
2. **8 位 icon-id 族**（`可达武器号域.csv` 里标 `现役引用`/`客户端近战` 的短号，如 `01010401`）
   —— 权威 = **库**（← `load_paired_ms_db.py`：`gow_wiki/data/units.json` 的
   `icon_id` 按"出现次数最多的第一档"归并 + 同一套换算）。本脚本对它们**只回灌、不改值**。
   方向：**库 → CSV**。

为什么第 2 族必须回灌（C4 实测）
--------------------------------
第 2 族的 CSV 行是**更早的占位管线**（`gen_weapon_pipeline.py`）写的：它把
**面板白字原样**塞进了原值列 —— `STABILITY=920`（真值 `0.397003`）、`LOCKON_CAM=760`
（真值 `75.960025`）、`POWER=950`（库里 `250`）。CSV 是**客户端要下载的那份下发件**
（`download_list.csv` 里有 `WEAPON_BATTLE_DETAIL`），所以这 32 行漂移不是"内部不一致"，
而是**真会被客户端按错口径读数**（集弹性能差 2300 倍）。
生成器侧故意不清这一族（键不在 sidecar ⇒ 判据 `_purge_fam36` 不命中，见
`gen_weapon_tables_wiki.py` §口径哨的"不抹掉别的管线的行"），于是**只能在这一侧补**。

安全
====
- 默认**干跑**；`--apply` 才写库，`--no-csv-mirror` 可只写库不动 CSV。
- 写库前把将被改动的行（含将被删的行）导出成回滚 SQL（`datatables/_rollback/`），并打印前后对账；
  回灌前把 CSV 原样另存为 `_rollback/<stamp>_weapon_battle_detail.csv`。
- 整个写入在一个事务里；任一行报错整体回滚。

用法
====
  python apply_weapon_tables_db.py            # 干跑 + 报告
  python apply_weapon_tables_db.py --apply    # 写库 + 回灌 CSV（自动留回滚件）
"""
import csv
import datetime
import io
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import weapon_client_raw as RAW  # noqa: E402  （import 期不动 stdout）

DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
T78 = os.path.join(DF, "item.csv")
T36 = os.path.join(DF, "weapon_battle_detail.csv")
T37 = os.path.join(DF, "weapon_settings.csv")
ROLLBACK_DIR = os.path.join(HERE, "_rollback")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

BATTLE_COLS = ("attr_name", "weapon_id_key", "attr_value", "attr_value_2")
FAM36 = RAW.FAMILIES_36


def rd(path):
    if not os.path.exists(path):
        return []
    return [r for r in csv.reader(open(path, encoding="utf-8", errors="replace")
                                  .read().replace("\r\n", "\n").split("\n"))
            if r and any(x.strip() for x in r) and not r[0].lstrip("\ufeff").startswith("#")]


def real_ids():
    """真实武器 id（sidecar 的武器ID 列）= 唯一允许被本脚本改写的 id 集合。"""
    out = set()
    for r in rd(SIDE):
        if len(r) > 1 and r[1].strip().isdigit():
            out.add(int(r[1].strip()))
    return out


def sql_quote(s):
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"


# ── 管理域外回灌（8 位 icon-id 族）────────────────────────────────────────────
# 见文件头 §口径。判据与生成器、写库两处**同口径**：键 ∉ sidecar 的 `ids`，且属性 ∈ FAM36。


def mirror_plan(ids, mirror):
    """返回 CSV 回灌计划：{body 新行, 改, 补, 删, 原行数}。

    只碰「键 ∉ ids 且属性 ∈ FAM36」的行 —— sidecar 族的行一个字都不动。
    """
    old = open(T36, encoding="utf-8", errors="replace").read().replace("\r\n", "\n").split("\n") \
        if os.path.exists(T36) else []
    head = [l for l in old if l.strip().startswith("#")]
    body = [l for l in old if l.strip() and not l.strip().startswith("#")]

    upd, add, dele = [], [], []
    out = []
    seen = set()
    for line in body:
        f = line.split(",")
        if len(f) >= 3 and f[1].strip().isdigit() and f[0].strip() in FAM36 \
                and int(f[1].strip()) not in ids:
            k = (int(f[1].strip()), f[0].strip())
            if k not in mirror:                      # 库里没有 ⇒ 是域外残渣，删
                dele.append(k)
                continue
            v, v2 = mirror[k]
            new = "%s,%s,%s,%s" % (k[1], k[0], v, v2)
            if new != line:
                upd.append((k, line, new))
            out.append(new)
            seen.add(k)
        else:
            out.append(line)
    for k in sorted(set(mirror) - seen):             # 库里有、CSV 没有 ⇒ 补
        v, v2 = mirror[k]
        new = "%s,%s,%s,%s" % (k[1], k[0], v, v2)
        add.append((k, new))
        out.append(new)
    return head, out, upd, add, dele, len(body)


def main():
    apply = "--apply" in sys.argv
    mirror_csv = "--no-csv-mirror" not in sys.argv
    ids = real_ids()
    if not ids:
        raise SystemExit("sidecar 里没读到武器ID")

    b36 = []          # (attr, id, val, val2)
    for r in rd(T36):
        if len(r) >= 3 and r[1].strip().isdigit():
            b36.append((r[0].strip(), r[1].strip(), r[2].strip(),
                        r[3].strip() if len(r) > 3 else ""))
    # CSV14 is an animation layer selector, not ammunition. Existing derived
    # CSVs contain wiki clip sizes here; never copy those into runtime models.
    # Finite ammunition is repaired by serverv/tools/repair_runtime_ammo.py.
    items = {}        # id -> 名称
    for r in rd(T78):
        if len(r) >= 5 and r[0].strip().isdigit():
            items[r[0].strip()] = r[2].strip()

    print("sidecar 真实武器 id %d；#36 行 %d（去重键 %d）；#37 跳过错误弹数投影；#78 名称 %d"
          % (len(ids), len(b36), len(set((a, i) for a, i, _, _ in b36)), len(items)))

    conn = psycopg.connect(DSN)
    conn.autocommit = False
    cur = conn.cursor()

    # ---- 现状快照 + 回滚件 ----
    keys = sorted(set((int(i), a) for a, i, _, _ in b36))
    cur.execute('''select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value),
                          btrim(coalesce(attr_value_2,'')), _row_id
                     from cfg."WEAPON_BATTLE_DETAIL"
                    where btrim(weapon_id_key) ~ '^[0-9]+$' ''')
    have = {}
    db_rows = []
    for k, a, v, v2, rid in cur.fetchall():
        have[(int(k), a)] = (v, v2)
        db_rows.append((rid, k, a, v, v2))

    before_have = sum(1 for k in keys if k in have)
    want = {(int(i), a): (v, v2) for a, i, v, v2 in b36 if int(i) in ids}
    diff = sorted((k, have.get(k), v) for k, v in want.items() if have.get(k) != v)
    add = sorted(k for k in want if k not in have)
    print("将被改写的 #36 键 %d：库里已有 %d、其中**值不同** %d、库里没有的（新增） %d"
          % (len(want), before_have, len(diff), len(add)))

    # ---- ★整族重写：库里多出来的行（真武器号 × FAM36，CSV 没有的）一律删 ----
    # 判据与生成器那侧的 purge 同口径（`gen_weapon_tables_wiki._purge_fam36` + `FAM36`）。
    prune = [r for r in db_rows
             if int(r[1]) in ids and r[2] in FAM36 and (int(r[1]), r[2]) not in want]
    _pc = Counter(r[2] for r in prune)
    print("将被整族重写**删掉**的 #36 行 %d：%s" % (len(prune), dict(_pc.most_common())))
    for rid, k, a, v, v2 in prune[:8]:
        print("   - #36 %-11s %-12s %s" % (k, a, v))

    # ---- ★管理域外回灌：8 位 icon-id 族的八族行，以库为准重写 CSV（见文件头 §口径）----
    mirror = {(int(k), a): (v, v2) for (k, a), (v, v2) in have.items()
              if int(k) not in ids and a in FAM36}
    head36, body36, m_upd, m_add, m_del, n_csv36 = mirror_plan(ids, mirror)
    print("管理域外（8 位 icon-id 族）八族：库 %d 行 / CSV %d 行 ⇒ 改 %d、补 %d、删 %d%s"
          % (len(mirror), n_csv36, len(m_upd), len(m_add), len(m_del),
             "" if mirror_csv else "（--no-csv-mirror：跳过）"))
    for k, old_l, new_l in m_upd[:6]:
        print("   ~ #36 %-11s %-12s %-12s → %s" % (k[0], k[1], old_l.split(",")[2], new_l.split(",")[2]))
    for k, new_l in m_add[:4]:
        print("   + #36 %-11s %-12s %s" % (k[0], k[1], new_l.split(",")[2]))

    cur.execute('''select btrim(item_id) from cfg."ITEM" ''')
    have_item = {int(k) for (k,) in cur.fetchall() if k.strip().isdigit()}
    item_missing = sorted(int(i) for i in items if int(i) in ids and int(i) not in have_item)
    print("将被补建的 #78 物品行 %d" % len(item_missing))

    if not apply:
        print()
        print("（干跑）示例改动：")
        for k, old, new in diff[:8]:
            print("   #36 %-12s %-12s %s → %s" % (k[0], k[1], old, new))
        print("★ 干跑结束。加 --apply 才写库。")
        conn.rollback()
        conn.close()
        return

    # ---- 回滚件 ----
    os.makedirs(ROLLBACK_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rb = os.path.join(ROLLBACK_DIR, "%s_weapon_tables.sql" % stamp)
    with open(rb, "w", encoding="utf-8", newline="\n") as f:
        f.write("-- 回滚件：%s 之前的战斗明细/物品状态（按键还原）\n" % stamp)
        f.write("begin;\n")
        for (wid, attr) in keys:
            f.write("delete from cfg.\"WEAPON_BATTLE_DETAIL\" where btrim(weapon_id_key)='%d' "
                    "and btrim(attr_name)=%s;\n" % (wid, sql_quote(attr)))
            if (wid, attr) in have:
                v, v2 = have[(wid, attr)]
                f.write("insert into cfg.\"WEAPON_BATTLE_DETAIL\" "
                        "(attr_name,weapon_id_key,attr_value,attr_value_2) values (%s,%d,%s,%s);\n"
                        % (sql_quote(attr), wid, sql_quote(v), sql_quote(v2)))
        for rid, k, a, v, v2 in prune:
            f.write("delete from cfg.\"WEAPON_BATTLE_DETAIL\" where _row_id=%d;\n" % rid)
            f.write("insert into cfg.\"WEAPON_BATTLE_DETAIL\" "
                    "(attr_name,weapon_id_key,attr_value,attr_value_2) values (%s,%s,%s,%s);\n"
                    % (sql_quote(a), k, sql_quote(v), sql_quote(v2)))
        for wid in item_missing:
            f.write("delete from cfg.\"ITEM\" where btrim(item_id)='%d';\n" % wid)
        f.write("commit;\n")
    print("回滚件：%s" % os.path.relpath(rb, ROOT))

    # ---- 写库 ----
    n_prune = 0
    for rid, k, a, v, v2 in prune:
        cur.execute('delete from cfg."WEAPON_BATTLE_DETAIL" where _row_id=%s', (rid,))
        n_prune += cur.rowcount
    n36 = 0
    for (wid, attr), (v, v2) in want.items():
        cur.execute('''delete from cfg."WEAPON_BATTLE_DETAIL"
                        where btrim(weapon_id_key)=%s and btrim(attr_name)=%s''', (str(wid), attr))
        cur.execute('''insert into cfg."WEAPON_BATTLE_DETAIL"
                        (attr_name, weapon_id_key, attr_value, attr_value_2)
                       values (%s,%s,%s,%s)''', (attr, str(wid), v, v2))
        n36 += 1
    n78 = 0
    for wid in item_missing:
        cur.execute('''insert into cfg."ITEM" (item_id, sort_group, name, description, item_type)
                       values (%s,%s,%s,'','WEAPON')''',
                    (str(wid), str(wid), items[str(wid)]))
        n78 += 1
    conn.commit()
    print("写入：#36 删 %d 行 / 改 %d 行 / #78 新建 %d 行"
          % (n_prune, n36, n78))

    # ---- 回灌 CSV（管理域外八族），先留原件的备份 ----
    if mirror_csv and (m_upd or m_add or m_del):
        bak = os.path.join(ROLLBACK_DIR, "%s_weapon_battle_detail.csv" % stamp)
        with open(bak, "wb") as f:
            f.write(open(T36, "rb").read())
        open(T36, "wb").write(("\r\n".join(head36 + body36) + "\r\n").encode("utf-8"))
        print("回灌 CSV：%s 改 %d / 补 %d / 删 %d（原件存 %s）"
              % (os.path.relpath(T36, ROOT), len(m_upd), len(m_add), len(m_del),
                 os.path.relpath(bak, ROOT)))
    elif mirror_csv:
        print("回灌 CSV：已是同值，无需改")
    print("★ 完成（回滚件在手，必要时 psql -f 它）")
    conn.close()


if __name__ == "__main__":
    main()

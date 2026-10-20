#!/usr/bin/env python3
"""旧库对账（P2 验收）：新模型的自然键 vs 旧 DDL 的 UNIQUE 索引。

为什么需要这一步
================
旧 DDL 每张表都是「代理主键 `id` + 唯一索引 `<自然键>`」——代理键让表之间无法建
外键（`relations.json` 因此是空数组），但**那个唯一索引里已经写着正确的自然键**，
它是旧 `plan.py` 用 `SLOT_SOURCES` 从线模型推出来的。新模型把自然键提上来当主键，
所以两边**必须逐表一致**：不一致就说明归位规则把行身份搞错了，而不是「新设计」。

口径
====
新 `PRIMARY KEY` = `(world_id, pilot_id) + own`；旧 UNIQUE = 旧库该表的唯一索引列。
只对**同名沿用**的表对账（旧表名 = `tbl_<x>` → `game.<x>`）；折叠吸收、新建的表不在
此列（它们没有可对账的旧唯一索引）。

旧库已删（「无兼容」口径），所以默认不再连库：唯一索引列序读**冻结证据**
`schema/_meta/legacy_evidence.json`（`tools/freeze_legacy.py` 冻结）。结论不变，
但这条对账从此**不需要数据库**、随时可重跑。

用法
====
  python tools/reconcile_legacy_ddl.py            # 只对账（读冻结证据）
  python tools/reconcile_legacy_ddl.py --strict   # 有差异则退出码 1
  python tools/reconcile_legacy_ddl.py --dsn DSN  # 确实还有旧库可连时，改读真库
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_homing as D  # noqa: E402

DEFAULT_DSN = os.environ.get(
    "MSGO_TEST_DSN",
    "postgres://postgres:admin123@127.0.0.1:5432/msgo?sslmode=disable")

_QUERY = """
select c.relname,
       string_agg(a.attname, ',' order by array_position(i.indkey, a.attnum))
from pg_index i
join pg_class c on c.oid = i.indrelid
join pg_namespace n on n.oid = c.relnamespace
join pg_attribute a on a.attrelid = c.oid and a.attnum = any(i.indkey)
where n.nspname = 'game' and c.relkind = 'r'
  and i.indisunique and not i.indisprimary and i.indnatts > 0
group by c.relname, i.indexrelid
"""


def psql_rows(dsn: str, query: str) -> list[list[str]]:
    exe = os.environ.get("PSQL", "psql")
    out = subprocess.run([exe, dsn, "-t", "-A", "-F", "|", "-c", query],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit(f"psql 失败：{out.stderr.strip()}")
    return [ln.split("|") for ln in out.stdout.splitlines() if ln.strip()]


def legacy_unique(dsn: str) -> dict[str, list[list[str]]]:
    """旧库 `game.<表>` → 唯一索引列集（去掉代理键 id）。"""
    boxes: dict[str, list[list[str]]] = {}
    for tbl, cols in psql_rows(dsn, _QUERY):
        boxes.setdefault(tbl, []).append(cols.split(","))
    return boxes


def legacy_unique_frozen() -> dict[str, list[list[str]]]:
    """同上，但读**冻结的旧库证据** `schema/_meta/legacy_evidence.json`（默认口径）。

    旧库已按「无兼容」口径删除，`psql` 那条路走不通了；把唯一索引列序冻进模型之后，
    这条对账反而变成**不需要数据库**、任何时候都能重跑的门——结论与旧库一致时也就能
    长期守住了（`--dsn` 只在确实还有一份旧库可连时才用）。
    """
    ev = D.legacy_declared()
    boxes: dict[str, list[list[str]]] = {}
    for stem, node in ev.items():
        live = node.get("live") or {}
        if not live.get("exists"):
            continue
        cols = [list(i.get("columns") or []) for i in live.get("unique_indexes") or []]
        if cols:
            boxes[stem] = cols
    return boxes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", help="旧库 DSN（默认读冻结证据，只有还真有旧库可连时才给）")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    m = D.Model()
    objects, _, _ = D.build(m)
    old = legacy_unique(args.dsn or DEFAULT_DSN) if args.dsn else legacy_unique_frozen()

    same, diff, only_new, only_old = 0, [], 0, []
    for o in sorted(objects.values(), key=lambda x: x["id"]):
        if o.get("disposition") != "PERSIST" or not o.get("is_root"):
            continue
        lt = (o.get("legacy_table") or "").removeprefix("tbl_")
        if not lt or lt not in old:
            only_new += 1
            continue
        # 新 PK 用**列名**口径比（`inv_place` 落库列名是 `slot`，与旧库同名才算一致）。
        # 投影在 `columns[]` 里，人工 `colname` 订正也反映在那里。
        col_of = {c["member"]: c["column"] for c in o.get("columns") or []}
        new_pk = [col_of.get(c, c) for c in o["keys"]["primary_key"]]
        olds = old[lt]
        if new_pk in olds:
            same += 1
            continue
        # 旧库可能把同一自然键建了多个唯一索引；取列集最接近的那个报差异
        diff.append((o["id"], lt, new_pk, olds, o["keys"]["pk_kind"]))
    for lt in old:
        if not any((o.get("legacy_table") or "") == "tbl_" + lt
                   for o in objects.values()):
            only_old.append(lt)

    w = max([len(d[0]) for d in diff] + [10])
    print(f"沿用旧表名且可对账 : {same} 表一致")
    print(f"                       {len(diff)} 表不一致")
    print(f"新建表（无旧索引可对）: {only_new}")
    print(f"旧表被折叠/消失       : {len(only_old)} -> {sorted(only_old)}")
    if diff:
        print()
        print(f"{'对象':<{w}}  {'旧表':<24} {'新 PK':<34} {'旧 UNIQUE':<34} 依据")
        for oid, lt, new_pk, olds, kind in diff:
            print(f"{oid:<{w}}  {lt:<24} {'+'.join(new_pk):<34} "
                  f"{'; '.join('+'.join(x) for x in olds):<34} {kind}")
    if args.strict and diff:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

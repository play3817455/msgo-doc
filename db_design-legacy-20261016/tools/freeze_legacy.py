#!/usr/bin/env python3
"""把「旧库证据」冻进模型：`schema/_meta/legacy_evidence.json`。

为什么需要这一步
================
归位裁决里有相当一部分**依据写在旧库上**，而不是写在 `db_design/schema/` 里：

* 24 条 `singleton`（每作用域一行）裁决引的是旧库 `uq_game_<table>_world_pilot (world_id, pilot_id)`；
* 「旧表守恒」门引的是 `_legacy_tables/*.json` 的人工声明（disposition / entity_ref）；
* `reserved` 列去留、`slot` 合成列、旧列名与线成员的对应，引的是旧库的列清单与列注释。

这些事实原先只存在于 `_backup_before_p4_*/migrations/live_game_schema.sql`（pg_dump 快照，仓库外）。
一旦按「旧库完全删除、不做兼容」把它删掉，上面的裁决就**只剩结论、没有依据**——下次有人问
「凭什么是单行」时无从复核。本工具做的是**把依据搬进模型**：结构化、可 diff、可被守卫校验。

产出
====
`schema/_meta/legacy_evidence.json`，按**表干**（`bracket` ← `game.bracket` / `tbl_bracket`）索引：

    declaration  人工声明：disposition（+ 来源）/ entity_ref / purpose / evidence_commands / row_key
    live         旧库实况：columns（名/类型/NOT NULL）、primary_key、unique_indexes、indexes、comments
                 `live.exists=false` 表示「声明过但真库里没有这张表」（P4 前查过的那 13 张）

声明侧是**合并**结果：`tbl_*.json` 优先、`schema/relations.json` 兜底（`tbl_pilot` 的
`PERSIST` 只在注册表里），`disposition_source` 记下每张表这一列的出处。

本文件是**只读证据**。引擎与守卫只读它，不写它；旧表声明变了要重跑本工具。
用法：

    python db_design/tools/freeze_legacy.py                       # 自动找 _backup_before_p4_*/live_game_schema.sql
    python db_design/tools/freeze_legacy.py --live-schema PATH     # 指定 pg_dump 快照
    python db_design/tools/freeze_legacy.py --check                # CI：与磁盘上的声明/快照是否一致
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = Path(__file__).resolve().parents[1] / "schema"
OUT = SCHEMA / "_meta" / "legacy_evidence.json"

TABLE_RE = re.compile(r"^CREATE TABLE game\.(\w+) \($(.*?)^\);$", re.M | re.S)
PK_RE = re.compile(r"ALTER TABLE ONLY game\.(\w+)\s+ADD CONSTRAINT \w+ PRIMARY KEY \(([^)]*)\);")
INDEX_RE = re.compile(r"^CREATE (UNIQUE )?INDEX (\w+) ON game\.(\w+) USING \w+ \(([^)]*)\);", re.M)
COMMENT_RE = re.compile(r"^COMMENT ON COLUMN game\.(\w+)\.(\w+) IS '(.*)';$", re.M)
COL_RE = re.compile(r'^\s{4}("?\w+"?) (.*?),?$')


def _col(name: str) -> str:
    return name.strip().strip('"')


def find_dump(explicit: str | None) -> Path | None:
    if explicit:
        return Path(explicit)
    hits = sorted(ROOT.glob("_backup_before_p4_*/migrations/live_game_schema.sql"))
    return hits[-1] if hits else None


def parse_dump(text: str) -> dict[str, dict]:
    """pg_dump 快照 → {表干: {columns, primary_key, unique_indexes, indexes, comments}}。"""
    live: dict[str, dict] = {}
    for table, body in TABLE_RE.findall(text):
        cols = []
        for line in body.splitlines():
            m = COL_RE.match(line)
            if not m:
                continue
            name, rest = m.group(1), m.group(2).strip()
            not_null = rest.endswith(" NOT NULL")
            if not_null:
                rest = rest[: -len(" NOT NULL")]
            pg_type = rest.split(" DEFAULT ")[0].strip()
            cols.append({"name": _col(name), "type": pg_type, "not_null": not_null})
        live[table] = {"exists": True, "columns": cols, "primary_key": [],
                       "unique_indexes": [], "indexes": [], "comments": {}}
    for table, cols in PK_RE.findall(text):
        if table in live:
            live[table]["primary_key"] = [_col(c) for c in cols.split(",")]
    for unique, idx, table, cols in INDEX_RE.findall(text):
        if table not in live:
            continue
        entry = {"name": idx, "columns": [_col(c) for c in cols.split(",")]}
        live[table]["indexes"].append(entry)
        if unique:
            live[table]["unique_indexes"].append(entry)
    for table, col, comment in COMMENT_RE.findall(text):
        if table in live:
            live[table]["comments"][col] = comment
    for t in live.values():
        t["indexes"].sort(key=lambda x: x["name"])
        t["unique_indexes"].sort(key=lambda x: x["name"])
    return live


def parse_declarations() -> dict[str, dict]:
    """旧表人工声明 = `_legacy_tables/tbl_*.json` **合并** `schema/relations.json` 的注册表。

    必须合并，且顺序是「表文件 → 注册表 → 已冻结的快照」三级兜底：

    * `tbl_pilot.json` 自己没写 `table_disposition`，只有（已退役的）`relations.json` 写着
      `PERSIST`（`generate_all.py` 当年就是这么合并的）。少这一步，快照会把 `tbl_pilot`
      降级成「未声明」，守恒门随之静默放行——正是它要防的那种静默丢表；
    * 旧表注册表退役后连它也没了，所以再兜一层**已冻结快照**：冻结过的事实只增不减，
      重跑本工具不会把 `purpose`/`status`/`disposition` 这类只写在注册表里的字段抹掉。

    `disposition_source` 记下每张表这一列最终是从哪儿来的。
    """
    index: dict[str, dict] = {}
    index_path = SCHEMA / "relations.json"
    if index_path.is_file():
        for entry in json.loads(index_path.read_text(encoding="utf-8")).get("tables") or []:
            index[entry.get("id", "")] = entry
    # 已冻结的快照：最后一级兜底
    frozen: dict[str, dict] = {}
    if OUT.is_file():
        try:
            frozen = json.loads(OUT.read_text(encoding="utf-8")).get("tables") or {}
        except (json.JSONDecodeError, OSError):
            frozen = {}

    def pick(*vals):
        """第一个非空值 + 它的来源标签。"""
        for label, v in vals:
            if v:
                return v, label
        return "", "none"

    out = {}
    for path in sorted((SCHEMA / "_legacy_tables").glob("tbl_*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        stem = path.stem.removeprefix("tbl_")
        tid = d.get("id", path.stem)
        reg = index.get(tid) or {}
        was = (frozen.get(stem) or {}).get("declaration") or {}
        rk = d.get("row_key") or {}
        disp, source = pick(("table_file", d.get("table_disposition")),
                            ("relations_json", reg.get("table_disposition")),
                            ("frozen", was.get("disposition")))
        status, ssource = pick(("table_file", d.get("status")),
                               ("relations_json", reg.get("status")),
                               ("frozen", was.get("status")))
        purpose, psource = pick(("table_file", d.get("purpose")),
                                ("relations_json", reg.get("purpose")),
                                ("frozen", was.get("purpose")))
        out[stem] = {
            "id": tid,
            "table": f"game.{stem}",
            "disposition": disp,
            "disposition_source": source,
            "status": status,
            "status_source": ssource,
            "entity_ref": d.get("entity_ref") or was.get("entity_ref") or "",
            "title": d.get("title") or was.get("title") or "",
            "purpose": purpose,
            "purpose_source": psource,
            "evidence_commands": sorted(set(d.get("evidence_commands") or [])
                                        | set(reg.get("evidence_commands") or [])
                                        | set(was.get("evidence_commands") or [])),
            "declared_row_key": list(rk.get("columns") or []) or None,
            "declared_external_row_key": list((rk.get("external") or {}).keys()) or None,
            "declared_child_tables": len(d.get("child_tables") or []),
        }
    return out


def build(live_path: Path | None, frozen: dict | None = None) -> dict:
    """`frozen` = 已冻结的旧产物（重跑时的上一版）：两级都只增不减。

    声明侧：`parse_declarations()` 用冻结值兜底（旧注册表退役后 `tbl_pilot` 的
    `PERSIST` 只能从这里来）；实况侧同理——**没有 pg_dump 可解析时，已冻结的 live 段
    原样保留**。否则旧库 dump 一删，随手重跑一次就把唯一键列序/列注释抹成
    `exists=false`，把「依据」原地烧掉（守卫会报错，但数据已经没了）。
    """
    decl = parse_declarations()
    live = parse_dump(live_path.read_text(encoding="utf-8")) if live_path and live_path.is_file() else {}
    frozen_tables = (frozen or {}).get("tables") or {}
    reused = []
    tables = {}
    for stem in sorted(set(decl) | set(live) | set(frozen_tables)):
        node = live.get(stem)
        if node is None:
            was = (frozen_tables.get(stem) or {}).get("live") or {}
            node = was if was else {"exists": False}
            if was.get("exists"):
                reused.append(stem)
        tables[stem] = {"declaration": decl.get(stem), "live": node}
    persist = [s for s, t in tables.items()
               if (t["declaration"] or {}).get("disposition") == "PERSIST"]
    single_row = [s for s, t in tables.items()
                  if any(set(i["columns"]) == {"world_id", "pilot_id"}
                         for i in (t["live"].get("unique_indexes") or []))]
    return {
        "_note": (
            "冻进模型的旧库证据（docs/05 §9.4）。旧库（pg_dump 快照 + 旧表声明）按「无兼容」口径删除后，"
            "归位裁决里凡引用旧库（单行 UNIQUE 列序、列清单/NOT NULL、列注释、声明 disposition/entity_ref）"
            "的事实都改由本文件承载。只读：引擎与守卫只读它，不写它；旧表声明变了重跑 tools/freeze_legacy.py。"
            "`live.exists=false` = 声明过但旧库里没有这张表（P4 前查过）。"
        ),
        "frozen_at": date.today().isoformat(),
        "sources": {
            "declarations": "schema/_legacy_tables/tbl_*.json",
            "table_index": "schema/relations.json（已退役，注册表内容并入本文件）",
            # 旧库 dump 删掉之后，这里保留**原始出处路径**（已失效，只作 provenance）：
            # 让「这批唯一键列序是从哪份 pg_dump 读的」永远可回答，见 live_reused_from_frozen。
            "live_schema_dump": (str(live_path) if live_path and live_path.is_file()
                                 else (frozen or {}).get("sources", {}).get("live_schema_dump", "")),
        },
        "stats": {
            "declared": len(decl),
            "declared_persist": len([s for s in decl if decl[s]["disposition"] == "PERSIST"]),
            "live_tables": len([s for s, t in tables.items() if t["live"].get("exists")]),
            "live_reused_from_frozen": len(reused),
            "disposition_from_relations_json": sorted(
                s for s in decl if decl[s]["disposition_source"] == "relations_json"),
            "declared_but_not_live": sorted(s for s, t in tables.items()
                                            if t["declaration"] and not t["live"].get("exists")),
            "single_row_unique": sorted(single_row),
        },
        "tables": tables,
    }


def _decl_core(decl: dict | None) -> dict:
    """声明里**去掉 `*_source` 出处标签**的部分。

    出处标签随「哪一级兜底命中」而变（旧注册表在 → `relations_json`；注册表退役后同一
    个值从冻结值兜底 → `frozen`），值本身没变，所以核对漂移时不该把它算作差异。
    """
    return {k: v for k, v in (decl or {}).items() if not k.endswith("_source")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live-schema", help="pg_dump 快照（默认自动找 _backup_before_p4_*/migrations/live_game_schema.sql）")
    ap.add_argument("--check", action="store_true", help="只校验：重算结果与已冻结文件是否一致")
    args = ap.parse_args()

    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.is_file() else None
    live_path = find_dump(args.live_schema)
    have_dump = bool(live_path and live_path.is_file())
    doc = build(live_path if have_dump else None, old)
    text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"

    if args.check:
        if old is None:
            print(f"FAIL  缺 {OUT}（先跑 python tools/freeze_legacy.py）")
            return 1
        if have_dump:
            if OUT.read_text(encoding="utf-8") != text:
                print(f"FAIL  {OUT} 与声明 + 旧库快照不一致"
                      f"（重跑 python tools/freeze_legacy.py，并确认是有意改的）")
                return 1
            print(f"OK    {OUT} 与声明 + 旧库快照一致（{doc['stats']['declared']} 声明 / "
                  f"{doc['stats']['live_tables']} 实表）")
            return 0
        # 旧库 dump 已按「无兼容」口径删除：live 段不再再生，只核①声明值没漂、②live 段还在。
        drift, soft = [], []
        was_tables = old.get("tables") or {}
        for stem, node in sorted(doc["tables"].items()):
            was = was_tables.get(stem)
            if was is None:
                drift.append(f"{stem}: 新增声明未冻结")
                continue
            if _decl_core(was.get("declaration")) != _decl_core(node["declaration"]):
                drift.append(f"{stem}: 声明与冻结值不一致")
            elif was.get("declaration") != node["declaration"]:
                soft.append(stem)
            if not (was.get("live") or {}):
                drift.append(f"{stem}: 冻结文件丢了 live 段")
        for stem in sorted(set(was_tables) - set(doc["tables"])):
            drift.append(f"{stem}: 冻结文件里有、声明侧已无（旧表被删？）")
        if drift:
            print(f"FAIL  {len(drift)} 处漂移（重跑 python tools/freeze_legacy.py 前先确认是有意改的）")
            for d in drift[:12]:
                print("  -", d)
            return 1
        if soft:
            print(f"      {len(soft)} 处出处标签变化（同名值改由冻结值兜底）：{' '.join(soft[:8])}")
        print(f"OK    {OUT} 与声明侧一致（{doc['stats']['declared']} 声明 / "
              f"{doc['stats']['live_tables']} 实表，其中 {doc['stats']['live_reused_from_frozen']} "
              f"张实况复用冻结值）；旧库 dump 已删，live 段只核存在性")
        return 0

    if live_path and not have_dump:
        print(f"WARN  找不到旧库快照 {live_path}——live 段沿用冻结值（不再重新解析）")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    s = doc["stats"]
    print(f"wrote {OUT}")
    print(f"  声明 {s['declared']}（PERSIST {s['declared_persist']}）· 旧库实表 {s['live_tables']} · "
          f"单行 UNIQUE {len(s['single_row_unique'])}")
    if s["live_reused_from_frozen"]:
        print(f"  实况复用冻结值 {s['live_reused_from_frozen']} 张（无 pg_dump 可解析）")
    if s["declared_but_not_live"]:
        print(f"  声明过但旧库没有：{' '.join(s['declared_but_not_live'])}")
    src = doc["sources"]["live_schema_dump"]
    if have_dump:
        print(f"  源：{src}")
    elif src:
        print(f"  源：{src}（已删；live 段全部复用冻结值，未重新解析）")
    else:
        print("  源：（无旧库快照，live 段来自冻结值）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

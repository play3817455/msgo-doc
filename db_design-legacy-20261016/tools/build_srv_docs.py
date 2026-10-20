#!/usr/bin/env python3
"""从迁移 SQL 生成 `db_design/schema/srv/*.json`（服务端配置表的文档投影）。

为什么是「生成」而不是手写
==========================
`srv.*` 的运行时来源是迁移 SQL（`serverv/migrations/0012_srv_config.up.sql`、
`0013_srv_lobby.up.sql`…），列的协议证据 VA 就写在 SQL 的 `COMMENT` 里。文档站要的那份
JSON 只是 HTML 的输入（用户口径：JSON 只当文档用），所以这里**从 SQL 反推**，避免
「SQL 改了、文档没改」两份真相。

**扫全部迁移**而不是写死一个文件名：`srv.*` 会随批次增长（0012 配置值、0013 大厅链…），
写死文件名就会出现「新表静默漏进文档站」。判定依据是迁移里有没有 `CREATE TABLE srv.`，
每张表的 `ddl` 字段记它**自己**来自哪个迁移。

用法
====
    python db_design/tools/build_srv_docs.py          # 生成
    python db_design/tools/build_srv_docs.py --check  # 只校验是否与 SQL 一致（门禁用）

`--check` 与生成走同一条解析路径：先算内存里的文档，再与磁盘上的 JSON 逐字节比对。
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS = ROOT / "serverv" / "migrations"
OUT_DIR = ROOT / "db_design" / "schema" / "srv"
GEN_BY = "db_design/tools/build_srv_docs.py"

NOTE = "本文件由 " + GEN_BY + " 从 <ddl> 生成，勿手改：改 srv.* 请改迁移再重跑生成器"

INTRO = [
    "这些表既不是客户端 datafile 的投影（那是 <code>cfg.*</code>，由 cfgload 按 CSV 动态建表），"
    "也不是每机师持久化（那是 <code>game.*</code>，行键含 world_id/pilot_id）："
    "它们是<strong>全服唯一的服务端策略参数 / 大区内容</strong>。",
    "运行时来源就是这些表本身——<code>db_design</code> 的 JSON 只当文档（HTML 站点输入）。"
    "缺省值与降级在 <code>internal/lounge/srv_config.go</code>（<code>loadSrv*</code>，"
    "表没播种/读库失败时用缺省值 + 告警，不断链）。按请求读表 ⇒ 改表即热更。",
    "每列的协议证据 VA 写在迁移 SQL 的 <code>COMMENT</code> 里，本页正文即由迁移反推"
    "（扫 <code>serverv/migrations/</code> 下所有含 <code>CREATE TABLE srv.</code> 的文件；"
    "每张表标出自己的迁移文件名，不写死版本号，免得新表静默漏进文档站）。",
]

# ---------------------------------------------------------------- SQL 解析

CREATE_RE = re.compile(r"CREATE TABLE\s+srv\.(\w+)\s*\((.*?)\n\)\s*;", re.S)
SRV_TABLE_RE = re.compile(r"CREATE TABLE\s+(?:IF NOT EXISTS\s+)?srv\.\w+")
TBL_COMMENT_RE = re.compile(r"COMMENT ON TABLE\s+srv\.(\w+)\s+IS\s+'(.*?)';", re.S)
COL_COMMENT_RE = re.compile(r"COMMENT ON COLUMN\s+srv\.(\w+)\.(\w+)\s+IS\s+'(.*?)';", re.S)
INSERT_RE = re.compile(r"INSERT INTO\s+srv\.(\w+)\s*\(([^)]*)\)\s*VALUES\s*(.*?);", re.S)
SECTION_RE = re.compile(r"^-- -+\s*(.+?)\s*$", re.M)
COL_RE = re.compile(r"^(\w+)\s+([A-Z][A-Z0-9]*(?:\(\d+(?:,\d+)?\))?)\b(.*)$")
DEFAULT_RE = re.compile(r"\bDEFAULT\s+(\S+)")
CHECK_RE = re.compile(r"\bCHECK\s*\((.+?)\)\s*(?:,|$)", re.S)


def split_csv(text: str) -> list[str]:
    return [p.strip() for p in text.split(",") if p.strip()]


def split_tuples(text: str) -> list[str]:
    out, depth, start = [], 0, -1
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and start >= 0:
                out.append(text[start:i])
    return out


def section_titles(sql: str) -> dict[str, str]:
    """`-- ---- 背包四栏容量` 这类分节注释 → 其后的表标题。"""
    titles: dict[str, str] = {}
    pending = None
    for line in sql.splitlines():
        m = SECTION_RE.match(line.strip())
        if m:
            pending = m.group(1)
            continue
        m = re.match(r"CREATE TABLE\s+srv\.(\w+)", line.strip())
        if m and pending:
            titles[m.group(1)] = pending
            pending = None
    return titles


def srv_sql_files() -> list[tuple[str, str]]:
    """所有建 `srv.*` 的迁移 → [(相对路径, SQL 全文)]，按文件名（= 版本号）排序。

    不写死 `0012`：`srv.*` 会随批次增长（0012 配置值、0013 大厅链…），写死会出现
    「新迁移的表静默不进文档站」。
    """
    out: list[tuple[str, str]] = []
    for path in sorted(MIGRATIONS.glob("*.up.sql")):
        text = path.read_text(encoding="utf-8")
        if SRV_TABLE_RE.search(text):
            out.append((path.relative_to(ROOT).as_posix(), text))
    if not out:
        raise SystemExit(f"{MIGRATIONS} 下找不到任何 CREATE TABLE srv.* 的迁移")
    return out


def parse(sql: str) -> tuple[dict[str, dict], dict[str, list[dict]], dict[str, list[str]]]:
    """返回 (表 → 定义, 表 → 种子行(列名→值), 表 → INSERT 列序)。"""
    purposes = {m.group(1): m.group(2).strip() for m in TBL_COMMENT_RE.finditer(sql)}
    col_meanings: dict[tuple[str, str], str] = {
        (m.group(1), m.group(2)): m.group(3).strip() for m in COL_COMMENT_RE.finditer(sql)
    }
    titles = section_titles(sql)

    tables: dict[str, dict] = {}
    order: dict[str, list[str]] = {}
    for m in CREATE_RE.finditer(sql):
        name, body = m.group(1), m.group(2)
        columns, pk = [], []
        for raw in body.splitlines():
            line = raw.strip()
            if not line or line.startswith("--"):
                continue
            pk_m = re.match(r"PRIMARY KEY\s*\((.*?)\)", line)
            if pk_m:
                pk = split_csv(pk_m.group(1))
                continue
            cm = COL_RE.match(line)
            if not cm:
                raise SystemExit(f"无法解析 {name} 的列定义: {line!r}")
            col, sql_type, rest = cm.group(1), cm.group(2), cm.group(3)
            if "PRIMARY KEY" in rest:
                pk = [col]
            checks = [c.strip() for c in CHECK_RE.findall(rest)]
            default_m = DEFAULT_RE.search(rest)
            column = {
                "name": col,
                "sql_type": sql_type,
                "not_null": "NOT NULL" in rest or col in pk,
                "default": default_m.group(1) if default_m else None,
                "checks": checks,
                "meaning": col_meanings.get((name, col), ""),
            }
            columns.append(column)
            order.setdefault(name, []).append(col)
        # 外键/serial 之类不在这批表里，出现即报错，避免静默丢列
        tables[name] = {
            "title": titles.get(name, name),
            "purpose": purposes.get(name, ""),
            "primary_key": pk,
            "columns": columns,
        }

    seeds: dict[str, list[dict]] = {}
    seed_cols: dict[str, list[str]] = {}
    for m in INSERT_RE.finditer(sql):
        name = m.group(1)
        cols = split_csv(m.group(2))
        seed_cols[name] = cols
        rows = []
        for tuple_text in split_tuples(m.group(3)):
            values = split_csv(tuple_text)
            if len(values) != len(cols):
                raise SystemExit(f"srv.{name} 种子行 {tuple_text!r} 有 {len(values)} 值，"
                                 f"INSERT 声明 {len(cols)} 列")
            for v in values:
                if v.count("'") % 2 != 0:
                    raise SystemExit(f"srv.{name} 种子值 {v!r} 的引号不闭合——多半是字符串里"
                                     f"含逗号把 split_csv 切坏了；先改用不含逗号的种子值，"
                                     f"或给解析器加逗号感知")
            rows.append(dict(zip(cols, values)))
        seeds[name] = rows
    return tables, seeds, seed_cols


def build_docs(files: list[tuple[str, str]]) -> tuple[dict, list[dict]]:
    """把多个迁移的 `srv.*` 合成一份文档（按迁移版本序）。"""
    tables: dict[str, dict] = {}
    seeds: dict[str, list[dict]] = {}
    seed_cols: dict[str, list[str]] = {}
    ddl_of: dict[str, str] = {}
    for rel, sql in files:
        t, s, sc = parse(sql)
        for name in t:
            if name in tables:
                raise SystemExit(f"srv.{name} 在多个迁移里重复建表（{ddl_of[name]} 与 {rel}）")
            ddl_of[name] = rel
        tables.update(t)
        seeds.update(s)
        seed_cols.update(sc)

    index_tables, docs = [], []
    for name, tbl in tables.items():
        cols = tbl["columns"]
        table_id = f"srv.{name}"
        ddl = ddl_of[name]
        rows = seeds.get(name, [])
        known = {c["name"] for c in cols}
        unknown = [c for c in seed_cols.get(name, []) if c not in known]
        if unknown:
            raise SystemExit(f"{table_id} 种子插入了不存在的列: {unknown}")
        docs.append(
            {
                "id": table_id,
                "slug": name,
                "title": tbl["title"],
                "kind": "server_config",
                "status": "complete",
                "ddl": ddl,
                "generated_by": GEN_BY,
                "note": NOTE.replace("<ddl>", ddl),
                "purpose": tbl["purpose"],
                "primary_key": tbl["primary_key"],
                "columns": cols,
                "seed_columns": seed_cols.get(name, []),
                "seed_rows": rows,
            }
        )
        index_tables.append(
            {
                "id": table_id,
                "slug": name,
                "title": tbl["title"],
                "ddl": ddl,
                "columns": len(cols),
                "seed_rows": len(rows),
                "purpose": tbl["purpose"],
            }
        )
    index = {
        "id": "srv",
        "title": "服务端配置表 srv.*",
        "kind": "server_config",
        "ddl": [rel for rel, _ in files],
        "generated_by": GEN_BY,
        "generated": date.today().isoformat(),
        "intro": INTRO,
        "tables": index_tables,
    }
    return index, docs


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    files = srv_sql_files()
    index, docs = build_docs(files)
    # generated 日期不参与一致性判定，否则 --check 每天都会报「不一致」
    index.pop("generated", None)

    wanted = {OUT_DIR / "index.json": dump(index)}
    for doc in docs:
        wanted[OUT_DIR / "tables" / f"{doc['slug']}.json"] = dump(doc)

    if check:
        problems = []
        for path, text in wanted.items():
            if not path.is_file():
                problems.append(f"缺文件: {path.relative_to(ROOT)}")
                continue
            on_disk = json.loads(path.read_text(encoding="utf-8"))
            on_disk.pop("generated", None)
            if dump(on_disk) != dump(json.loads(text)):
                problems.append(f"内容漂移: {path.relative_to(ROOT)}")
        stale = [
            p
            for p in (OUT_DIR / "tables").glob("*.json")
            if p not in wanted
        ] if (OUT_DIR / "tables").is_dir() else []
        for p in stale:
            problems.append(f"多余文件（SQL 里已无此表）: {p.relative_to(ROOT)}")
        if problems:
            print("srv 文档与迁移 SQL 不一致：")
            for p in problems:
                print("  -", p)
            print(f"修复：python {GEN_BY}")
            return 1
        print(f"srv 文档与迁移一致（{len(docs)} 张表，来源 {', '.join(rel for rel, _ in files)}）")
        return 0

    (OUT_DIR / "tables").mkdir(parents=True, exist_ok=True)
    for path, text in wanted.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    print(f"已生成 {len(docs)} 张 srv 表文档 -> {OUT_DIR.relative_to(ROOT)}")
    for doc in docs:
        print(f"  {doc['id']}: {doc['title']}（{len(doc['columns'])} 列，"
              f"{len(doc['seed_rows'])} 行种子）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""build_gm_catalog.py — 生成 serverv/static/gm_catalog.json（GM 的表说明层）。

GM（serverv/internal/gm）从真库读列、类型、注释与唯一索引，但“这张表是干什么的、
行键为什么是这几列”属于研究结论，不在库里。于是按已有的 cfg_schema.json 惯例，
把说明性字段编译成一个静态 JSON，随 gmd 一起部署：

  db_design/schema/tables/tbl_*.json   game.* 的 purpose / entity / 显式 row_key
  db_design/schema/cfg/tables/*.json   cfg.* 的 purpose / csv_path
  serverv/migrations/*.up.sql          srv.*/core.* 的 COMMENT ON TABLE、
                                       game.* 的 `-- tbl_x: entity=… wire=…` 头注释、
                                       `-- slot 行键来源：…`
  db_design/schema/gm_domains.json     可选：手工指定的玩法域覆盖（存在才读）

输出只含说明字段；列定义与注释一律以真库为准（避免两处漂移）。
`game.*` 里**旧库有声明、新库不建表**的条目带 `retired` 标记与理由（退役/派生/战斗期/
从没建过），免得读这份 JSON 的人把它们当成现役表。

用法：
    python db_design/tools/build_gm_catalog.py           # 写盘
    python db_design/tools/build_gm_catalog.py --check   # 只校验是否一致（门禁用）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVERV = ROOT / "serverv"
DB_DESIGN = ROOT / "db_design"
SCHEMA = DB_DESIGN / "schema"
OUT = SERVERV / "static" / "gm_catalog.json"
DOMAIN_OVERRIDES = SCHEMA / "gm_domains.json"

HOMING = SCHEMA / "homing"
OVERRIDES = HOMING / "_overrides.json"
HOMING_OBJECTS = HOMING / "objects"
LEGACY_EVIDENCE = SCHEMA / "_meta" / "legacy_evidence.json"

HEADER_RE = re.compile(r"^--\s+(?P<name>[^:]+):\s+(?P<body>.*)$")
ENTITY_RE = re.compile(r"entity=(?P<entity>[A-Za-z0-9_]+)")
WIRE_RE = re.compile(r"wire=(?P<wire>[^;\s]+)")
MULTI_RE = re.compile(r"多行\((?P<key>[^)]+)\)")
FIELD_RE = re.compile(r"字段列=(?P<n>\d+)")
CHILD_RE = re.compile(r"子表=(?P<n>\d+)")
SLOT_SRC_RE = re.compile(r"^--\s*slot 行键来源：\s*(?P<note>.+?)\s*$")
ROWKEY_SRC_RE = re.compile(r"^--\s*行键来源：\s*(?P<note>.+?)\s*$")
CREATE_RE = re.compile(r"^CREATE TABLE\s+(?:IF NOT EXISTS\s+)?(?P<schema>\w+)\.(?P<table>\w+)")
# 1:1 嵌套子表的头注释（`-- news.avatar: 内嵌复合体 avatar（18B）→ 1:1 子表`）。
# 与「元素数组」（数组→子表）是两种形状，解析要分别认，否则这类子表在
# catalog 里**整条缺失**（GM 里点得到表、却没有用途与行键说明）。
NESTED_1TO1_RE = re.compile(r"内嵌复合体\s*(?P<member>\w+)（(?P<wire>[^）]*)）→\s*1:1\s*子表")

# core.* 没有 COMMENT ON TABLE，这里按表语义手写一句（值以迁移 DDL 为准）。
CORE_PURPOSES = {
    "core.accounts": "账号主表：登录名、密码哈希、角色、封禁与找回密钥",
    "core.worlds": "世界（服）列表：开关与每服 config",
    "core.pilot_registry": "账号 ↔ 飞行员归属登记（world_id + pilot_id）",
    "core.sessions": "登录会话：token 哈希与过期时间",
    "core.login_log": "登录日志：时间、IP、成败与详情",
    "core.pilot_meta": "飞行员改名/删除元数据 + 信封上的单值字段（教程步进/标志、充值点 MB）："
                       "名字唯一性、冷却、删除倒计时与 charge_point",
}


def load_overrides() -> dict[str, str]:
    if not DOMAIN_OVERRIDES.is_file():
        return {}
    raw = json.loads(DOMAIN_OVERRIDES.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in raw.items()}


def retired_notes() -> dict[str, dict]:
    """`game.*` 里「旧库有声明、新库不建表」的表 → 一句「为什么没了」。

    catalog 是按**旧库表声明**（`schema/_legacy_tables/tbl_*.json`）建的，所以退场表会
    留下「有说明、没有这张表」的条目：GM 里点不到（它按真库 introspection），但读这份
    JSON 的人或按 catalog 生成文档的脚本会把它们当成现役表。这里逐条补 `retired` 标记，
    理由按「越具体越优先」取：

      1. `_overrides.json.disposition.<对象>`（批 17 的逐对象裁决：DERIVED/EVENT/CONFIG）；
      2. 归位对象自己的 `disposition` + `no_table_reason`（引擎自动判的非 PERSIST）；
      3. `_overrides.json.retire_tables`（同一批行被并进另一张表，如 `pcard` → `pilot`）；
      4. 冻结的旧库证据 `live.exists=false`（旧库也没建过这张表，纯声明遗留）。
    """
    out: dict[str, dict] = {}

    def put(key: str, kind: str, note: str) -> None:
        if key.startswith("game.") and key not in out and note:
            out[key] = {"kind": kind, "note": note}

    ov: dict = {}
    if OVERRIDES.is_file():
        ov = json.loads(OVERRIDES.read_text(encoding="utf-8"))

    disp_ov = {k: v for k, v in (ov.get("disposition") or {}).items()
               if not str(k).startswith("_") and isinstance(v, dict)}
    # 折叠目标：退场登记里没写 `reason` 的那些（`pcard`/`pilots_list`），
    # 从 `fold` 段查出「行并进了哪个对象」，说明才不是一句空话。
    fold_as: dict[str, str] = {}
    for g in ov.get("fold") or []:
        if not isinstance(g, dict):
            continue
        target = str(g.get("as") or "").strip()
        for c in g.get("composites") or []:
            if target:
                fold_as.setdefault(str(c), target)

    def render(kind: str, why: str) -> str:
        why = why.strip()
        return f"新库不建此表（{kind}）：{why}" if why else f"新库不建此表（{kind}）"

    if HOMING_OBJECTS.is_dir():
        for path in sorted(HOMING_OBJECTS.glob("*.json")):
            o = json.loads(path.read_text(encoding="utf-8"))
            stem = str(o.get("legacy_table") or "").removeprefix("tbl_")
            if not stem:
                continue
            key = f"game.{stem}"
            spec = disp_ov.get(str(o.get("id")))
            if spec:
                as_ = str(spec.get("as") or "").strip() or "no_table"
                put(key, as_, render(as_, str(spec.get("reason") or "")))
                continue
            disp = str(o.get("disposition") or "")
            if disp and disp != "PERSIST":
                why = str(o.get("no_table_reason") or "").strip()
                if why.startswith("disposition=") and "：" in why:
                    why = why.split("：", 1)[1].strip()
                put(key, disp, render(disp, why))

    for e in ov.get("retire_tables") or []:
        if not isinstance(e, dict):
            continue
        table = str(e.get("table") or "")
        why = str(e.get("reason") or "").strip()
        if not why:
            target = fold_as.get(table.removeprefix("game."))
            why = (f"同一批行并进 `{target}`，见 _overrides.json.fold "
                   f"（同一张线形留两张表必然漂移）。" if target
                   else str(e.get("evidence") or "").split("。")[0].strip() + "。")
        put(table, "folded", render("已退场，行并进别的表", why))

    if LEGACY_EVIDENCE.is_file():
        ev = json.loads(LEGACY_EVIDENCE.read_text(encoding="utf-8")).get("tables") or {}
        for stem, node in ev.items():
            if (node.get("live") or {}).get("exists") is False:
                put(f"game.{stem}", "never_live",
                    "旧库也没建过这张表（声明里有、库里没有，见 schema/_meta/legacy_evidence.json）；"
                    "新库同样不建")

    return out


def parse_migrations() -> tuple[dict[str, dict], dict[str, str], set[str]]:
    """返回 (每张 game 表的说明, 每张带 COMMENT ON TABLE 的表的用途, 真被建出来的表)。

    迁移由 gen_migration 生成，表头注释即研究结论的机器可读投影。
    """
    game_notes: dict[str, dict] = {}
    table_comments: dict[str, str] = {}
    live_tables: set[str] = set()
    for path in sorted(SERVERV.glob("migrations/*.up.sql")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        current_create = ""
        pending_note: dict = {}
        for i, line in enumerate(lines):
            stripped = line.strip()
            m = CREATE_RE.match(stripped)
            if m:
                current_create = f"{m.group('schema')}.{m.group('table')}"
                live_tables.add(current_create)
                if current_create.startswith("game.") and pending_note:
                    game_notes.setdefault(current_create, {}).update(pending_note)
                pending_note = {}
                continue
            cm = re.match(r"^COMMENT ON TABLE\s+(\w+)\.(\w+)\s+IS\s+'(?P<text>.*)';\s*$", stripped)
            if cm:
                table_comments[f"{cm.group(1)}.{cm.group(2)}"] = cm.group("text").replace("''", "'")
                continue
            slot = SLOT_SRC_RE.match(stripped) or ROWKEY_SRC_RE.match(stripped)
            if slot and current_create.startswith("game."):
                prefix = "slot 行键来源：" if SLOT_SRC_RE.match(stripped) else "行键来源："
                note = game_notes.setdefault(current_create, {})
                # 两类行键说明可能同时存在（`item`：声明行键 slot + slot 值来自
                # inv_place），都留着——GM 的表说明要能回答「这个 slot 从哪来」。
                note["row_key_note"] = (
                    note["row_key_note"] + "；" if note.get("row_key_note") else "") \
                    + prefix + slot.group("note")
                continue
            hm = HEADER_RE.match(stripped)
            if not hm:
                continue
            name, body = hm.group("name").strip(), hm.group("body").strip()
            # 表头形如 `-- clan_eff: entity=clan_eff wire=11B; 多行(行键=clan_id); 字段列=5`，
            # 其中 `name` 是 gen_migration 的 `plan.table_id`（旧产物写作 `tbl_<name>`，
            # 这里两种都认；要求是「像表 id 的单个词」，免得把说明性散文当成表头）。
            if body.startswith("entity=") and re.fullmatch(r"(?:tbl_)?[\w.]+", name):
                note: dict = {}
                if em := ENTITY_RE.search(body):
                    note["entity"] = em.group("entity")
                if wm := WIRE_RE.search(body):
                    note["wire"] = wm.group("wire")
                shape = []
                if mm := MULTI_RE.search(body):
                    key = mm.group("key")
                    # 现行表头是 `多行(行键=clan_id)`；旧产物是 `多行(slot)`。
                    shape.append(f"多行（{key}）" if key.startswith("行键=")
                                 else f"多行（{key} 槽）")
                elif "单行" in body:
                    shape.append("单行")
                if fm := FIELD_RE.search(body):
                    shape.append(f"{fm.group('n')} 个字段列")
                if chm := CHILD_RE.search(body):
                    shape.append(f"{chm.group('n')} 张子表")
                if shape:
                    note["note"] = "；".join(shape)
                pending_note = note
            elif "元素数组" in body or body.startswith("嵌套"):
                # 子表头：-- bracket.nodes: 元素数组 15×11B（bracket_node）→ 子表
                parent, _, member = name.partition(".")
                note = pending_note if pending_note else {}
                note = dict(note, note=(note.get("note", "") + "；" if note.get("note") else "") + body)
                if parent and member:
                    game_notes.setdefault(f"game.{parent}__{member}", {}).update({"note": note["note"]})
            elif NESTED_1TO1_RE.search(body):
                # 1:1 嵌套子表头：-- news.avatar: 内嵌复合体 avatar（18B）→ 1:1 子表
                # 与「元素数组」是两种形状（一个是数组→子表、一个是定长嵌套→1:1 子表），
                # 漏认会让这类子表在 catalog 里整条缺失。
                parent, _, member = name.partition(".")
                if parent and member:
                    ckey = f"game.{parent}__{member}"
                    prev = game_notes.setdefault(ckey, {})
                    prev["note"] = (prev["note"] + "；" if prev.get("note") else "") + body
        if current_create.startswith("game.") and pending_note:
            game_notes.setdefault(current_create, {}).update(pending_note)
    return game_notes, table_comments, live_tables


def build() -> dict:
    overrides = load_overrides()
    game_notes, table_comments, live_tables = parse_migrations()
    retired = retired_notes()
    tables: dict[str, dict] = {}

    def entry(key: str) -> dict:
        return tables.setdefault(key, {})

    for path in sorted((SCHEMA / "_legacy_tables").glob("tbl_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        table = str(doc.get("id", ""))[len("tbl_"):]
        if not table:
            continue
        key = f"game.{table}"
        e = entry(key)
        if doc.get("purpose"):
            e["purpose"] = doc["purpose"]
        if doc.get("entity_ref"):
            e["entity"] = doc["entity_ref"]
        rk = doc.get("row_key") or {}
        if rk.get("columns"):
            cols = ", ".join(str(c) for c in rk["columns"])
            reason = (rk.get("reason") or "").strip()
            note = f"行键追加 {cols}"
            if reason:
                note += f"（{reason}）"
            if rk.get("evidence_va"):
                note += f" 证据 {rk['evidence_va']}"
            e["row_key_note"] = note

    for path in sorted((SCHEMA / "cfg" / "tables").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        table = str(doc.get("id", ""))
        if not table:
            continue
        e = entry(f"cfg.{table}")
        if doc.get("purpose"):
            e["purpose"] = doc["purpose"]

    for key, note in game_notes.items():
        e = entry(key)
        for field in ("entity", "wire", "row_key_note"):
            if note.get(field) and not e.get(field):
                e[field] = note[field]
        if note.get("note"):
            e["note"] = (e.get("note", "") + "；" if e.get("note") else "") + note["note"]

    for key, comment in table_comments.items():
        e = entry(key)
        if not e.get("purpose"):
            e["purpose"] = comment

    for key, purpose in CORE_PURPOSES.items():
        e = entry(key)
        e.setdefault("purpose", purpose)

    # 子表（xxx__yyy）没有自己的 purpose，继承父表的，并标出成员名。
    for key in list(tables):
        if tables[key].get("purpose"):
            continue
        parent, sep, member = key.partition("__")
        if not sep:
            continue
        parent_purpose = tables.get(parent, {}).get("purpose")
        if parent_purpose:
            tables[key]["purpose"] = f"{parent_purpose}〔子表 {member}〕"

    for key, domain in overrides.items():
        tables.setdefault(key, {})["domain"] = domain

    # 现役 game 表（DDL 真建出来的）以真库为准；其余 game.* 是旧库声明留下的条目 ——
    # 打 `retired` 标记，别让读 JSON 的人把它们当现役表。
    for key, e in tables.items():
        if not key.startswith("game.") or key in live_tables:
            continue
        hint = retired.get(key) or {
            "kind": "unknown",
            "note": "新库不建此表，且原因未登记（见 db_design 归位模型与 docs/05 §9）",
        }
        e["retired"] = True
        e["retired_kind"] = hint["kind"]
        e["retired_note"] = hint["note"]

    return {
        "note": "由 db_design/tools/build_gm_catalog.py 生成；GM 只取用途/行键说明，"
                "列定义与注释以数据库为准。玩法域可用 schema/gm_domains.json 覆盖。"
                "带 `retired=true` 的条目是旧库有声明、新库不建的表（理由见 `retired_note`），"
                "真库里没有它们，GM 也读不到。",
        "tables": dict(sorted(tables.items())),
    }


def live_without_notes(catalog: dict) -> list[str]:
    """现役 `game.*` 表里没有说明条目的（应为空：DDL 每张表都有头注释）。

    这一门防的是「头注释形状变了、解析器不认」——表在 GM 里能点开、用途却是空的。
    """
    text = ";".join(p.read_text(encoding="utf-8")
                    for p in sorted(SERVERV.glob("migrations/*.up.sql")))
    live = {f"{m.group('schema')}.{m.group('table')}"
            for line in text.splitlines() if (m := CREATE_RE.match(line.strip()))}
    return sorted(t for t in live if t.startswith("game.") and t not in catalog["tables"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只校验不写盘")
    args = parser.parse_args()

    catalog = build()
    if len(catalog["tables"]) < 100:
        print(f"WARN: 只解析到 {len(catalog['tables'])} 张表的说明，疑似来源文件缺失",
              file=sys.stderr)
    missing = live_without_notes(catalog)
    if missing:
        print(f"WARN: {len(missing)} 张现役 game 表没有说明条目（头注释形状可能变了）："
              f"{', '.join(missing)}", file=sys.stderr)
    text = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print(f"{OUT} 与来源不一致，请重跑 build_gm_catalog.py", file=sys.stderr)
            return 1
        print(f"gm catalog OK ({len(catalog['tables'])} tables)")
        return 0

    OUT.write_text(text, encoding="utf-8")
    print(f"gm catalog -> {OUT} ({len(catalog['tables'])} tables)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

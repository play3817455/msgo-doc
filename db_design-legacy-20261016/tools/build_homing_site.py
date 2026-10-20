#!/usr/bin/env python3
"""归位库站点（新库设计）：读 `schema/homing/` + 生成的 `0003` DDL，渲染只读 HTML。

与 `build_cfg_site.py` 同款：只接收 `page()` 构造器，不反向 import `build_site`。

渲染的六件事（对应 docs/05 §7 的 P3–P6 成果）：

  homing/index.html      对象/表总览 + 角色词表 + 类型映射 + 未建表对象
  homing/coverage.html   归位覆盖率（正向：每列有出处；反向：不落库成员有理由）
  homing/relations.html  外键 / 主数据引用 / 未决引用
  homing/unresolved.html 未决清单（渲染引擎产出的 unresolved.md）
  homing/objects/*.html  单对象：视图 + 每张表的列（含 DDL 类型与出处）+ 关联 + 命令

DDL 是「落库事实」，homing JSON 是「归位推理」，两边都渲染，漂移一眼可见。
"""

from __future__ import annotations

import collections
import html
import json
import re
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DB_DESIGN = TOOLS_DIR.parent
SCHEMA_DIR = DB_DESIGN / "schema"
HOMING_DIR = SCHEMA_DIR / "homing"
SITE_DIR = DB_DESIGN / "site"
DDL_PATH = DB_DESIGN.parent / "serverv" / "migrations" / "0003_game_persist.up.sql"

ROLE_COLORS = {
    "identity": "#2e7d32",
    "scope": "#1565c0",
    "slot": "#00838f",
    "ref": "#6a1b9a",
    "counter": "#ef6c00",
    "flag": "#5d4037",
    "timestamp": "#ad1457",
    "attribute": "#455a64",
    "padding": "#9e9e9e",
    "payload": "#c62828",
    "": "#9e9e9e",
}
SHAPE_LABELS = {
    "root": "根表",
    "child": "数组子表",
    "nested": "内嵌子表",
    "value": "取值结构",
}
DISPOSITION_COLORS = {
    "PERSIST": "#2e7d32",
    "EVENT": "#c62828",
    "TBD": "#757575",
    "COMPOSITE": "#455a64",
}


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def load_json(path: Path, default=None):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def badge(text: str, color: str) -> str:
    if not text:
        return ""
    return f'<span class="badge" style="background:{color}">{esc(text)}</span>'


def role_badge(role: str) -> str:
    return badge(role or "—", ROLE_COLORS.get(role, "#9e9e9e"))


def disp_badge(d: str) -> str:
    return badge(d or "—", DISPOSITION_COLORS.get(d, "#757575"))


def shape_label(shape: str, parent_table: str = "") -> str:
    lbl = SHAPE_LABELS.get(shape, shape or "—")
    return f'{esc(lbl)}' + (f' <span class="muted">← {esc(parent_table)}</span>' if parent_table else "")


def code_list(values) -> str:
    return "".join(f"<code>{esc(v)}</code> " for v in (values or [])) or '<span class="muted">—</span>'


# ------------------------------------------------------------------ DDL 解析

_STOP = {"NOT", "NULL", "DEFAULT", "PRIMARY", "UNIQUE", "REFERENCES", "CHECK", "CONSTRAINT"}


def load_ddl(path: Path) -> tuple[dict, dict, dict]:
    """→ (表→列→{type,not_null,pk}, 表→列→注释, 表→[(索引名, 列)])"""
    if not path.is_file():
        return {}, {}, {}
    text = path.read_text(encoding="utf-8")
    cols: dict[str, dict] = {}
    comments: dict[str, dict] = {}
    indexes: dict[str, list] = {}

    for m in re.finditer(r"CREATE TABLE (game\.\w+) \((.*?)\n\);", text, re.S):
        tbl, body = m.group(1), m.group(2)
        entry: dict[str, dict] = {}
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.startswith("--"):
                continue
            toks = line.split()
            name = toks[0].strip('"')
            typ_toks = []
            for t in toks[1:]:
                if t.upper() in _STOP:
                    break
                typ_toks.append(t)
            entry[name] = {
                "type": " ".join(typ_toks),
                "not_null": "NOT NULL" in line,
                "pk": "PRIMARY KEY" in line,
            }
        cols[tbl] = entry

    for m in re.finditer(r"COMMENT ON COLUMN (game\.\w+)\.(\"?[\w]+\"?) IS '(.*?)';", text, re.S):
        comments.setdefault(m.group(1), {})[m.group(2).strip('"')] = m.group(3)

    for m in re.finditer(r"CREATE UNIQUE INDEX (\w+) ON (game\.\w+) \(([^)]*)\);", text):
        indexes.setdefault(m.group(2), []).append(
            (m.group(1), [c.strip().strip('"') for c in m.group(3).split(",")]))
    return cols, comments, indexes


def load_objects() -> dict[str, dict]:
    out = {}
    for p in sorted((HOMING_DIR / "objects").glob("*.json")):
        d = load_json(p, {})
        out[d.get("id", p.stem)] = d
    return out


# ------------------------------------------------------------------ 总览页

def build_homing_index(summary: dict, roles: dict, objects: dict,
                       ddl_cols: dict, tables_of: dict, change_counts: dict) -> str:
    stats = [
        ("对象", summary.get("objects", 0)),
        ("根对象", summary.get("objects_root", 0)),
        ("PERSIST 对象", summary.get("objects_persist", 0)),
        ("折入对象复合体", summary.get("composites_folded", 0)),
        ("线上成员", summary.get("members_total", 0)),
        ("落库成员", summary.get("members_persist", 0)),
        ("期望列", summary.get("columns_expected", 0)),
        ("建表数", len(ddl_cols)),
        ("对象关联", summary.get("relations", 0)),
        ("主数据引用", summary.get("master_refs", 0)),
        ("运行时句柄", summary.get("runtime_refs", 0)),
        ("未决引用", summary.get("ref_unresolved", 0)),
        ("孪生已裁决", (summary.get("gates") or {}).get("twins_reviewed", 0)),
    ]
    stat_html = "".join(
        f'<div class="stat"><div class="num">{esc(v)}</div><div class="lbl">{esc(k)}</div></div>'
        for k, v in stats)

    cov = summary.get("coverage", {})
    gates = [
        ("复合体全折入", cov.get("composites_folded") == cov.get("composites_total"),
         f'{cov.get("composites_folded")}/{cov.get("composites_total")}'),
        ("无出处成员归零", not cov.get("members_unjustified"),
         f'unjustified {cov.get("members_unjustified", 0)} · 已知缺口 {cov.get("members_known_gap", 0)}'),
        ("每列带 VA", True, f'members_without_va {cov.get("members_without_va", 0)}（有 ref 出处可替）'),
        ("行键不变量", True, f'根 PERSIST {cov.get("roots_persist")} · 无身份根 {len(cov.get("roots_without_pk", []))}（未决，非失败）'),
        ("同形孪生逐组裁决", (summary.get("gates") or {}).get("unlinked_layout_twins", 0) == 0,
         f'已裁 {(summary.get("gates") or {}).get("twins_reviewed", 0)} 组 · '
         f'未裁 {(summary.get("gates") or {}).get("unlinked_layout_twins", 0)} 组'
         f'（明细见未决清单 §8）'),
    ]
    gate_html = "".join(
        f'<li>{"✓" if ok else "✗"} <strong>{esc(name)}</strong> <span class="muted">{esc(note)}</span></li>'
        for name, ok, note in gates)

    role_rows = ""
    for name, note in (roles.get("roles") or {}).items():
        role_rows += (f'<tr><td>{role_badge(name)}</td><td><code>{esc(name)}</code></td>'
                      f'<td>{esc(note)}</td><td>{(roles.get("role_counts") or {}).get(name, 0)}</td></tr>')
    maps = "".join(f'<tr><td><code>{esc(k)}</code></td><td><code>{esc(v)}</code></td></tr>'
                   for k, v in sorted((roles.get("wire_to_pg") or {}).items()))
    go_maps = "".join(f'<tr><td><code>{esc(k)}</code></td><td><code>{esc(v)}</code></td></tr>'
                      for k, v in sorted((roles.get("wire_to_go") or {}).items()))
    opaque = "".join(f'<tr><td>{esc(k)} 字节</td><td><code>{esc(v)}</code></td></tr>'
                     for k, v in sorted((roles.get("opaque_pg") or {}).items(), key=lambda kv: int(kv[0])))

    # 建表清单
    rows = []
    for name in sorted(ddl_cols):
        meta = tables_of.get(name)
        oid, tbl = (meta or (None, None))[0], (meta or (None, None))[1]
        if oid is None:
            rows.append(f'<tr><td><code>{esc(name)}</code></td><td colspan="6" class="muted">'
                        f'DDL 里有、homing 里没有对应对象（需查）</td></tr>')
            continue
        obj = objects[oid]
        pk = ", ".join(tbl.get("primary_key") or [])
        ev = change_counts.get(name, (0, 0))
        rows.append(
            f'<tr><td><code>{esc(name)}</code></td>'
            f'<td><a href="objects/{esc(oid)}.html"><code>{esc(oid)}</code></a></td>'
            f'<td>{shape_label(tbl.get("shape", ""), tbl.get("parent_table", ""))}</td>'
            f'<td>{esc(pk)}</td>'
            f'<td>{len(ddl_cols[name])}</td>'
            f'<td>{esc(obj.get("domain", ""))}</td>'
            f'<td>{ev[0]} / {ev[1]}</td></tr>')

    unbuilt = []
    for oid, obj in sorted(objects.items()):
        tblname = obj.get("table") or ""
        if obj.get("shape") != "root":
            continue
        if obj.get("disposition") != "PERSIST":
            reason = obj.get("no_table_reason") or "非 PERSIST，不建表"
            unbuilt.append(f'<li><a href="objects/{esc(oid)}.html"><code>{esc(oid)}</code></a> '
                           f'{disp_badge(obj.get("disposition"))} '
                           f'<span class="muted">{esc(obj.get("title", ""))} · {esc(reason)}</span></li>')
        elif tblname and tblname not in ddl_cols:
            unbuilt.append(f'<li><code>{esc(tblname)}</code> · <a href="objects/{esc(oid)}.html">'
                           f'<code>{esc(oid)}</code></a> {disp_badge(obj.get("disposition"))} '
                           f'<span class="muted">{esc(obj.get("title", ""))} · 模型建了表但 0003 里没有</span></li>')

    body = f"""
    <h2>归位库（新库设计）</h2>
    <p class="lead">三层模型：<strong>L1 域</strong>（capabilities）→ <strong>L2 对象</strong>（折复合体，含多视图）
      → <strong>L3 角色</strong>（身份/作用域/槽位/引用/属性…）。DDL 与 Go store 都由这套对象生成，
      旧 <code>schema/_legacy_tables/</code> 只作留档。口径见
      <a href="../../docs/05-字段归位与重做库.md">docs/05-字段归位与重做库.md</a>。</p>
    <div class="grid stats">{stat_html}</div>

    <section class="asm-panel">
      <h3>归位门</h3>
      <ul>{gate_html}</ul>
      <p class="muted">未决清单见 <a href="unresolved.html">未决清单</a>；逐列出处见
        <a href="coverage.html">归位覆盖率</a>；引用解析见 <a href="relations.html">关联</a>。</p>
    </section>

    <h3>角色词表（L3）</h3>
    <table>
      <thead><tr><th>角色</th><th>代码</th><th>落库口径</th><th>成员数</th></tr></thead>
      <tbody>{role_rows}</tbody>
    </table>

    <h3>类型映射</h3>
    <table class="srv-table" style="float:none">
      <thead><tr><th>wire</th><th>PG</th></tr></thead><tbody>{maps}</tbody>
    </table>
    <table class="srv-table" style="float:none">
      <thead><tr><th>wire</th><th>Go</th></tr></thead><tbody>{go_maps}</tbody>
    </table>
    <table class="srv-table" style="float:none">
      <thead><tr><th>语义未定块</th><th>PG（禁 BYTEA）</th></tr></thead><tbody>{opaque}</tbody>
    </table>

    <h3>建表清单（{len(ddl_cols)} 张 · 来自 0003）</h3>
    <p class="muted">「写 / 读」= 该表的对象在 CS 命令里被写的条数 / SC 命令里被读的条数。</p>
    <table>
      <thead><tr><th>表</th><th>对象</th><th>形态</th><th>主键（自然键）</th><th>列数</th><th>域</th><th>写/读</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table>

    <h3>归位为「不建表」的根对象（{len(unbuilt)}）</h3>
    <p class="muted">线上只有 EVENT/TBD 生命周期，战斗持久化属 B6，本轮不建表。</p>
    <ul>{"".join(unbuilt) or '<li class="muted">无</li>'}</ul>
    """
    return body


# ------------------------------------------------------------------ 对象页

def _member_index(obj: dict) -> dict:
    return {m.get("name", ""): m for m in obj.get("members", [])}


def _column_row(oid: str, tblname: str, col: dict, member: dict, ddl_cols: dict,
                comments: dict, existing_cmds: set[str]) -> str:
    ddl = (ddl_cols.get(tblname) or {}).get(col.get("column", ""))
    typ = ddl["type"] if ddl else "—"
    if ddl and ddl.get("not_null"):
        typ += " NOT NULL"
    wire = col.get("wire_type", "")
    length = member.get("length", "") if member else ""
    meaning = (member or {}).get("meaning", "")
    comment = (comments.get(tblname) or {}).get(col.get("column", ""), "")
    va = (member or {}).get("evidence_va", "") or ""
    ref = (member or {}).get("evidence_ref") or {}
    cmd = ref.get("command", "")
    if cmd and cmd in existing_cmds:
        ev = f'<a href="../../commands/{esc(cmd)}.html"><code>{esc(cmd)}</code></a>'
    elif cmd:
        ev = f'<code>{esc(cmd)}</code>'
    else:
        ev = ""
    if va:
        ev += f' <span class="muted">@{esc(va)}</span>'
    if not ev:
        ev = '<span class="muted">行键合成</span>' if col.get("synthetic") else '<span class="muted">—</span>'
    notes = []
    if col.get("synthetic"):
        notes.append("行键合成")
    if col.get("pk"):
        notes.append("PK")
    if member and member.get("memory_only"):
        notes.append("memory_only")
    if member and (member.get("lifetime") or "") not in ("", "PERSIST"):
        notes.append(f'lifetime={member.get("lifetime")}')
    wire_alias = ""
    if col.get("member") and col.get("member") != col.get("column"):
        wire_alias = f' <span class="muted">（线名 {esc(col.get("member"))}）</span>'
    note_txt = f' <span class="muted">{esc(" · ".join(notes))}</span>' if notes else ""
    return (f'<tr><td><code>{esc(col.get("column", ""))}</code>{wire_alias}{note_txt}</td>'
            f'<td><code>{esc(typ)}</code></td>'
            f'<td>{role_badge(col.get("role", ""))}</td>'
            f'<td><code>{esc(wire)}</code>{f" · {esc(length)}B" if length != "" else ""}</td>'
            f'<td>{esc(meaning)}</td>'
            f'<td class="muted">{esc(comment)}</td>'
            f'<td>{ev}</td></tr>')


def build_object_page(oid: str, obj: dict, objects: dict, ddl_cols: dict, comments: dict,
                      indexes: dict, relations: dict, existing_cmds: set[str]) -> str:
    nav_key = f"homing/objects/{oid}.html"
    members = _member_index(obj)
    keys = obj.get("keys") or {}
    views = obj.get("views") or []

    head = [
        ("对象", f'<code>{esc(oid)}</code>'),
        ("形态", shape_label(obj.get("shape", ""))),
        ("L1 域", f'{esc(obj.get("domain", ""))} '
                  f'<span class="muted">{esc(json.dumps(obj.get("domain_votes") or {}, ensure_ascii=False))}</span>'),
        ("生命周期", disp_badge(obj.get("disposition", ""))),
        ("旧表锚点", f'<code>{esc(obj.get("legacy_table", ""))}</code>' if obj.get("legacy_table") else '<span class="muted">—</span>'),
        ("身份列", code_list(obj.get("identity"))),
        ("主键", code_list(keys.get("primary_key"))),
        ("主键类别", f'<code>{esc(keys.get("pk_kind", ""))}</code>'),
        ("作用域", code_list(keys.get("scope"))),
        ("数组子表键", code_list(keys.get("child_key"))),
        ("内嵌成员", code_list(keys.get("nested"))),
        ("父对象", code_list(obj.get("parents"))),
        ("线视图", "".join(f'<code>{esc(v.get("composite", ""))}</code> ' for v in views) or '<span class="muted">—</span>'),
    ]
    # 折叠族（`_overrides.json.fold`，docs/05 §9.9）：宿主线体（行模型用的那一形）与
    # 一起折进来的其它形——它们不另建表，列并进宿主对象的并集。
    if obj.get("wire_body"):
        folded = [c for c in (obj.get("folded_composites") or []) if c != obj.get("wire_body")]
        head.append(("宿主线体", f'<code>{esc(obj.get("wire_body"))}</code>'))
        head.append(("折叠线形", "".join(f'<code>{esc(c)}</code> ' for c in folded)
                              or '<span class="muted">—</span>'))
    head_html = "".join(f"<dt>{esc(k)}</dt><dd>{v}</dd>" for k, v in head)

    view_rows = ""
    for v in views:
        cmds = v.get("commands") or []
        links = "".join(
            (f'<a href="../../commands/{esc(c)}.html"><code>{esc(c)}</code></a> ' if c in existing_cmds
             else f'<code>{esc(c)}</code> ') for c in cmds)
        view_rows += (f'<tr><td><code>{esc(v.get("composite", ""))}</code></td>'
                      f'<td>{esc(v.get("length", ""))} B</td>'
                      f'<td>{esc(v.get("memory_claim", ""))} B</td>'
                      f'<td><code>{esc(v.get("reader", ""))}</code></td>'
                      f'<td><code>{esc(v.get("printer", ""))}</code></td>'
                      f'<td>{len(cmds)} · {links}</td></tr>')

    tbl_html = ""
    for tbl in obj.get("tables", []):
        name = tbl.get("name", "")
        ddl = ddl_cols.get(name)
        uniq = indexes.get(name) or []
        idx_txt = " · ".join(f'<code>{esc(n)}</code> ({esc(", ".join(c))})' for n, c in uniq)
        built = name in ddl_cols
        row_html = ""
        for col in tbl.get("columns", []):
            row_html += _column_row(oid, name, col, members.get(col.get("member", "")), ddl_cols,
                                    comments, existing_cmds)
        extra = tbl.get("key_extra") or []
        tbl_html += f"""
    <section class="col-group">
      <h3><code>{esc(name)}</code> {shape_label(tbl.get("shape", ""), tbl.get("parent_table", ""))}
        {'<span class="badge" style="background:#c62828">未建表</span>' if not built else ''}</h3>
      <p class="muted">自然键 <code>{esc(", ".join(tbl.get("primary_key") or []))}</code>
        {f' · 额外键 {esc(", ".join(extra))}' if extra else ''}
        {f' · 经成员 <code>{esc(tbl.get("via_member"))}</code> 挂到 <code>{esc(tbl.get("parent_table"))}</code>' if tbl.get("parent_table") else ''}
        {f' · 唯一索引 {idx_txt}' if idx_txt else ''}</p>
      <table>
        <thead><tr><th>列</th><th>DDL 类型</th><th>角色</th><th>线类型 / 长</th><th>含义</th><th>DDL 注释（出处）</th><th>归位出处</th></tr></thead>
        <tbody>{row_html or '<tr><td colspan="7" class="muted">无列</td></tr>'}</tbody>
      </table>
    </section>"""

    link_rows = ""
    for l in obj.get("links", []):
        if l.get("view_of_root"):
            # 视图格：`member_rows_in_root` 下这几格不是子表，行的真身在别人的根表里。
            link_rows += (
                f'<tr><td><code>{esc(l.get("member", ""))}</code></td>'
                f'<td><code>view_of_root</code></td>'
                f'<td><code>{esc(l.get("view_of_root", ""))}</code>'
                f' <span class="badge" style="background:#00695c">行在根表</span></td>'
                f'<td>{esc(l.get("count", ""))}</td><td>{esc(l.get("length", ""))}</td>'
                f'<td><code>{esc(l.get("composite", ""))}</code></td>'
                f'<td><span class="muted">{esc(l.get("evidence_va", ""))}</span></td></tr>')
            continue
        link_rows += (
            f'<tr><td><code>{esc(l.get("member", ""))}</code></td><td><code>{esc(l.get("kind", ""))}</code></td>'
            f'<td><code>{esc(l.get("child_table", ""))}</code></td>'
            f'<td>{esc(l.get("count", ""))}</td><td>{esc(l.get("length", ""))}</td>'
            f'<td><code>{esc(l.get("composite", ""))}</code></td><td><span class="muted">{esc(l.get("evidence_va", ""))}</span></td></tr>')

    view_member_rows = ""
    for v in obj.get("view_rows", []):
        va = v.get("evidence_va") or ""
        view_member_rows += (
            f'<li><code>{esc(v.get("member", ""))}</code> → <code>{esc(v.get("root_table", ""))}</code>'
            f'（行键在根对象 <code>{esc(v.get("root_object", ""))}</code>'
            f'{f"，{v.get("count")} 格定长窗口" if v.get("count") else ""}）'
            f'<span class="muted"> · {esc(v.get("reason", ""))}'
            f'{f" · VA {esc(va)}" if va else ""}</span></li>')

    # 引用：出向（本对象 → 别处）
    out_rows, in_rows = "", ""
    for r in relations.get("relations", []):
        if r.get("from", "").split(".")[0] == oid:
            out_rows += (f'<tr><td><code>{esc(r.get("from", ""))}</code></td>'
                         f'<td><code>{esc(r.get("to", ""))}</code></td>'
                         f'<td>{esc(r.get("kind", ""))}</td><td>{esc(r.get("basis", ""))}</td>'
                         f'<td><span class="muted">{esc(r.get("evidence_va", ""))}</span></td></tr>')
        if r.get("to", "").split(".")[0] == oid:
            in_rows += (f'<tr><td><code>{esc(r.get("from", ""))}</code></td>'
                        f'<td><code>{esc(r.get("to", ""))}</code></td>'
                        f'<td>{esc(r.get("kind", ""))}</td>'
                        f'<td><span class="muted">{esc(r.get("evidence_va", ""))}</span></td></tr>')
    master_rows = "".join(
        f'<tr><td><code>{esc(r.get("from", ""))}</code></td><td><code>{esc(r.get("to", ""))}</code></td>'
        f'<td>{esc(r.get("basis", ""))}</td><td><span class="muted">{esc(r.get("evidence_va", ""))}</span></td></tr>'
        for r in relations.get("master_refs", []) if r.get("from", "").split(".")[0] == oid)
    # 本对象若**不建表**（DERIVED/EVENT/CONFIG/TBD），它的出向引用落在 `wire_refs[]`
    # 里：仍然列出（证据不丢），但标出「线上引用」——库里没有源表，建不出外键。
    wire_rows = "".join(
        f'<tr><td><code>{esc(r.get("from", ""))}</code></td><td><code>{esc(r.get("to", ""))}</code></td>'
        f'<td>{esc(r.get("kind", ""))}·线上引用</td><td>{esc(r.get("reason", ""))}</td>'
        f'<td><span class="muted">{esc(r.get("evidence_va", ""))}</span></td></tr>'
        for r in relations.get("wire_refs", []) if r.get("from", "").split(".")[0] == oid)
    dangling_rows = "".join(
        f'<tr><td><code>{esc(r.get("from", ""))}</code></td><td>{esc(r.get("reason", ""))}</td>'
        f'<td><span class="muted">{esc(r.get("evidence_va", ""))}</span></td></tr>'
        for r in relations.get("dangling", []) if r.get("from", "").split(".")[0] == oid)

    excluded_rows = "".join(
        f'<tr><td><code>{esc(c.get("member", ""))}</code></td><td>{role_badge((members.get(c.get("member", "")) or {}).get("role", ""))}</td>'
        f'<td>{esc(c.get("reason", ""))}</td>'
        f'<td><code>{esc((members.get(c.get("member","")) or {}).get("wire_type", ""))}</code></td>'
        f'<td><span class="muted">{esc(c.get("evidence_va", ""))}</span></td></tr>'
        for c in obj.get("columns_excluded", []))

    def _cmd_rows(items):
        out = ""
        for it in items:
            c = it.get("command", "")
            link = (f'<a href="../../commands/{esc(c)}.html"><code>{esc(c)}</code></a>'
                    if c in existing_cmds else f'<code>{esc(c)}</code>')
            # 写方点名登记（docs/05 §9.9）：命令线体里没有这个复合体、只带目标 id，
            # `via` 自然是空的——标成「声明登记 @VA」，别让人误读成「没证据」。
            via = it.get("via", "")
            if it.get("declared_reason"):
                va = it.get("evidence_va") or ""
                via = f"声明登记{(' @' + va) if va else ''}"
            out += (f'<tr><td>{link}</td><td>{esc(it.get("op", ""))}</td>'
                    f'<td><code>{esc(via)}</code></td>'
                    f'<td>{esc(", ".join(it.get("verbs") or []))}</td></tr>')
        return out

    writes_rows = _cmd_rows(obj.get("writes", []))
    reads_rows = _cmd_rows(obj.get("reads", []))
    declared_notes = "".join(
        f'<li><code>{esc(it.get("command", ""))}</code>：{esc(it.get("declared_reason", ""))}'
        f'{(" （VA <code>" + esc(it.get("evidence_va", "")) + "</code>）") if it.get("evidence_va") else ""}</li>'
        for it in (obj.get("writes", []) + obj.get("reads", []))
        if it.get("declared_reason"))

    child_links = "".join(
        f'<li><code>{esc(t.get("name", ""))}</code></li>' for t in obj.get("tables", [])
        if t.get("parent_table") == obj.get("table"))

    body = f"""
    <nav class="breadcrumb"><a href="../index.html">归位库</a> / <span><code>{esc(oid)}</code></span></nav>
    <h2>{esc(obj.get("title") or oid)} {disp_badge(obj.get("disposition", ""))} {role_badge(obj.get("shape", ""))}</h2>
    <section class="asm-panel"><dl class="asm-dl">{head_html}</dl></section>

    <h3>线视图（同一对象在线上可能有多种形态）</h3>
    <table>
      <thead><tr><th>复合体</th><th>线长</th><th>槽宽</th><th>reader</th><th>printer</th><th>命令</th></tr></thead>
      <tbody>{view_rows or '<tr><td colspan="6" class="muted">—</td></tr>'}</tbody>
    </table>

    <h3>落库</h3>
    {tbl_html or (f'<p class="muted">无表 · {esc(obj.get("no_table_reason") or "不落库对象")}'
                  f'（不落库对象，B6 入口见 <a href="../index.html">归位库首页「不建表」清单</a>）</p>'
                  if obj.get("disposition") != "PERSIST"
                  else '<p class="muted">无表（不落库对象）</p>')}

    <h3>子表链接</h3>
    <table><thead><tr><th>成员</th><th>类别</th><th>子表 / 行所在表</th><th>元素数</th><th>元素线长</th><th>复合体</th><th>VA</th></tr></thead>
      <tbody>{link_rows or '<tr><td colspan="7" class="muted">无</td></tr>'}</tbody></table>
    {f'<h3>视图格（行在别人的根表，本表不另存）</h3><ul>{view_member_rows}</ul>' if view_member_rows else ''}

    <h3>外键（出向）</h3>
    <table><thead><tr><th>本列</th><th>目标</th><th>类别</th><th>依据</th><th>VA</th></tr></thead>
      <tbody>{out_rows or wire_rows or '<tr><td colspan="5" class="muted">无</td></tr>'}</tbody></table>
    {f'<p class="muted">本对象不建表（disposition={esc(obj.get("disposition", ""))}），上表是<strong>线上引用</strong>：线体里成立，DDL 建不出外键。</p>' if wire_rows and not out_rows else ''}
    <h3>外键（入向：别人指向我）</h3>
    <table><thead><tr><th>来源列</th><th>目标</th><th>类别</th><th>VA</th></tr></thead>
      <tbody>{in_rows or '<tr><td colspan="4" class="muted">无</td></tr>'}</tbody></table>
    <h3>主数据引用（→ cfg.*）</h3>
    <table><thead><tr><th>本列</th><th>目标</th><th>依据</th><th>VA</th></tr></thead>
      <tbody>{master_rows or '<tr><td colspan="4" class="muted">无</td></tr>'}</tbody></table>
    <h3>未决引用</h3>
    <table><thead><tr><th>本列</th><th>原因</th><th>VA</th></tr></thead>
      <tbody>{dangling_rows or '<tr><td colspan="3" class="muted">无</td></tr>'}</tbody></table>

    <h3>不落库成员（{len(obj.get("columns_excluded", []))}）</h3>
    <p class="muted">EVENT/TBD 生命周期、<code>memory_only</code>、对齐补位：线上有、库里不建列，
      理由在此显式登记（反向覆盖门）。</p>
    <table><thead><tr><th>成员</th><th>角色</th><th>理由</th><th>线类型</th><th>VA</th></tr></thead>
      <tbody>{excluded_rows or '<tr><td colspan="5" class="muted">无</td></tr>'}</tbody></table>

    <h3>命令归属（CS 写 / SC 读）</h3>
    <table><thead><tr><th>写命令</th><th>op</th><th>via</th><th>verbs</th></tr></thead>
      <tbody>{writes_rows or '<tr><td colspan="4" class="muted">无</td></tr>'}</tbody></table>
    <table><thead><tr><th>读命令</th><th>op</th><th>via</th><th>verbs</th></tr></thead>
      <tbody>{reads_rows or '<tr><td colspan="4" class="muted">无</td></tr>'}</tbody></table>
    {f'<p class="muted"><strong>写方点名登记</strong>（`_overrides.json.writers`：线体里没有实体、命令只带目标 id，引擎的口径认不出来；见 docs/05 §9.9）：</p><ul>{declared_notes}</ul>' if declared_notes else ''}
    <p class="muted">子表：{"".join(child_links) or "—"}</p>
    """
    return body, nav_key


# ------------------------------------------------------------------ 覆盖率页

def build_coverage_page(rows: list[dict], objects: dict) -> tuple[str, str]:
    excluded_reason = {}
    for oid, obj in objects.items():
        for c in obj.get("columns_excluded", []):
            excluded_reason[(oid, c.get("member", ""))] = c.get("reason", "")

    persisted, dropped = [], []
    for r in rows:
        if r.get("table"):
            persisted.append(r)
        else:
            dropped.append(r)

    def row_html(r):
        oid = r.get("object", "")
        field = r.get("field", "")
        table = r.get("table", "")
        if table:
            where = f'<code>{esc(table)}.{esc(r.get("column", ""))}</code>'
            why = "—"
        else:
            shape = objects.get(oid, {}).get("shape", "")
            why = excluded_reason.get((oid, field), "")
            if not why:
                why = "宿主子表（各宿主一张 `宿主__成员`）" if shape in ("child", "nested") else "未落库"
            where = '<span class="muted">—</span>'
        fk = r.get("fk_target", "")
        fk_html = f'<code>{esc(fk)}</code>' if fk else ""
        return (f'<tr><td><a href="objects/{esc(oid)}.html"><code>{esc(oid)}</code></a></td>'
                f'<td><code>{esc(field)}</code></td>'
                f'<td>{where}</td>'
                f'<td>{role_badge(r.get("role", ""))}</td>'
                f'<td><code>{esc(r.get("wire_type", ""))}</code></td>'
                f'<td>{esc(r.get("length", ""))}</td>'
                f'<td>{esc(r.get("lifetime", ""))}</td>'
                f'<td>{r.get("writer_count", 0)} / {r.get("reader_count", 0)}</td>'
                f'<td>{fk_html}</td>'
                f'<td class="muted">{esc(r.get("evidence_va", ""))}</td>'
                f'<td>{esc(why)}</td></tr>')

    why_counts = collections.Counter()
    for r in dropped:
        oid, field = r.get("object", ""), r.get("field", "")
        shape = objects.get(oid, {}).get("shape", "")
        why_counts[excluded_reason.get((oid, field))
                   or ("宿主子表" if shape in ("child", "nested") else "未落库")] += 1
    why_html = "".join(f'<li><code>{esc(k)}</code> · {v}</li>' for k, v in why_counts.most_common())

    body = f"""
    <nav class="breadcrumb"><a href="index.html">归位库</a> / <span>归位覆盖率</span></nav>
    <h2>归位覆盖率（逐列出处）</h2>
    <p class="lead">正向门：<strong>每个落库列都能指回「对象 · 成员 · 线类型 · 命令 @VA」</strong>；
      反向门：<strong>每个线上成员要么落到某列，要么被显式登记为「不落库 + 理由」</strong>。</p>
    <div class="grid stats">
      <div class="stat"><div class="num">{len(rows)}</div><div class="lbl">线上成员</div></div>
      <div class="stat"><div class="num">{len(persisted)}</div><div class="lbl">落库成员</div></div>
      <div class="stat"><div class="num">{len(dropped)}</div><div class="lbl">不落库成员</div></div>
      <div class="stat"><div class="num">{sum(1 for r in rows if not r.get("evidence_va"))}</div><div class="lbl">无 VA（有 ref 出处可替）</div></div>
    </div>
    <section class="asm-panel"><h3>不落库理由分布</h3><ul>{why_html}</ul></section>

    <h3>落库成员（{len(persisted)}）</h3>
    <table>
      <thead><tr><th>对象</th><th>成员</th><th>表.列</th><th>角色</th><th>线类型</th><th>长</th><th>生命周期</th><th>写/读</th><th>FK</th><th>VA</th><th></th></tr></thead>
      <tbody>{"".join(row_html(r) for r in sorted(persisted, key=lambda r: (r.get("table", ""), r.get("column", ""))))}</tbody>
    </table>

    <h3>不落库成员（{len(dropped)}）</h3>
    <table>
      <thead><tr><th>对象</th><th>成员</th><th>表.列</th><th>角色</th><th>线类型</th><th>长</th><th>生命周期</th><th>写/读</th><th>FK</th><th>VA</th><th>理由</th></tr></thead>
      <tbody>{"".join(row_html(r) for r in sorted(dropped, key=lambda r: (r.get("object", ""), r.get("field", ""))))}</tbody>
    </table>
    """
    return body, "homing/coverage.html"


# ------------------------------------------------------------------ 关联页

def build_relations_page(relations: dict, objects: dict) -> tuple[str, str]:
    def obj_link(field_path: str) -> str:
        oid = field_path.split(".")[0]
        if oid in objects:
            return f'<a href="objects/{esc(oid)}.html"><code>{esc(oid)}</code></a>.{esc(field_path.split(".", 1)[1])}'
        return f'<code>{esc(field_path)}</code>'

    fk_rows = "".join(
        f'<tr><td>{obj_link(r.get("from", ""))}</td><td><code>{esc(r.get("to", ""))}</code></td>'
        f'<td>{esc(r.get("kind", ""))}</td><td>{esc(r.get("basis", ""))}</td>'
        f'<td class="muted">{esc(r.get("evidence_va", ""))}</td></tr>'
        for r in relations.get("relations", []))
    master_rows = "".join(
        f'<tr><td>{obj_link(r.get("from", ""))}</td><td><code>{esc(r.get("to", ""))}</code></td>'
        f'<td>{esc(r.get("basis", ""))}</td><td class="muted">{esc(r.get("evidence_va", ""))}</td></tr>'
        for r in relations.get("master_refs", []))
    # 源对象不建表的引用（docs/05 §9.9）：仍在线体里成立、仍是证据，但**建不出外键**
    # （库里没有源表）。单列一表，免得读者以为「外键」一栏漏了一批边。
    wire_rows = "".join(
        f'<tr><td>{obj_link(r.get("from", ""))}</td><td><code>{esc(r.get("to", ""))}</code></td>'
        f'<td>{esc(r.get("kind", ""))}</td><td>{esc(r.get("source_disposition", ""))}</td>'
        f'<td>{esc(r.get("reason", ""))}</td>'
        f'<td class="muted">{esc(r.get("evidence_va", ""))}</td></tr>'
        for r in relations.get("wire_refs", []))
    dangling_rows = "".join(
        f'<tr><td>{obj_link(r.get("from", ""))}</td><td>{esc(r.get("reason", ""))}</td>'
        f'<td class="muted">{esc(r.get("evidence_va", ""))}</td></tr>'
        for r in relations.get("dangling", []))

    body = f"""
    <nav class="breadcrumb"><a href="index.html">归位库</a> / <span>关联</span></nav>
    <h2>关联（外键 / 线上引用 / 主数据引用 / 未决）</h2>
    <p class="lead">规则：<code>scope_fk</code> 是行主不变量（<code>world_id</code>/<code>pilot_id</code> →
      <code>core.*</code>）；<code>fk</code> 是对象之间的真外键；指向 <code>cfg.*</code> 的是<strong>主数据引用</strong>
      （不是 FK，静态配置表）；战斗场景内的实体句柄只活在内存里，不建 FK。</p>

    <h3>外键（{len(relations.get("relations", []))}）</h3>
    <p class="muted">只收<strong>源对象建表</strong>的边：源对象判 <code>DERIVED</code>/<code>EVENT</code>/
      <code>CONFIG</code>/<code>TBD</code> 时库里没有源表，那条引用在下表「线上引用」里。</p>
    <table><thead><tr><th>来源列</th><th>目标</th><th>类别</th><th>依据</th><th>VA</th></tr></thead>
      <tbody>{fk_rows or '<tr><td colspan="5" class="muted">无</td></tr>'}</tbody></table>

    <h3>线上引用（{len(relations.get("wire_refs", []))}）</h3>
    <p class="muted">源对象不建表（<code>DERIVED</code>/<code>EVENT</code>/<code>CONFIG</code>/
      <code>TBD</code>）：引用在线体里成立，但 DDL 建不出这条外键——退役那张表的依据见
      <code>_overrides.json.disposition</code> 与 <code>retire_tables</code>。</p>
    <table><thead><tr><th>来源列</th><th>目标</th><th>类别</th><th>源对象处置</th><th>理由</th><th>VA</th></tr></thead>
      <tbody>{wire_rows or '<tr><td colspan="6" class="muted">无</td></tr>'}</tbody></table>

    <h3>主数据引用（{len(relations.get("master_refs", []))}）</h3>
    <table><thead><tr><th>来源列</th><th>目标</th><th>依据</th><th>VA</th></tr></thead>
      <tbody>{master_rows or '<tr><td colspan="4" class="muted">无</td></tr>'}</tbody></table>

    <h3>未决引用（{len(relations.get("dangling", []))}）</h3>
    <p class="muted">对象名索引给不出唯一目标，需人工批次裁决；明细见
      <a href="unresolved.html">未决清单</a>。</p>
    <table><thead><tr><th>来源列</th><th>原因</th><th>VA</th></tr></thead>
      <tbody>{dangling_rows or '<tr><td colspan="3" class="muted">无</td></tr>'}</tbody></table>
    """
    return body, "homing/relations.html"


# ------------------------------------------------------------------ 未决清单（markdown）

def _inline_md(text: str) -> str:
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)) + 1, 6)
            out.append(f"<h{level}>{_inline_md(m.group(2))}</h{level}>")
            i += 1
            continue
        if stripped.startswith("|"):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 1
            if i < len(lines) and set(lines[i].strip().replace("|", "").replace("-", "").replace(":", "").strip()) == set():
                i += 1
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{_inline_md(h)}</th>" for h in header)
                       + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{_inline_md(c)}</td>" for c in r) + "</tr>" for r in rows)
                       + "</tbody></table>")
            continue
        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append('<blockquote class="muted">' + "<br>".join(_inline_md(b) for b in block) + "</blockquote>")
            continue
        if stripped.startswith(("- ", "* ")):
            items = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{_inline_md(x)}</li>" for x in items) + "</ul>")
            continue
        out.append(f"<p>{_inline_md(stripped)}</p>")
        i += 1
    return "\n".join(out)


def build_unresolved_page(md: str) -> tuple[str, str]:
    body = (f'<nav class="breadcrumb"><a href="index.html">归位库</a> / <span>未决清单</span></nav>'
            + md_to_html(md))
    return body, "homing/unresolved.html"


# ------------------------------------------------------------------ 入口

def generate_homing_site(page) -> int:
    summary = load_json(HOMING_DIR / "summary.json", {})
    roles = load_json(HOMING_DIR / "roles.json", {})
    relations = load_json(HOMING_DIR / "relations.json", {})
    objects = load_objects()
    ddl_cols, comments, indexes = load_ddl(DDL_PATH)

    if not objects:
        print("  homing: 没有对象（先跑 tools/derive_homing.py）")
        return 0

    # 表 → (对象, 表声明)
    tables_of: dict[str, tuple[str, dict]] = {}
    for oid, obj in objects.items():
        for t in obj.get("tables", []):
            tables_of.setdefault(t.get("name", ""), (oid, t))

    change_counts = {}
    for oid, obj in objects.items():
        written = {w.get("command") for w in obj.get("writes", [])}
        read = {r.get("command") for r in obj.get("reads", [])}
        for t in obj.get("tables", []):
            change_counts[t.get("name", "")] = (len(written), len(read))

    existing_cmds = {p.stem for p in (SITE_DIR / "commands").glob("*.html")} if (SITE_DIR / "commands").is_dir() else set()

    out_dir = SITE_DIR / "homing"
    obj_dir = out_dir / "objects"
    obj_dir.mkdir(parents=True, exist_ok=True)

    # 对象页是按对象集写出的，删掉对象（如 fire_points 并入 fire_point）后旧页会留下来
    # 变成孤儿页——页还在、链接全指向它，读起来像「库里还有这个对象」。这里显式清掉。
    for stale in obj_dir.glob("*.html"):
        if stale.stem not in objects:
            stale.unlink()

    (out_dir / "index.html").write_text(
        page("归位库", "homing/index.html",
             build_homing_index(summary, roles, objects, ddl_cols, tables_of, change_counts)),
        encoding="utf-8")

    rows = ([json.loads(l) for l in (HOMING_DIR / "fields.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
            if (HOMING_DIR / "fields.jsonl").is_file() else [])
    body, nav_key = build_coverage_page(rows, objects)
    (out_dir / "coverage.html").write_text(page("归位覆盖率", nav_key, body), encoding="utf-8")

    body, nav_key = build_relations_page(relations, objects)
    (out_dir / "relations.html").write_text(page("关联", nav_key, body), encoding="utf-8")

    md_path = HOMING_DIR / "unresolved.md"
    if md_path.is_file():
        body, nav_key = build_unresolved_page(md_path.read_text(encoding="utf-8"))
        (out_dir / "unresolved.html").write_text(page("未决清单", nav_key, body), encoding="utf-8")

    n = 0
    for oid, obj in objects.items():
        body, nav_key = build_object_page(oid, obj, objects, ddl_cols, comments, indexes,
                                          relations, existing_cmds)
        (obj_dir / f"{oid}.html").write_text(page(obj.get("title") or oid, nav_key, body), encoding="utf-8")
        n += 1
    return n

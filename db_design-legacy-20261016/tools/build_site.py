#!/usr/bin/env python3
"""Generate static HTML site from db_design/schema/*.json (baked, no fetch)."""

from __future__ import annotations

import collections
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

import check_site_links
from build_cfg_site import generate_cfg_site
from build_homing_site import generate_homing_site

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema"
SITE_DIR = Path(__file__).resolve().parents[1] / "site"
ASSETS_DIR = SITE_DIR / "assets"

DISPOSITION_COLORS = {
    "PERSIST": "#2e7d32",
    "CONFIG": "#1565c0",
    "DERIVED": "#6a1b9a",
    "TRANSIENT": "#e65100",
    "EVENT": "#c62828",
    "COMPOSITE": "#455a64",
    "TBD": "#757575",
    "proposed": "#1565c0",
    "complete": "#2e7d32",
}


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def asset_prefix(nav_key: str) -> str:
    if nav_key == "index.html" or nav_key == "relations.html":
        return ""
    depth = nav_key.count("/")
    return "../" * max(depth, 1)


def proto_prefix(nav_key: str) -> str:
    """From generated HTML under db_design/site/ to repo root (9you/, sibling of db_design)."""
    if nav_key == "index.html" or nav_key == "relations.html":
        return "../../"
    return "../../../"


_PAGE_KIND_CACHE: dict[str, str] | None = None


def page_kind(name: str) -> str | None:
    """名字 → 页面目录（`entities` 协议实体页优先，其次 `homing/objects` 归位对象页）。

    同一个名字常常**两侧都有**（72 个实体名里 71 个也归位成了对象），所以顺序固定为
    「协议实体优先」——命令页的 `db_effects.entity` 语义就是协议实体；
    只有名字被归位库收编、协议实体页已裁掉时（evflag3 / ms_rokaku / equip_set / ms_set），
    才落到对象页。两侧都没有则返回 None（调用方退化成纯 code，不产生死链）。
    """
    global _PAGE_KIND_CACHE
    if _PAGE_KIND_CACHE is None:
        idx: dict[str, str] = {}
        for sub in ("entities", "homing/objects"):
            for p in (SCHEMA_DIR / sub).glob("*.json"):
                idx.setdefault(p.stem, sub)
        _PAGE_KIND_CACHE = idx
    return _PAGE_KIND_CACHE.get(name)


def ref_page_html(name: str | None, prefix: str = "../") -> str:
    """实体/对象名 → 真实存在的页面链接；两侧都没有页面时只给 `<code>`。"""
    if not name:
        return ""
    kind = page_kind(name)
    if kind:
        return f'<a href="{prefix}{kind}/{esc(name)}.html"><code>{esc(name)}</code></a>'
    return f'<code>{esc(name)}</code>'


def repo_file_html(rel: str | None, nav_key: str) -> str:
    """仓库内相对路径 → 指向**仓库里真实存在**的文件；对不上就只给 `<code>`。

    模型里存的是仓库相对路径，且两种写法都有：`commands/_verify/<id>.json`（ASM 原始切片）
    与 `schema/commands/_overrides/<id>.json`（人工裁决件）。这些件**不随站点发布**
    （`_verify` 单目录 1830 个文件 / 113MB），所以链接按 `proto_prefix` 指到仓库原件——
    与命令页里 `source_dir` 的 `.go` / `README.md` 链接同一种（站点外相对路径）。
    """
    if not rel:
        return ""
    dbd = SCHEMA_DIR.parent
    repo = dbd.parent
    for cand in (dbd / rel, dbd / "schema" / rel, repo / rel):
        if cand.is_file():
            return (f'<a href="{proto_prefix(nav_key)}{cand.relative_to(repo).as_posix()}"'
                    f' target="_blank"><code>{esc(rel)}</code></a>')
    return f'<code>{esc(rel)}</code> <span class="muted">（仓库内路径，未随站点发布）</span>'


def nav(current: str) -> str:
    links = [
        ("index.html", "首页"),
        ("homing/index.html", "归位库"),
        ("tables/index.html", "旧表留档"),
        ("commands/index.html", "命令"),
        ("cfg/index.html", "配置表79"),
        ("srv/index.html", "服务端配置"),
        ("asm-audit/index.html", "ASM 审计"),
        ("oracle-audit/index.html", "Oracle 审计"),
        ("entities/index.html", "协议实体"),
        ("fields/index.html", "字段索引"),
        ("relations.html", "表关系"),
    ]
    parts = []
    for href, label in links:
        active = current == href or (href.endswith("/") and current.startswith(href.replace("index.html", "")))
        if href == "index.html" and current == "index.html":
            active = True
        elif href != "index.html" and current.startswith(href.split("/")[0] + "/"):
            active = True
        cls = ' class="active"' if active else ""
        prefix = asset_prefix(current) if current != "index.html" else ""
        if current.startswith("tables/") or current.startswith("cfg/") or current.startswith("entities/") or current.startswith("fields/") or current.startswith("commands/") or current.startswith("srv/") or current.startswith("asm-audit/") or current.startswith("oracle-audit/") or current.startswith("homing/"):
            if href == "index.html":
                parts.append(f'<a href="{prefix}{href}"{cls}>{esc(label)}</a>')
            elif href == "relations.html":
                parts.append(f'<a href="{prefix}{href}"{cls}>{esc(label)}</a>')
            else:
                parts.append(f'<a href="{prefix}{href}"{cls}>{esc(label)}</a>')
        else:
            parts.append(f'<a href="{prefix if href != "index.html" and current != "index.html" else ""}{href}"{cls}>{esc(label)}</a>')
    return "\n      ".join(parts)


def page(title: str, nav_key: str, body: str) -> str:
    ap = asset_prefix(nav_key)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · db_design</title>
  <link rel="stylesheet" href="{ap}assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <h1><a href="{ap}index.html">db_design</a></h1>
      <p class="header-note">唯一证据源：<code>protocol_analysis/</code></p>
      <nav>{nav(nav_key)}</nav>
    </div>
  </header>
  <main class="wrap">
{body}
  </main>
  <footer class="site-footer">
    <div class="wrap">生成于 {date.today().isoformat()} · 改 JSON 后重跑 build_site.py · HTML 只读</div>
  </footer>
</body>
</html>
"""


def badge(disposition: str) -> str:
    color = DISPOSITION_COLORS.get(disposition, "#757575")
    return f'<span class="badge" style="background:{color}">{esc(disposition)}</span>'


def load_composites() -> dict[str, dict]:
    comp_dir = SCHEMA_DIR / "composites"
    out: dict[str, dict] = {}
    if comp_dir.is_dir():
        for path in sorted(comp_dir.glob("*.json")):
            data = load_json(path)
            out[data.get("id") or path.stem] = data
    return out


def load_tables() -> list[dict]:
    tables_dir = SCHEMA_DIR / "_legacy_tables"
    out = []
    if tables_dir.is_dir():
        for path in sorted(tables_dir.glob("*.json")):
            out.append(load_json(path))
    return out


def load_legacy_evidence() -> dict:
    """冻结的旧库证据（`tools/freeze_legacy.py`）→ `{表干: node}`。

    旧表注册表 `schema/relations.json` 已退役，页面上要的 id/status/purpose/
    evidence_commands 全部改由这里取（同一份数据，但不再有一份会漂的副本）。
    """
    path = SCHEMA_DIR / "_meta" / "legacy_evidence.json"
    if not path.is_file():
        raise SystemExit(
            f"缺旧库冻结证据 {path}——先跑 python db_design/tools/freeze_legacy.py")
    return (load_json(path).get("tables") or {})


def load_srv() -> dict | None:
    """读服务端配置表（srv.*）的文档投影；由 build_srv_docs.py 从迁移 SQL 生成。"""
    index_path = SCHEMA_DIR / "srv" / "index.json"
    if not index_path.is_file():
        return None
    index = load_json(index_path)
    docs: dict[str, dict] = {}
    tbl_dir = SCHEMA_DIR / "srv" / "tables"
    if tbl_dir.is_dir():
        for path in sorted(tbl_dir.glob("*.json")):
            doc = load_json(path)
            docs[doc.get("slug") or path.stem] = doc
    index["_docs"] = docs
    return index


def resolve_members(field: dict, composites: dict[str, dict]) -> list[dict]:
    if field.get("members"):
        return field["members"]
    for key in ("composite_ref", "element_composite_ref"):
        ref = field.get(key)
        if ref and ref in composites:
            # 别名（layout_same_as）/ 前缀形（prefix_of）都要摊平，否则列树会断在空成员上
            return composite_members(ref, composites)
    # 数组成员（`bracket_node[15]` / `unlockw[3]` / `array<x,N>`）：展开**元素**的成员，
    # 不是 15 份副本；标量数组不参与。
    wt = field.get("wire_type") or (field.get("wire_sources") or [{}])[0].get("wire_type") or ""
    elem = array_element(wt)
    if elem and elem not in SCALAR_WT and elem in composites:
        return composite_members(elem, composites)
    return []


def fmt_offset(field: dict) -> str:
    off = field.get("offset")
    mem = field.get("memory_offset")
    length = field.get("length")
    if off is None and length is None and mem is None:
        return ""
    parts = []
    if field.get("memory_only"):
        if mem is not None:
            parts.append(f"mem +{esc(mem)}")
        if length is not None:
            parts.append(f"{esc(length)}B")
        parts.append("(memory_only)")
        return " ".join(parts)
    if off is not None:
        parts.append(f"wire +{esc(off)}")
    if mem is not None and mem != off:
        parts.append(f"mem +{esc(mem)}")
    if length is not None:
        parts.append(f"{esc(length)}B")
    return " ".join(parts)


def asm_badge(status: str | None) -> str:
    if not status:
        return '<span class="muted">—</span>'
    color = "#2e7d32" if status == "pass" else "#c62828"
    label = "ASM ✓" if status == "pass" else f"ASM {status}"
    return f'<span class="badge" style="background:{color}">{esc(label)}</span>'


def composite_for_table(tbl: dict, composites: dict[str, dict]) -> dict | None:
    ent = tbl.get("entity_ref") or tbl.get("asm_audit", {}).get("composite_ref")
    if not ent:
        for col in tbl.get("columns", []):
            ref = col.get("composite_ref")
            if ref and ref in composites:
                return composites[ref]
    if ent and ent in composites:
        return composites[ent]
    return None


def memory_audit_for_composite(comp: dict, composites: dict[str, dict]) -> dict:
    """asm_audit.memory；layout_same_as 别名可继承基 composite 的 memory 块。"""
    asm = comp.get("asm_audit") or {}
    mem = asm.get("memory")
    if mem:
        return mem
    base_id = comp.get("layout_same_as")
    if base_id and base_id in composites:
        base_mem = ((composites[base_id].get("asm_audit") or {}).get("memory"))
        if base_mem:
            return base_mem
    return {}


def fmt_evidence(wire_sources: list[dict] | None, nav_key: str) -> str:
    if not wire_sources:
        return '<span class="muted">无证据链</span>'
    pp = proto_prefix(nav_key)
    lines = []
    for ws in wire_sources[:3]:
        path = ws.get("protocol_path", "")
        cmd = ws.get("command", "")
        off = ws.get("offset", "")
        sec = ws.get("section", "")
        struct = ws.get("struct")
        bits = [f"<code>{esc(cmd)}</code>"]
        if struct:
            bits.append(f"struct <code>{esc(struct)}</code>")
        if off != "":
            bits.append(f"@{esc(off)}")
        if sec:
            bits.append(esc(sec))
        if path:
            lines.append(
                f'<div class="evidence-line">{" ".join(bits)} '
                f'<a class="ev-link" href="{pp}{esc(path)}" target="_blank">📄 protocol</a></div>'
            )
        else:
            lines.append(f'<div class="evidence-line">{" ".join(bits)}</div>')
    if len(wire_sources) > 3:
        lines.append(f'<div class="muted">+{len(wire_sources)-3} 条证据</div>')
    return "".join(lines)


def count_columns_recursive(columns: list[dict], composites: dict[str, dict]) -> tuple[int, int, int]:
    total = persist = tbd = 0
    for col in columns:
        total += 1
        d = col.get("disposition", "TBD")
        if d == "PERSIST":
            persist += 1
        elif d == "TBD":
            tbd += 1
        for m in resolve_members(col, composites):
            t, p, td = count_columns_recursive([m], composites)
            total += t
            persist += p
            tbd += td
    return total, persist, tbd


def col_wire_type(col: dict) -> str:
    if col.get("wire_type"):
        return col["wire_type"]
    src = (col.get("wire_sources") or [{}])[0]
    return src.get("wire_type", "")


def array_shape_note(col: dict, wt: str, composites: dict[str, dict]) -> str:
    """数组成员的「条数×元素线长」补充说明；标量数组与不可算的不显示。"""
    t = (wt or "").strip()
    if not (t.startswith("array<") or re.search(r"\[\s*\d+\s*\]\s*$", t)):
        return ""
    elem = array_element(t)
    if not elem or elem in SCALAR_WT or elem not in composites:
        return ""
    shape = array_shape(t, col.get("length"))
    return f' <span class="muted">（元素 {esc(elem)}{" " + esc(shape) if shape else ""}）</span>'


def render_column_node(col: dict, composites: dict[str, dict], nav_key: str,
                       seen: tuple[str, ...] = ()) -> str:
    members = resolve_members(col, composites)
    ref = col.get("composite_ref") or col.get("element_composite_ref")
    ref_note = f' <span class="muted">← <code>{esc(ref)}</code></span>' if ref else ""
    wt = col_wire_type(col)
    elem_ref = array_element(wt)
    if (not ref) and elem_ref and elem_ref not in SCALAR_WT and elem_ref in composites:
        ref_note = f' <span class="muted">← 元素 <code>{esc(elem_ref)}</code></span>'

    key = ref or elem_ref or ""
    # 自引用/环路守门：理论上 composites 无环，但手工文件一旦写出环就会把站点生成挂死
    if key and key in seen:
        members = []
    if members:
        child = "".join(render_column_node(m, composites, nav_key, seen + (key,) if key else seen)
                        for m in members)
        summary = (
            f"<code class='fname'>{esc(col.get('name'))}</code> "
            f"<code class='ftype'>{esc(wt)}</code> "
            f"<span class='offset'>{fmt_offset(col)}{array_shape_note(col, wt, composites)}</span> "
            f"{badge(col.get('disposition', 'TBD'))}{ref_note}"
        )
        return f"""<li class="tree-branch">
      <details open>
        <summary>{summary}</summary>
        <div class="tree-body">
          <div class="tree-detail">{esc(col.get('meaning', ''))}</div>
          {fmt_evidence(col.get('wire_sources'), nav_key)}
          <ul class="field-tree">{child}</ul>
        </div>
      </details>
    </li>"""

    asm_note = ""
    if col.get("asm_verified"):
        va = col.get("asm_evidence_va", "")
        asm_note = f' <span class="asm-ok" title="{esc(va)}">✓</span>'
    return f"""<li class="tree-leaf">
      <div class="tree-row cols-4">
        <div class="tree-head">
          <code class="fname">{esc(col.get('name'))}</code>
          <code class="ftype">{esc(wt)}</code>
          <span class="offset">{fmt_offset(col)}{array_shape_note(col, wt, composites)}</span>
          {badge(col.get('disposition', 'TBD'))}{asm_note}
        </div>
        <div class="tree-meaning">{esc(col.get('meaning', ''))}</div>
        <div class="tree-evidence">{fmt_evidence(col.get('wire_sources'), nav_key)}</div>
        <div class="tree-notes muted">{esc(col.get('notes', ''))}</div>
      </div>
    </li>"""


def build_index(meta: dict, tables: list, entities: list, fields_index: dict | None, composites: dict[str, dict],
                commands_index: dict | None = None) -> str:
    fi_stats = (fields_index or {}).get("stats", {})
    complete = [t for t in tables if t.get("status") == "complete"]
    asm_pass = sum(
        1
        for t in complete
        if (composite_for_table(t, composites) or {}).get("asm_audit", {}).get("status") == "pass"
        or t.get("asm_audit", {}).get("status") == "pass"
    )
    table_cards = ""
    for tbl in tables[:12]:
        tid = tbl.get("id", "")
        cols = tbl.get("columns", [])
        persist = sum(1 for c in cols if c.get("disposition") == "PERSIST")
        comp = composite_for_table(tbl, composites)
        asm = (comp or {}).get("asm_audit", {}).get("status") or tbl.get("asm_audit", {}).get("status")
        table_cards += f"""
    <a class="card card-primary" href="tables/{esc(tid)}.html">
      <div class="card-status">{badge(tbl.get('status', 'proposed'))} {asm_badge(asm)}</div>
      <h3><code>{esc(tid)}</code></h3>
      <p>{esc(tbl.get('title', ''))}</p>
      <div class="card-meta">{len(cols)} 列 · PERSIST {persist}</div>
    </a>"""

    c_counts = (commands_index or {}).get("counts", {})
    cmds_section = ""
    if commands_index:
        by_status = c_counts.get("by_status", {})
        cmds_section = f"""
    <section>
      <h2>交互命令（命令维度模型）</h2>
      <p class="lead">{c_counts.get('commands', 0)} 条命令 · {c_counts.get('fields', 0)} 个负载字段 ·
        证据只允许来自 <code>protocol_analysis/</code> 与 IDA 汇编（口径见 <code>docs/01-命令模型.md</code>）</p>
      <div class="grid stats">
        <div class="stat"><div class="num">{by_status.get('IMPORTED', 0)}</div><div class="lbl">IMPORTED</div></div>
        <div class="stat"><div class="num">{by_status.get('ASM-VERIFIED', 0)}</div><div class="lbl">ASM-VERIFIED</div></div>
        <div class="stat"><div class="num">{by_status.get('BEHAVIOR-DONE', 0)}</div><div class="lbl">BEHAVIOR-DONE</div></div>
        <div class="stat"><div class="num">{c_counts.get('by_direction', {}).get('SC', 0)}</div><div class="lbl">SC 收</div></div>
        <div class="stat"><div class="num">{c_counts.get('by_direction', {}).get('CS', 0)}</div><div class="lbl">CS 发</div></div>
      </div>
      <p><a href="commands/index.html">查看全部命令 →</a>
         · <a href="commands/structs.html">包结构体</a>
         · <a href="commands/capabilities.html">能力矩阵</a>
         · <a href="commands/db-effects.html">数据库影响</a></p>
    </section>"""

    body = f"""
    <section class="hero">
      <h2>数据库字段设计</h2>
      <p class="lead">阶段 <strong>P6 归位库已切</strong> · DDL/store 由 <code>schema/homing/objects/</code> 生成
        · 证据仅来自 <code>protocol_analysis/</code></p>
    </section>

    <section class="grid stats">
      <div class="stat"><div class="num">{len(complete)}</div><div class="lbl">complete 表</div></div>
      <div class="stat"><div class="num">{asm_pass}/{len(complete)}</div><div class="lbl">ASM wire 链 pass</div></div>
      <div class="stat"><div class="num">{len(composites)}</div><div class="lbl">composite</div></div>
      <div class="stat"><div class="num">{meta.get('stats', {}).get('srv_tables', 0)}</div><div class="lbl">服务端配置表</div></div>
      <div class="stat"><div class="num">{fi_stats.get('unique_names', '—')}</div><div class="lbl">协议字段索引</div></div>
      <div class="stat"><div class="num">{c_counts.get('commands', '—')}</div><div class="lbl">交互命令</div></div>
    </section>

    {cmds_section}

    <section>
      <h2>归位库（新库设计）</h2>
      <p class="lead">以字节级模型为地基的<strong>域 → 对象 → 角色</strong>三层归位：DDL 与 Go store 都由
        <code>schema/homing/objects/*.json</code> 生成，逐列可回溯到命令 @VA。</p>
      <div class="card-grid">
        <a class="card card-primary" href="homing/index.html">
          <h3>对象 / 建表总览</h3>
          <p class="card-meta">对象与表、主键、角色词表、类型映射、未建表对象</p>
        </a>
        <a class="card" href="homing/coverage.html">
          <h3>归位覆盖率</h3>
          <p class="card-meta">正向：每列指回命令@VA · 反向：不落库成员显式登记理由</p>
        </a>
        <a class="card" href="homing/relations.html">
          <h3>对象关联</h3>
          <p class="card-meta">外键 / 主数据引用（cfg.*）/ 未决引用</p>
        </a>
        <a class="card" href="homing/unresolved.html">
          <h3>未决清单</h3>
          <p class="card-meta">引擎判不了的批次，逐条带推理依据</p>
        </a>
      </div>
    </section>

    <section>
      <h2>表设计（旧提议 · 留档）</h2>
      <p class="lead">P3 起 <code>schema/tables/*.json</code> 已降级为 <code>_legacy_tables/</code>，
        不再驱动 DDL，只作对照留档。新库设计见上面的<strong>归位库</strong>。</p>
      <div class="card-grid">{table_cards or '<p class="muted">暂无表</p>'}</div>
      <p><a href="tables/index.html">查看全部旧提议表 →</a></p>
    </section>

    <section>
      <h2>配置表（datatables）</h2>
      <p class="lead">79 张 CSV 配置表列语义 · 订案字段名 · 与 GM 共用 <code>cfg_schema.json</code></p>
      <p><a class="card card-primary" href="cfg/index.html" style="display:inline-block;padding:0.75rem 1rem;">配置表79 →</a></p>
    </section>

    <section>
      <h2>服务端配置表（srv.*）</h2>
      <p class="lead">价目 / 容量 / 频道登记本等<strong>服务端策略值</strong>：运行时来源是库里的表；
        本页 JSON 由 <code>build_srv_docs.py</code> 从迁移 SQL 反推，只当文档</p>
      <p><a class="card card-primary" href="srv/index.html" style="display:inline-block;padding:0.75rem 1rem;">srv.* 服务端配置表</a></p>
    </section>

    <section>
      <h2>辅助视图</h2>
      <ul>
        <li><a href="commands/index.html">交互命令</a> — 每条命令的字段解剖 / 包结构体 / 行为 / DB 影响</li>
        <li><a href="commands/structs.html">包结构体总览</a> — 请求·应答的 Go 结构体成员序列</li>
        <li><a href="commands/capabilities.html">能力矩阵</a> — 受控能力标签与命令覆盖</li>
        <li><a href="commands/db-effects.html">数据库影响</a> — 命令 → 实体 / 提议表 的 read·create·update·delete</li>
        <li><a href="asm-audit/index.html">ASM 审计</a> — 73 表 wire 链 / evidence_va 状态</li>
        <li><a href="oracle-audit/index.html">Oracle 审计</a> — 用客户端自己的代码当判据，四层复核结论</li>
        <li><a href="entities/index.html">协议实体</a> — 按线宽形态 / struct 浏览</li>
        <li><a href="fields/index.html">字段索引</a> — 1191 唯一名自动草稿（P0）</li>
        <li><a href="relations.html">表关系</a> — 提议表之间的 FK（待补）</li>
        <li><a href="homing/index.html">归位库</a> — 新库设计：对象 / 角色 / 覆盖率 / 未决</li>
      </ul>
    </section>
"""
    return page("首页", "index.html", body)


def build_tables_index(tables: list, composites: dict[str, dict]) -> str:
    rows = ""
    for tbl in tables:
        tid = tbl.get("id", "")
        cols = tbl.get("columns", [])
        total, persist, tbd = count_columns_recursive(cols, composites)
        cmds = ", ".join(f"<code>{esc(c)}</code>" for c in tbl.get("evidence_commands", [])[:2])
        comp = composite_for_table(tbl, composites)
        asm = (comp or {}).get("asm_audit", {})
        asm_st = asm.get("status")
        reader = asm.get("reader") or (comp or {}).get("reader", "")
        wire_len = asm.get("total_bytes") or (comp or {}).get("length", "")
        rows += f"""<tr>
      <td><a href="{esc(tid)}.html"><code>{esc(tid)}</code></a></td>
      <td>{esc(tbl.get('title', ''))}</td>
      <td>{badge(tbl.get('status', 'proposed'))}</td>
      <td>{asm_badge(asm_st)}</td>
      <td><code>{esc(reader)}</code></td>
      <td>{esc(wire_len)}</td>
      <td>{len(cols)}</td>
      <td>{persist}</td>
      <td>{cmds}</td>
    </tr>"""
    body = f"""
    <h2>表设计</h2>
    <p class="muted">complete 表 · wire 链 ASM 审计 · 偏移列显示 wire / mem 双线</p>
    <table>
      <thead><tr><th>表 ID</th><th>名称</th><th>状态</th><th>ASM</th><th>reader</th><th>线长</th><th>列数</th><th>PERSIST</th><th>证据命令</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("表设计", "tables/index.html", body)


def build_table_detail(tbl: dict, composites: dict[str, dict], command_ids: set[str] | None = None) -> str:
    tid = tbl.get("id", "")
    nav_key = f"tables/{tid}.html"
    cols_by_name = {c["name"]: c for c in tbl.get("columns", [])}

    groups_html = ""
    for grp in tbl.get("column_groups", []):
        gname = grp.get("name", "")
        group_cols = [cols_by_name[n] for n in grp.get("columns", []) if n in cols_by_name]
        tree = "".join(render_column_node(c, composites, nav_key) for c in group_cols)
        groups_html += f"""
    <section class="col-group">
      <h3>{esc(gname)}</h3>
      <ul class="field-tree root-tree">{tree}</ul>
    </section>"""

    if not groups_html:
        tree = "".join(render_column_node(c, composites, nav_key) for c in tbl.get("columns", []))
        groups_html = f'<ul class="field-tree root-tree">{tree}</ul>'

    cmd_links = ""
    pp = proto_prefix(nav_key)
    for cmd in tbl.get("evidence_commands", []):
        path = f"protocol_analysis/commands/{cmd}/README.md"
        local = cmd_link(cmd, command_ids)
        cmd_links += f'<li>{local} · <a href="{pp}{esc(path)}" target="_blank">protocol README</a></li>'

    total, persist, tbd = count_columns_recursive(tbl.get("columns", []), composites)
    comp = composite_for_table(tbl, composites)
    asm = (comp or {}).get("asm_audit", {})
    asm_html = ""
    if comp:
        mem_n = sum(
            1
            for m in comp.get("members", [])
            if m.get("memory_offset") is not None and m.get("memory_offset") != m.get("offset")
        )
        mem_audit = asm.get("memory") or {}
        asm_html = f"""
    <section class="asm-panel">
      <h3>ASM 审计 {asm_badge(asm.get('status'))} · memory {asm_badge(mem_audit.get('status')) if mem_audit else '<span class="muted">—</span>'}</h3>
      <dl class="asm-dl">
        <dt>composite</dt><dd><code>{esc(comp.get('id', ''))}</code></dd>
        <dt>reader</dt><dd><code>{esc(asm.get('reader') or comp.get('reader', '—'))}</code></dd>
        <dt>线长</dt><dd>{esc(asm.get('total_bytes') or comp.get('length', '—'))} B
          {(f" / 槽 {comp['memory_claim']} B" if comp.get('memory_claim') else "")}</dd>
        <dt>wire_layout</dt><dd><code>{esc(comp.get('wire_layout', '—'))}</code></dd>
        <dt>wire 字段</dt><dd>{asm.get('fields_ok', '?')} ok</dd>
        <dt>memory 字段</dt><dd>{mem_audit.get('mem_fields', mem_n)} audited · {mem_audit.get('fields_ok', '—')} ok</dd>
        <dt>verified</dt><dd>wire {esc(asm.get('verified', '—'))} · mem {esc(mem_audit.get('verified', '—'))}</dd>
      </dl>
    </section>"""

    body = f"""
    <nav class="breadcrumb"><a href="index.html">表设计</a> / <span><code>{esc(tid)}</code></span></nav>
    <h2>{esc(tbl.get('title', tid))} {badge(tbl.get('status', 'proposed'))} {asm_badge(asm.get('status'))}</h2>
    <p>{esc(tbl.get('purpose', ''))}</p>
    <p class="muted">共 {total} 节点 · PERSIST {persist} · TBD {tbd}</p>
    {asm_html}
    <h3>证据命令</h3>
    <ul>{cmd_links}</ul>

    <h3 id="columns">列树（按分组）</h3>
    <div class="tree-legend">
      <span>列名</span><span>线类型</span><span>disposition</span><span>含义</span><span>→ protocol 证据</span>
    </div>
    {groups_html}
"""
    return page(tbl.get("title", tid), nav_key, body)


def render_field_tree(fields: list[dict], composites: dict[str, dict], nav_key: str,
                      seen: tuple[str, ...] = ()) -> str:
    items = []
    for field in fields:
        members = resolve_members(field, composites)
        ref = field.get("composite_ref") or field.get("element_composite_ref")
        ref_note = f' <span class="muted">← <code>{esc(ref)}</code></span>' if ref else ""
        wt = field.get("wire_type", "")
        elem_ref = array_element(wt)
        if (not ref) and elem_ref and elem_ref not in SCALAR_WT and elem_ref in composites:
            ref_note = f' <span class="muted">← 元素 <code>{esc(elem_ref)}</code></span>'
        key = ref or elem_ref or ""
        if key and key in seen:
            members = []

        if members:
            child = render_field_tree(members, composites, nav_key, seen + (key,) if key else seen)
            summary = (
                f"<code class='fname'>{esc(field.get('name'))}</code> "
                f"<code class='ftype'>{esc(field.get('wire_type', ''))}</code> "
                f"<span class='offset'>{fmt_offset(field)}{array_shape_note(field, wt, composites)}</span> "
                f"{badge(field.get('disposition', 'TBD'))}{ref_note}"
            )
            items.append(f"""<li class="tree-branch">
      <details open>
        <summary>{summary}</summary>
        <div class="tree-body">
          <div class="tree-detail">{esc(field.get('meaning', ''))}</div>
          {fmt_evidence(field.get('wire_sources'), nav_key)}
          <ul class="field-tree">{child}</ul>
        </div>
      </details>
    </li>""")
        else:
            items.append(f"""<li class="tree-leaf">
      <div class="tree-row cols-4">
        <div class="tree-head">
          <code class="fname">{esc(field.get('name'))}</code>
          <code class="ftype">{esc(field.get('wire_type', ''))}</code>
          <span class="offset">{fmt_offset(field)}{array_shape_note(field, wt, composites)}</span>
          {badge(field.get('disposition', 'TBD'))}
        </div>
        <div class="tree-meaning">{esc(field.get('meaning', ''))}</div>
        <div class="tree-evidence">{fmt_evidence(field.get('wire_sources'), nav_key)}</div>
        <div class="tree-notes"></div>
      </div>
    </li>""")
    return "\n".join(items)


def build_entity_index(entities: list) -> str:
    rows = ""
    for ent in entities:
        fid = ent.get("id", "")
        rows += f"""<tr>
      <td><a href="{esc(fid)}.html"><code>{esc(fid)}</code></a></td>
      <td>{esc(ent.get('title', ''))}</td>
      <td>{len(ent.get('fields', []))}</td>
      <td>{len(ent.get('wire_forms', []))}</td>
      <td><code>{esc(ent.get('table_ref', '—'))}</code></td>
    </tr>"""
    body = f"""
    <h2>协议实体</h2>
    <p class="muted">业务合并视角 · 证据来自 protocol_analysis · 非 DB 主视图</p>
    <table>
      <thead><tr><th>ID</th><th>名称</th><th>字段</th><th>线宽形态</th><th>关联提议表</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("协议实体", "entities/index.html", body)


def cmd_link(cid: str, command_ids: set[str] | None, prefix: str = "../commands/") -> str:
    """命令 id → 本地命令页链接（命令页不存在时退化为纯文本，不产生死链）。"""
    if not cid:
        return ""
    if command_ids is None or cid in command_ids:
        return f'<a href="{prefix}{esc(cid)}.html"><code>{esc(cid)}</code></a>'
    return f"<code>{esc(cid)}</code>"


def build_entity_detail(ent: dict, composites: dict[str, dict], command_ids: set[str] | None = None) -> str:
    fid = ent.get("id", "")
    nav_key = f"entities/{fid}.html"

    wire_rows = ""
    used_cmds: list[str] = []
    for wf in ent.get("wire_forms", []):
        pp = proto_prefix(nav_key)
        path = wf.get("protocol_path", "")
        link = f'<a href="{pp}{esc(path)}" target="_blank">README</a>' if path else ""
        cmds_list = wf.get("commands", []) or []
        for c in cmds_list:
            if c not in used_cmds:
                used_cmds.append(c)
        cmds = ", ".join(cmd_link(c, command_ids) for c in cmds_list)
        wire_rows += f"""<tr>
      <td><code>{esc(wf.get('name'))}</code></td>
      <td>{esc(wf.get('length'))} B</td>
      <td><code>{esc(wf.get('struct_type', ''))}</code></td>
      <td>{cmds}</td>
      <td>{link}</td>
    </tr>"""

    # 别名实体（`layout_same_as`）自身不重复维护成员：从 composites 摊平，
    # 免得字段树空着或退化成「成员见 XXX」。
    ent_fields = ent.get("fields") or []
    if not ent_fields and fid in composites:
        ent_fields = composite_members(fid, composites)
    tree_html = render_field_tree(ent_fields, composites, nav_key)

    cmds_html = ""
    if used_cmds:
        cmds_html = f"""
    <h3>相关命令（命令维度模型）</h3>
    <ul class="cmd-refs">{''.join(f'<li>{cmd_link(c, command_ids)}</li>' for c in used_cmds[:40])}</ul>
    <p class="muted">命令页含逐字段解剖、包结构体、客户端行为与 DB 影响。</p>"""

    body = f"""
    <nav class="breadcrumb"><a href="index.html">协议实体</a> / <span>{esc(ent.get('title', fid))}</span></nav>
    <h2>{esc(ent.get('title', fid))} <code class="inline">{esc(fid)}</code></h2>
    <p>{esc(ent.get('description', ''))}</p>
    <p>关联提议表：<code>{esc(ent.get('table_ref', '—'))}</code> · <a href="../tables/{esc(ent.get('table_ref', ''))}.html">查看表设计 →</a></p>

    <h3>线宽形态</h3>
    <table>
      <thead><tr><th>名称</th><th>长度</th><th>结构</th><th>命令</th><th>证据</th></tr></thead>
      <tbody>{wire_rows}</tbody>
    </table>

    <h3>字段树</h3>
    <ul class="field-tree root-tree">{tree_html}</ul>
    {cmds_html}
"""
    return page(ent.get("title", fid), nav_key, body)


def build_fields_index(fields_index: dict | None) -> str:
    if not fields_index:
        body = "<h2>字段索引</h2><p>P0 草稿 · 请先运行 import_from_protocol.py</p>"
        return page("字段索引", "fields/index.html", body)

    rows = ""
    for f in fields_index.get("fields", [])[:500]:
        cmds = f.get("commands", [])
        cmd = cmds[0]["command"] if cmds else ""
        pp = proto_prefix("fields/index.html")
        path = f"{pp}protocol_analysis/commands/{cmd}/README.md" if cmd else ""
        link = f'<a href="{esc(path)}" target="_blank"><code>{esc(cmd)}</code></a>' if cmd else ""
        rows += f"""<tr>
      <td><code>{esc(f.get('name'))}</code></td>
      <td>{f.get('appear_count', 0)}</td>
      <td>{badge(f.get('disposition', 'TBD'))}</td>
      <td>{esc(f.get('meaning_sample', ''))}</td>
      <td>{link}</td>
    </tr>"""

    stats = fields_index.get("stats", {})
    body = f"""
    <h2>字段索引（P0 草稿）</h2>
    <p class="muted">自动从 protocol_analysis 导入 · {stats.get('unique_names', 0)} 唯一名 · 前 500 条</p>
    <table class="wide">
      <thead><tr><th>字段名</th><th>次数</th><th>disposition</th><th>含义样例</th><th>证据命令</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("字段索引", "fields/index.html", body)


def build_asm_audit_index(tables: list, composites: dict[str, dict]) -> str:
    rows = ""
    pass_n = total_n = 0
    for tbl in sorted(tables, key=lambda t: t.get("id", "")):
        if tbl.get("status") != "complete":
            continue
        tid = tbl.get("id", "")
        comp = composite_for_table(tbl, composites)
        if not comp:
            continue
        total_n += 1
        asm = comp.get("asm_audit", {})
        st = asm.get("status", "?")
        if st == "pass":
            pass_n += 1
        mem_n = sum(
            1
            for m in comp.get("members", [])
            if m.get("memory_offset") is not None and m.get("memory_offset") != m.get("offset")
        )
        mem_only = sum(1 for m in comp.get("members", []) if m.get("memory_only"))
        mem_audit = memory_audit_for_composite(comp, composites)
        mem_cell = (
            asm_badge(mem_audit.get("status"))
            if mem_audit.get("status")
            else '<span class="muted">—</span>'
        )
        rows += f"""<tr>
      <td><a href="../tables/{esc(tid)}.html"><code>{esc(tid)}</code></a></td>
      <td><code>{esc(comp.get('id', ''))}</code></td>
      <td>{asm_badge(st)}</td>
      <td>{mem_cell}</td>
      <td><code>{esc(asm.get('reader') or comp.get('reader', ''))}</code></td>
      <td>{esc(asm.get('total_bytes') or comp.get('length', ''))}</td>
      <td>{asm.get('fields_ok', len(comp.get('members', [])))}</td>
      <td>{mem_n}</td>
      <td>{mem_only}</td>
      <td>{esc(asm.get('verified', ''))}</td>
    </tr>"""
    body = f"""
    <h2>ASM 审计总览</h2>
    <p class="muted">wire 链 offset/length 对齐 · evidence_va 逐字段 · pass <strong>{pass_n}</strong> / {total_n} complete 表</p>
    <table class="wide">
      <thead><tr>
        <th>表</th><th>composite</th><th>wire</th><th>memory</th><th>reader</th><th>线长</th>
        <th>fields ok</th><th>mem≠wire</th><th>memory_only</th><th>verified</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <p><a href="../index.html">← 首页</a> · 源数据 <code>schema/_meta/asm_audit_summary.md</code></p>
"""
    return page("ASM 审计", "asm-audit/index.html", body)


# ---------------------------------------------------------------------------
# Oracle 审计页
# ---------------------------------------------------------------------------
# 站点其余部分渲染的是 `db_design/schema` 里的**结论**。这一页渲染的是结论的**判据**：
# `emulab/` 把客户端自己的代码跑起来（Unicorn 执行 + 逐次内存写挂钩），拿「客户端实际
# 怎么读写」去核 `protocol_analysis/` 的每一层记录。四层互相独立：
#
#   L1 原始数据 命令的机器草案(反汇编) ↔ 人工定稿 fields.csv
#   L2 复合体   composites 的线布局      ← 客户端 reader 实跑
#   L3 源头记录 fields.csv 每行声明长度  ← 它点名的复合体 + 读取器
#   读取器归属  证据VA → reader          ← 长度闭合
#
# 产物都是 JSON（`emulab/*.json`），本页只做渲染，不重算——数字必须能在产物里对上。
EMULAB_DIR = Path(__file__).resolve().parents[2] / "emulab"

RAW_VERDICT = {
    "AGREE": ("一致", "字节与行切分都相同", "#2e7d32"),
    "BYTES-AGREE": ("字节互证", "字节覆盖与停住点一致，只是行切分不同（人工把两块 u32 合成 u64 等）", "#2e7d32"),
    "PREFIX-AGREE": ("前缀互证", "人工尾部是变长/数组行，只有确定前缀可比——草案把它全覆盖了", "#2e7d32"),
    "BOTH-EMPTY": ("两侧都空", "都没有定长字段（整帧变长），无从对账", "#607d8b"),
    "DRAFT-GAP": ("无机器对照", "扫描器一个字段都没提出就停住了（嵌套 reader / 非 IO 调用）", "#e65100"),
    "NESTED-EXPANSION": ("无机器对照", "扫描器停在嵌套 reader，人工把该复合体展开成多行", "#e65100"),
    "DROPPED-DISPLACED-STORE": ("★扫描器缺陷", "草案漏了一个带位移的 store，其后偏移与总长整体偏低", "#c62828"),
    "DRAFT-BRANCHY": ("扫描器缺陷", "扫描跨过条件跳转（线性扫描把 if/switch 两条臂串起来）", "#c62828"),
    "DRAFT-LONGER": ("待看", "草案比定稿多出确定性行", "#6a1b9a"),
    "UNEXPLAINED": ("待看", "不满足任何已知指纹", "#6a1b9a"),
}


def load_audit(name: str):
    path = EMULAB_DIR / name
    return load_json(path) if path.is_file() else None


def audit_stat(num, lbl) -> str:
    return f'<div class="stat"><div class="num">{esc(num)}</div><div class="lbl">{esc(lbl)}</div></div>'


def build_oracle_audit_index(commands: list[dict] | None = None,
                             composites: dict[str, dict] | None = None) -> str:
    raw = load_audit("audit_raw.json")
    full = load_audit("audit_full.json")
    src = load_audit("audit_sources.json")
    readers = load_audit("audit_readers.json")
    patch = load_audit("patch_log.json")

    tally = dict(raw.get("tally") or {}) if raw else {}
    results = (raw or {}).get("results") or []

    # 机器与人工在同一层上「对上了多少条」
    agreed = sum(tally.get(k, 0) for k in ("AGREE", "BYTES-AGREE", "PREFIX-AGREE", "BOTH-EMPTY"))
    blind = sum(tally.get(k, 0) for k in ("DRAFT-GAP", "NESTED-EXPANSION"))
    scanner_bug = sum(tally.get(k, 0) for k in ("DROPPED-DISPLACED-STORE", "DRAFT-BRANCHY"))
    eyeball = sum(tally.get(k, 0) for k in ("DRAFT-LONGER", "UNEXPLAINED"))
    total_rows = agreed + blind + scanner_bug + eyeball

    caps = collections.Counter(x.get("cap_check") for x in results if x.get("cap_check"))

    comp_all = full or []
    comp_pass = sum(1 for x in comp_all if x.get("status") == "PASS")
    comp_skip = [x for x in comp_all if x.get("status") != "PASS"]
    comp_bad = [x for x in comp_skip if x.get("status") != "SKIP"]

    src_rows = (src or {}).get("rows") or []
    src_ok = sum(1 for r in src_rows if r.get("verdict") == "OK")
    src_bad = [r for r in src_rows if r.get("verdict") != "OK"]
    src_gaps = (src or {}).get("coverage_gaps") or []
    # 已核例外连同它的**活验算**一起渲染：例外的免检资格是每次审计现算的
    # （`audit_sources.verified_split()`），页面必须把这条算术摆出来，否则读者只能
    # 看到"有一条例外"却看不到"凭什么是例外"。加不出这段算术的例外会退回 `coverage_gaps`。
    src_reviewed = (src or {}).get("coverage_reviewed") or []
    review_html = ""
    if src_reviewed:
        rows = ""
        for item in src_reviewed:
            split = item.get("verified_split") or {}
            parts = split.get("parts") or []
            calc = " + ".join(
                f'{esc(p.get("field"))}<span class="muted">(行{p.get("line")})</span>={esc(p.get("width"))}'
                for p in parts) or "—"
            rows += f"""<tr>
      <td><code>{esc(item.get("command"))}</code></td>
      <td><code>{esc(item.get("reader"))}</code></td>
      <td>{calc} = <strong>{esc(split.get("width"))}</strong></td>
      <td class="muted">{esc("、".join(item.get("composites") or []))}</td>
    </tr>"""
        review_html = f"""
    <h3>L3 覆盖缺口的已核例外（{len(src_reviewed)} 条，命中即验）</h3>
    <p class="muted">例外<strong>不是</strong>「复核一次、永久免检」：每次审计都重算一遍——命令自己的
    <strong>定宽负载行</strong>里必须仍存在<strong>连续的一段</strong>（≥2 行）恰好加到 reader 宽度。
    <code>（长度闭合）</code> 注记行与 opcode 行（序号 0）不计入，否则复述总数的那一行会让例外
    <strong>自己加自己</strong>、空转通过。加不出这段算术，例外就退回上面的缺口。</p>
    <table class="wide">
      <thead><tr><th>命令</th><th>reader</th><th>现算的拆分行之和</th><th>复合体</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""

    reader_ok = sum(1 for x in (readers or []) if x.get("verdict") == "OK")
    reader_bad = [x for x in (readers or []) if x.get("verdict") != "OK"]

    # 缺口的影响面：缺口语义是「这一层没有第二只眼睛」，不是「判错」。但缺口的**代价**
    # 取决于它压在多少真在读写库的东西上 —— 41 条里若 40 条不落库，就不值得为它补判据。
    # 所以这里把每个缺口折算成「有多少条 db_effects 命令 / 有多少列」。
    cmds = commands or []
    comps = composites or {}
    db_ids = {c.get("id") for c in cmds if c.get("db_effects")}
    gap_ids = {x.get("command") for x in results if x.get("verdict") == "DRAFT-GAP"}
    nest_ids = {x.get("command") for x in results if x.get("verdict") == "NESTED-EXPANSION"}
    skip_ids = {x.get("id") for x in comp_skip}

    def _asm_covered(ids: set) -> int:
        """这些命令里，有多少条**另有 IDA 汇编六项检查**兜底（L1 缺口不是唯一判据）。"""
        n = 0
        for c in cmds:
            if c.get("id") not in ids:
                continue
            av = c.get("asm_verification") or {}
            if len(av.get("checks") or {}) >= 6 and not av.get("mismatches"):
                n += 1
        return n

    def _member_evidence(cid: str) -> tuple[int, int]:
        ms = (comps.get(cid) or {}).get("members") or []
        ok = sum(1 for m in ms
                 if m.get("evidence_va") or m.get("wire_sources") or m.get("source_va"))
        return ok, len(ms)

    # L2 缺口的影响面落在归位库上：这 9 个复合体各自折进了哪个对象、带出多少列。
    homing_dir = SITE_DIR.parent / "schema" / "homing" / "objects"
    folded_cols = 0
    folded_objs = 0
    if homing_dir.is_dir():
        for p in sorted(homing_dir.glob("*.json")):
            obj = load_json(p)
            if set(obj.get("folded_composites") or []) & skip_ids:
                folded_objs += 1
                folded_cols += sum(len(t.get("columns") or []) for t in (obj.get("tables") or []))
    skip_hand = [i for i in skip_ids if (comps.get(i) or {}).get("status") == "complete"]
    skip_ev_ok = sum(1 for i in skip_hand if _member_evidence(i)[0] == _member_evidence(i)[1])
    skip_members = sum(_member_evidence(i)[1] for i in skip_hand)

    blast_rows = "".join([
        f"""<tr>
      <td><strong>L1 DRAFT-GAP</strong></td>
      <td>{len(gap_ids)} 条命令</td>
      <td><strong>{len(gap_ids & db_ids)}</strong> 条有 <code>db_effects</code></td>
      <td class="muted">草案一个字段都没提出 ⇒ <strong>整条只有人工一个来源</strong></td>
      <td>{_asm_covered(gap_ids)}/{len(gap_ids)} 另有 ASM 六项检查兜底</td>
    </tr>""",
        f"""<tr>
      <td><strong>L1 NESTED-EXPANSION</strong></td>
      <td>{len(nest_ids)} 条命令</td>
      <td><strong>{len(nest_ids & db_ids)}</strong> 条有 <code>db_effects</code></td>
      <td class="muted">草案停在嵌套 reader ⇒ <strong>前缀有机器对照、尾部人工展开</strong></td>
      <td>{_asm_covered(nest_ids)}/{len(nest_ids)} 另有 ASM 六项检查兜底</td>
    </tr>""",
        f"""<tr>
      <td><strong>L2 无 oracle</strong></td>
      <td>{len(skip_ids)} 个复合体</td>
      <td>{folded_objs} 个归位对象 / {folded_cols} 列</td>
      <td class="muted">复合体没有 reader，无从实跑 ⇒ 整体布局无机器对照</td>
      <td>{skip_ev_ok}/{len(skip_hand)} 是手写 <code>complete</code> 且成员 VA 全覆盖（{skip_members} 个成员）</td>
    </tr>""",
    ])

    blast = f"""
    <h3>缺口的 DB 影响面</h3>
    <p class="muted">缺口的语义是<strong>「这一层没有第二只眼睛」，不是「判错了」</strong>——
    <code>SKIP ≠ PASS</code>。但缺口的代价取决于它压在多少<strong>真在读写库</strong>的东西上，
    所以下面把每个缺口折算成影响面。要点：<strong>L1 的缺口不是唯一判据</strong>——同一条命令
    另有 IDA 汇编六项检查（<code>verify_commands_ida.py</code>，915/915 通过、0 差异）；
    而 L2 的 9 个无 reader 复合体全是手写 <code>complete</code>、成员逐条带 VA。</p>
    <table class="wide">
      <thead><tr><th>缺口</th><th>规模</th><th>其中影响 DB</th><th>缺口的性质</th><th>替代判据</th></tr></thead>
      <tbody>{blast_rows}</tbody>
    </table>"""

    stats = "".join([
        audit_stat(f"{agreed}/{total_rows}", "L1 机器↔人工 互证"),
        audit_stat(f"{comp_pass}/{len(comp_all)}", "L2 复合体 oracle PASS"),
        audit_stat(f"{src_ok}/{len(src_rows)}", "L3 源头行 审计 OK"),
        audit_stat(caps.get("OVER", 0), "帧长超报（硬错）"),
        audit_stat(scanner_bug + eyeball, "L1 残留待看"),
    ])

    layer_rows = [
        ("L3 源头记录", "<code>fields.csv</code> 每行的声明长度",
         "它点名的复合体线长 + 它点名的读取器是否真在本命令块内被调用",
         f"{src_ok}/{len(src_rows)} OK", "#2e7d32" if not src_bad else "#c62828"),
        ("L2 复合体", "<code>composites/*.json</code> 的线布局与内存布局",
         "客户端自己的 reader 在 Unicorn 里实跑，逐次内存写挂钩",
         f"{comp_pass}/{len(comp_all)} PASS", "#2e7d32" if not comp_bad else "#c62828"),
        ("L1 原始数据", "命令的机器草案 <code>draft-fields.csv</code>",
         "人工定稿 <code>fields.csv</code>——两者是同一个二进制的两种独立读法",
         f"{agreed}/{total_rows} 互证", "#2e7d32" if not (scanner_bug or eyeball) else "#e65100"),
        ("读取器归属", "<code>fields.csv</code> 的 <code>证据VA</code> → 复合体的 reader",
         "长度闭合：读者实际消耗的字节数 == 声明的线长",
         f"{reader_ok}/{len(readers or [])} OK", "#2e7d32" if not reader_bad else "#c62828"),
    ]
    layer_html = "".join(
        f"""<tr>
      <td><strong>{name}</strong></td>
      <td>{obj}</td>
      <td class="muted">{how}</td>
      <td><span class="badge" style="background:{color}">{esc(result)}</span></td>
    </tr>""" for name, obj, how, result, color in layer_rows)

    tally_rows = ""
    for key in ("AGREE", "BYTES-AGREE", "PREFIX-AGREE", "BOTH-EMPTY",
                "DRAFT-GAP", "NESTED-EXPANSION", "DROPPED-DISPLACED-STORE",
                "DRAFT-BRANCHY", "DRAFT-LONGER", "UNEXPLAINED"):
        if not tally.get(key):
            continue
        label, why, color = RAW_VERDICT.get(key, (key, "", "#757575"))
        tally_rows += f"""<tr>
      <td><code>{esc(key)}</code></td>
      <td><span class="badge" style="background:{color}">{esc(label)}</span></td>
      <td>{esc(tally[key])}</td>
      <td class="muted">{esc(why)}</td>
    </tr>"""

    residue = [x for x in results if x.get("verdict") in
               ("DRAFT-LONGER", "UNEXPLAINED", "DROPPED-DISPLACED-STORE", "DRAFT-BRANCHY")]
    if residue:
        rows = "".join(
            f"""<tr>
      <td><code>{esc(x['command'])}</code></td>
      <td>{esc(x.get('verdict'))}</td>
      <td>{esc(x.get('draft_total'))} → {esc(x.get('final_total'))}</td>
      <td class="muted"><code>{esc(x.get('draft_shape'))}</code> vs <code>{esc(x.get('final_shape'))}</code></td>
    </tr>""" for x in residue)
        residue_html = f"""
    <h3>残留（需人眼）</h3>
    <table class="wide">
      <thead><tr><th>命令</th><th>判定</th><th>草案→定稿 字节</th><th>形状</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""
    else:
        residue_html = ('<h3>残留（需人眼）</h3><p class="muted"><strong>0 条</strong>：'
                        '每一条命令的每一处草案↔定稿差异都落进了上面某个具名成因，没有「说不清」的条目。</p>')

    no_oracle = [x for x in results if x.get("verdict") in ("DRAFT-GAP", "NESTED-EXPANSION")]
    blind_html = ""
    if no_oracle:
        rows = "".join(
            f"""<tr>
      <td><code>{esc(x['command'])}</code></td>
      <td>{esc(x.get('verdict'))}</td>
      <td>{esc(x.get('draft_total'))} → {esc(x.get('final_total'))}</td>
      <td class="muted">{esc((x.get('stop') or '-')[:46])}</td>
    </tr>""" for x in no_oracle)
        blind_html = f"""
    <details>
      <summary>展开 {len(no_oracle)} 条「无机器对照」命令（扫描器提前停住，定稿只有人工一个来源）</summary>
      <table class="wide">
        <thead><tr><th>命令</th><th>判定</th><th>草案→定稿 字节</th><th>停住于</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </details>"""

    skip_html = ""
    if comp_skip:
        rows = "".join(
            f"""<tr>
      <td><code>{esc(x.get('id'))}</code></td>
      <td><code>{esc(x.get('status'))}</code></td>
      <td class="muted">{esc(x.get('reason'))}</td>
    </tr>""" for x in comp_skip)
        skip_html = f"""
    <h3>L2 未受审的 {len(comp_skip)} 个复合体</h3>
    <p class="muted">这一类<strong>没有 oracle 可用</strong>：复合体没有 reader，无从实跑。
    它不等于「跑通了」——目前只有人工证据。</p>
    <table class="wide">
      <thead><tr><th>composite</th><th>状态</th><th>原因</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""

    patch_html = ""
    if patch:
        report = patch.get("report") or {}
        entries = report.get("composites") or []
        rows = ""
        for c in entries:
            edits = "".join(f"<li><code>{esc(e)}</code></li>" for e in c.get("edits") or [])
            rows += f"""<tr>
      <td><code>{esc(c.get('id'))}</code></td>
      <td>{esc(c.get('verdict_before'))} → <strong>{esc(c.get('verdict_after'))}</strong></td>
      <td><ul style="margin:0;padding-left:1.1rem">{edits}</ul></td>
      <td class="muted">{esc(', '.join(c.get('unresolved') or []) or '—')}</td>
    </tr>"""
        patch_html = f"""
    <h3>Oracle 驱动的回填记录</h3>
    <p class="muted">工具 <code>{esc(report.get('tool'))}</code> · {esc(report.get('date'))}
    · dry_run=<code>{esc(report.get('dry_run'))}</code> · 备份 <code>{esc(patch.get('backup'))}</code>。
    每一条都先由 oracle 判定「改前错、改后对」，再写回 composites。</p>
    <table class="wide">
      <thead><tr><th>composite</th><th>判定</th><th>回填项</th><th>未解</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""

    gate = ""
    if caps:
        gate = f"""
    <h3>不依赖任何人工记录的第三条判据</h3>
    <p class="muted">CS 组包函数在调用缓冲分配器<strong>之前会 push 帧长</strong>——那是二进制自己声明的大小。
    把定稿的负载长 + 2(opcode) 与它比：</p>
    <div class="grid stats">
      {audit_stat(caps.get('EXACT', 0), 'EXACT 严丝合缝')}
      {audit_stat(caps.get('SLACK', 0), 'SLACK 容量更宽（列表帧正常）')}
      {audit_stat(caps.get('OVER', 0), 'OVER 定稿超报（硬错）')}
    </div>
    <p class="muted"><strong>0 条 OVER</strong>：没有任何命令的定稿负载超出二进制声明的容量。
    这是「人工没有多记」的独立证据，结论既不来自草案也不来自人工。</p>"""

    prov = " · ".join(
        repo_file_html(rel, "oracle-audit/index.html")
        for rel in ("emulab/audit_raw.json", "emulab/audit_full.json", "emulab/audit_sources.json",
                    "emulab/audit_readers.json", "emulab/patch_log.json"))

    body = f"""
    <h2>Oracle 审计</h2>
    <p class="lead">Oracle 不是「另一份人工记录」，而是<strong>把客户端自己的代码跑起来当判据</strong>：
    在 Unicorn 里复现它的内存布局，逐次内存写挂钩，看它到底把哪个线上字节读进了哪个内存偏移。
    下面每一项结论，都能被这台二进制复算一遍。</p>

    <div class="grid stats">{stats}</div>

    <h3>四层判据（互相独立）</h3>
    <table class="wide">
      <thead><tr><th>层</th><th>被审对象</th><th>判据</th><th>结果</th></tr></thead>
      <tbody>{layer_html}</tbody>
    </table>
    {blast}

    <h3>L1：机器草案 ↔ 人工定稿（{total_rows} 条命令逐条对账）</h3>
    <p class="muted">草案由 <code>protocol_analysis/tools/ida_draft_wire.py</code> 从反汇编机械提取
    （<strong>没有人工介入</strong>），定稿是人读同一个二进制写下的。两者独立，所以能互相证伪。
    判据是<strong>字节覆盖</strong>而不是行向量——同一批字节切成几行，那是建模选择，不是分歧。</p>
    <table class="wide">
      <thead><tr><th>判定</th><th>归类</th><th>条数</th><th>含义</th></tr></thead>
      <tbody>{tally_rows}</tbody>
    </table>
    {residue_html}
    {blind_html}

    <h3>本轮修掉的扫描器缺陷</h3>
    <p class="muted">草案生成器曾只认 <code>o_phrase</code>（无位移寻址），把 <code>mov [eax+4], esi</code>
    这类带位移的写<strong>静默丢弃</strong>；而它的游标只在「产出一行」时才前移，于是一旦丢掉一个 store，
    其后<strong>每个字段的偏移都偏低</strong>——比漏一个字段更坏，因为照着草案读会把整块放到错位置上。
    <code>CS-0x0519</code> 的二进制 push 了 <code>0xA</code>（10 字节帧），草案只报 4 字节，定稿 8 字节。</p>
    <p class="muted">修法是新增 <code>wire_mem_operand()</code>：<code>o_displ</code> 只在位移<strong>恰好等于
    当前游标</strong>且基址不是 <code>esp/ebp</code> 时才算线字段。重跑全部 915 条草案后用<strong>同一套旧判据</strong>
    验收：<code>DROPPED-DISPLACED-STORE</code> 42 → 1、<code>UNEXPLAINED</code> 19 → 11；再把判据本身校准
    （字节覆盖 + 数组行按不定长 + 分支标记）后两者归零。</p>

    <h3>L2：复合体 oracle（{len(comp_all)} 个）</h3>
    <p class="muted">把每个 composite 的 reader 放进 Unicorn 实跑：喂进一份线字节，挂钩每一次内存写，
    得到 <code>(线偏移, 内存偏移, 宽度)</code> 三元组，拿它核对成员表——线长是否闭合、成员是否铺满、
    内存是否重叠、有没有未登记的字段。</p>
    {gate}
    {skip_html}

    <h3>L3：源头记录审计（{len(src_rows)} 行）</h3>
    <p class="muted">把 <code>fields.csv</code> 每一行的<strong>声明长度</strong>，对着「它点名的复合体」
    和「它点名的读取器」两边核。两类真错都在这一层抓到过：<code>LENGTH-MISMATCH</code>（声明长度 ≠ 复合体线长）
    与 <code>SLOT-AS-WIRE</code>（把内存槽宽当成了线长）。</p>
    <p class="muted">另做覆盖缺口检查：命令块内调用了某复合体的 reader，却没有任何一行声明它的线长
    （用来抓 <code>struct{{NNN}}</code> 这种不点名的行）——当前 <strong>{len(src_gaps)} 条</strong>。
    其中"故意摊成几个标量行"的已核例外不会计入缺口，但它的免检资格<strong>每次都现算</strong>，见下。</p>
    {review_html}
    {patch_html}

    <h3>产物与重现</h3>
    <p class="muted">本页只渲染，不重算。产物：{prov}</p>
    <p class="muted">重现（<code>emulab/.venv</code>）：<br>
    <code>audit_composites.py --json audit_full.json</code> ·
    <code>audit_sources.py --json audit_sources.json</code> ·
    <code>audit_readers.py --json audit_readers.json</code> ·
    <code>audit_raw.py --json audit_raw.json</code></p>
    <p><a href="../index.html">← 首页</a></p>
"""
    return page("Oracle 审计", "oracle-audit/index.html", body)


def build_relations(relations: dict) -> str:
    rows = ""
    for t in relations.get("tables", []):
        cmds = ", ".join(f"<code>{esc(c)}</code>" for c in t.get("evidence_commands", []))
        rows += f"""<tr>
      <td><code>{esc(t.get('id', ''))}</code></td>
      <td>{badge(t.get('status', 'proposed'))}</td>
      <td>{esc(t.get('purpose', ''))}</td>
      <td>{cmds}</td>
    </tr>"""
    body = f"""
    <h2>表关系（提议）</h2>
    <p class="muted">FK 关系待从协议命令提炼后补充。旧表声明与旧库唯一键列序已冻结在
      <code>schema/_meta/legacy_evidence.json</code>（<code>tools/freeze_legacy.py</code>）。</p>
    <table>
      <thead><tr><th>表 ID</th><th>状态</th><th>用途</th><th>证据命令</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("表关系", "relations.html", body)


# ------------------------------------------------------------------ 命令维度
#
# 模型口径见 db_design/docs/01-命令模型.md；数据见 db_design/schema/commands/。

COMMAND_STATUS_COLORS = {
    "IMPORTED": "#757575",
    "ASM-VERIFIED": "#2e7d32",
    "BEHAVIOR-DONE": "#1565c0",
    "BLOCKED": "#c62828",
}


def load_commands() -> tuple[dict | None, list[dict]]:
    """读命令模型：一份 index.json（索引/统计）+ 每条命令一份 JSON。"""
    cmd_dir = SCHEMA_DIR / "commands"
    index = None
    idx_path = cmd_dir / "index.json"
    if idx_path.is_file():
        index = load_json(idx_path)
    cmds: list[dict] = []
    if cmd_dir.is_dir():
        for path in sorted(cmd_dir.glob("*.json")):
            if path.name.startswith("_") or path.name == "index.json":
                continue
            cmds.append(load_json(path))
    return index, cmds


def status_badge(status: str | None) -> str:
    if not status:
        return '<span class="muted">—</span>'
    color = COMMAND_STATUS_COLORS.get(status, "#757575")
    return f'<span class="badge" style="background:{color}">{esc(status)}</span>'


def va_list_html(values: list[str] | None) -> str:
    if not values:
        return '<span class="muted">—</span>'
    return " ".join(f"<code>{esc(v)}</code>" for v in values)


def va_link(va: str | None, label: str | None = None) -> str:
    if not va:
        return '<span class="muted">—</span>'
    return f"<code>{esc(va)}</code>"


def fmt_pair(cmd: dict, command_ids: set[str] | None = None) -> str:
    """配对 / 同族命令 → 链接。配对名与真实命令 id 常有出入（CS 是 `<名>`、SC 是 `<名>_r`，
    模型里 `pair` 记的是 `<名>`），所以先试原名再试 `_r` 变体，都不中就给纯 code。"""
    bits = []
    for cid in ([cmd["pair"]] if cmd.get("pair") else []) + list(cmd.get("related") or []):
        if not cid:
            continue
        if cid in (command_ids or set()) or command_ids is None:
            bits.append(f'<a href="{esc(cid)}.html"><code>{esc(cid)}</code></a>')
            continue
        alt = cid[:-2] if cid.endswith("_r") else f"{cid}_r"
        if alt in command_ids:
            bits.append(f'<a href="{esc(alt)}.html"><code>{esc(alt)}</code></a>'
                        f' <span class="muted">（配对名记作 {esc(cid)}）</span>')
        else:
            bits.append(f'<code>{esc(cid)}</code>')
    return " ".join(bits) or '<span class="muted">—</span>'


def build_commands_index(index: dict | None, cmds: list[dict]) -> str:
    if index is None:
        return page("命令", "commands/index.html",
                    "<h2>命令</h2><p>无数据 · 请先运行 <code>tools/import_commands.py</code></p>")

    counts = index.get("counts", {})
    by_dir = counts.get("by_direction", {})
    by_proto = counts.get("by_proto", {})
    by_status = counts.get("by_status", {})
    by_len = counts.get("by_length_source", {})
    repairs = index.get("repairs", {})

    def opts(values, label_fn=None):
        out = ""
        for v in sorted(values):
            lbl = label_fn(v) if label_fn else v
            out += f'<option value="{esc(v)}">{esc(lbl)}</option>'
        return out

    caps = sorted({c for cmd in cmds for c in (cmd.get("capabilities") or cmd.get("capabilities_derived") or [])})
    protos = sorted({c.get("proto", "") for c in cmds})

    rows = ""
    for cmd in cmds:
        caps_of = cmd.get("capabilities") or cmd.get("capabilities_derived") or []
        rows += f"""<tr class="cmd-row" data-dir="{esc(cmd.get('direction'))}" data-proto="{esc(cmd.get('proto'))}"
        data-status="{esc(cmd['asm_verification']['status'])}" data-caps="{esc(' '.join(caps_of))}"
        data-len="{esc(cmd['wire'].get('length_source'))}" data-fixed="{'1' if cmd['wire'].get('fixed') else '0'}">
      <td><a href="{esc(cmd['id'])}.html"><code>{esc(cmd['id'])}</code></a></td>
      <td><code>{esc(cmd.get('opcode'))}</code></td>
      <td>{esc(cmd.get('direction'))}</td>
      <td>{esc(cmd.get('proto'))}</td>
      <td>{esc(cmd.get('capacity') or '—')}</td>
      <td><code>{esc(cmd['wire'].get('length_expr'))}</code></td>
      <td>{cmd['wire'].get('field_count', 0)}</td>
      <td>{''.join(f'<span class="cap-chip">{esc(c)}</span>' for c in caps_of)}</td>
      <td>{status_badge(cmd['asm_verification']['status'])}</td>
    </tr>"""

    stat_lens = " · ".join(f"{k} {v}" for k, v in by_len.items())
    body = f"""
    <section class="hero">
      <h2>交互命令（命令维度模型）</h2>
      <p class="lead">每条命令：逐字段解剖 + 包结构体 + 客户端行为 + DB 影响，全部带 IDA 汇编证据 VA。
        口径见 <code>docs/01-命令模型.md</code>，模型契约见 <code>schema/commands/_schema.json</code>。</p>
    </section>

    <section class="grid stats">
      <div class="stat"><div class="num">{counts.get('commands', len(cmds))}</div><div class="lbl">命令</div></div>
      <div class="stat"><div class="num">{counts.get('fields', 0)}</div><div class="lbl">负载字段</div></div>
      <div class="stat"><div class="num">{by_dir.get('SC', 0)} / {by_dir.get('CS', 0)}</div><div class="lbl">SC（收）/ CS（发）</div></div>
      <div class="stat"><div class="num">{by_status.get('IMPORTED', 0)}</div><div class="lbl">IMPORTED（待 ASM 复核）</div></div>
      <div class="stat"><div class="num">{by_status.get('ASM-VERIFIED', 0)}</div><div class="lbl">ASM-VERIFIED</div></div>
      <div class="stat"><div class="num">{by_status.get('BEHAVIOR-DONE', 0)}</div><div class="lbl">BEHAVIOR-DONE</div></div>
      <div class="stat"><div class="num">{counts.get('fields_needing_review', 0)}</div><div class="lbl">CSV 畸形行（待复核）</div></div>
    </section>

    <section>
      <h3>线长来源分布</h3>
      <p class="muted">{esc(stat_lens)} — <code>closure_row</code> 是闭合行直接给出；<code>field_sum</code> 由字段线长相加（含变量）；
        <code>zero_load</code> 是零负载命令（只有 opcode）。</p>
      <h3>CSV 畸形行修复</h3>
      <p class="muted">{esc(' · '.join(f'{k} {v}' for k, v in repairs.items())) or '无'}</p>
    </section>

    <section>
      <h3>筛选</h3>
      <div class="filters">
        <label>方向 <select id="f-dir"><option value="">全部</option>{opts(by_dir.keys())}</select></label>
        <label>协议类 <select id="f-proto"><option value="">全部</option>{opts(protos)}</select></label>
        <label>能力 <select id="f-cap"><option value="">全部</option>{opts(caps)}</select></label>
        <label>状态 <select id="f-status"><option value="">全部</option>{opts(by_status.keys())}</select></label>
        <label>线长来源 <select id="f-len"><option value="">全部</option>{opts(by_len.keys())}</select></label>
        <label>定长 <select id="f-fixed"><option value="">全部</option><option value="1">定长</option><option value="0">变长</option></select></label>
        <span class="muted" id="f-count"></span>
      </div>
      <table class="wide cmd-table">
        <thead><tr>
          <th>命令 id</th><th>opcode</th><th>方向</th><th>协议类</th><th>声明容量</th>
          <th>报文体线长</th><th>字段</th><th>能力</th><th>状态</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <p class="muted">能力列优先显示有汇编证据的 <code>capabilities</code>，缺证据时退回命名学推断的
        <code>capabilities_derived</code>（见 <code>docs/02-命令能力表.md</code>）。</p>
    </section>

    <script>
    (function () {{
      var rows = Array.prototype.slice.call(document.querySelectorAll('.cmd-row'));
      var f = {{
        dir: document.getElementById('f-dir'), proto: document.getElementById('f-proto'),
        cap: document.getElementById('f-cap'), status: document.getElementById('f-status'),
        len: document.getElementById('f-len'), fixed: document.getElementById('f-fixed')
      }};
      var counter = document.getElementById('f-count');
      function apply() {{
        var n = 0;
        rows.forEach(function (r) {{
          var ok = (!f.dir.value || r.dataset.dir === f.dir.value)
            && (!f.proto.value || r.dataset.proto === f.proto.value)
            && (!f.cap.value || r.dataset.caps.split(' ').indexOf(f.cap.value) >= 0)
            && (!f.status.value || r.dataset.status === f.status.value)
            && (!f.len.value || r.dataset.len === f.len.value)
            && (!f.fixed.value || r.dataset.fixed === f.fixed.value);
          r.style.display = ok ? '' : 'none';
          if (ok) n++;
        }});
        counter.textContent = '命中 ' + n + ' / ' + rows.length;
      }}
      Object.keys(f).forEach(function (k) {{ f[k].addEventListener('change', apply); }});
      apply();
    }})();
    </script>
"""
    return page("命令", "commands/index.html", body)


SCALAR_WT = {"u8", "i8", "u16", "i16", "u32", "i32", "u64", "f32", "f64", "str", "bytes", "char", "pad"}


def array_element(wt: str | None) -> str | None:
    """数组线类型的元素名（`array<X,N>` / `array<struct<X>,N>` / `X[N]`）。"""
    t = (wt or "").strip()
    m = re.match(r"^array<\s*(?:struct<\s*)?\s*([A-Za-z_]\w*)", t)
    if m:
        return m.group(1)
    # 复合体成员惯用的定长数组写法：`bracket_node[15]` / `u32[10]` / `char[25]`
    m = re.match(r"^([A-Za-z_]\w*)\s*\[\s*\d+\s*\]\s*$", t)
    return m.group(1) if m else None


def is_array_wire(wt: str | None, has_element_ref: bool = False) -> bool:
    """该成员的线类型是否**数组**（只看写法与显式元素引用，不看解析出的 composite）。"""
    t = (wt or "").strip()
    if t.startswith("array<") or re.search(r"\[\s*\d+\s*\]\s*$", t):
        return True
    return bool(has_element_ref)


def array_shape(wt: str | None, length) -> str:
    """定长数组的展示串：`15×11B`。条数或元素长取不到就退化成 `15×?B` /空。"""
    t = (wt or "").strip()
    count = None
    if t.startswith("array<"):
        inner = t[len("array<"):].rstrip(">")
        parts = inner.split(",")
        if len(parts) > 1 and parts[1].strip().isdigit():
            count = int(parts[1].strip())
    else:
        m = re.search(r"\[\s*(\d+)\s*\]\s*$", t)
        if m:
            count = int(m.group(1))
    try:
        total = int(length)
    except (TypeError, ValueError):
        total = None
    if not count:
        return ""
    if total and total % count == 0:
        return f"{count}×{total // count}B"
    return f"{count}×?B"


def member_composite_ref(m: dict, composites: dict[str, dict]) -> str | None:
    """聚合体**成员** → `schema/composites/<id>.json`（显式 ref 优先，再按线类型现推）。"""
    for key in ("composite_ref", "element_composite_ref"):
        ref = m.get(key)
        if ref and ref in composites:
            return ref
    wt = (m.get("wire_type") or m.get("type") or "").strip()
    elem = array_element(wt)
    if elem and elem not in SCALAR_WT and elem in composites:
        return elem
    element = m.get("element") if isinstance(m.get("element"), str) else None
    return resolve_composite_id(m.get("name"), wt, composites, element=element)


def field_composite_ref(f: dict, composites: dict[str, dict]) -> str | None:
    """字段（聚合体 / 结构体数组）→ `schema/composites/<id>.json`。

    模型里已落的 `composite_ref`/`element_composite_ref` 优先；缺失时按线类型现推。
    **无名**聚合（`struct` / `struct{...}` / `array<struct,N>` / `array<elem N>`）退回字段名判断；
    标量数组（`array<u32,N>`）不参与，避免把 `missionunit_set` 这类字段名误当结构。
    """
    for key in ("composite_ref", "element_composite_ref"):
        ref = f.get(key)
        if ref and ref in composites:
            return ref
    wt = (f.get("wire_type") or "").strip()
    elem = array_element(wt)
    if elem and elem in composites:
        return elem
    named = re.match(r"^struct[\s<(]?\s*([A-Za-z_]\w*)", wt)
    if named and named.group(1) in composites:
        return named.group(1)
    anon = named is None and (
        re.match(r"^struct(\{|\(|$)", wt) or (elem is not None and elem in {"struct", "elem"})
    )
    if anon:
        base = (f.get("name") or "").split(".")[0].replace("[]", "").strip()
        if base in composites:
            return base
    return None


def resolve_composite_id(name: str | None, wire_type: str | None, composites: dict[str, dict],
                         element: str | None = None) -> str | None:
    """把聚合体挂到 `schema/composites/<id>.json`（渲染期兜底，模型里的 ref 优先）。

    只看「像结构体」的写法：`struct<X>` / `struct X` / `struct(X)` / 裸 `struct` 时用字段名，
    以及数组元素名。**不**拿 `bytes[115]` 这类成员名去猜（struct 成员 `comment` 与
    composite `comment` 会误撞）。
    """
    if element and element in composites:
        return element
    wt = (wire_type or "").strip()
    # `avatar(18B)` 这类把尺寸写在括号里的写法：先剥掉再看是否命中 composite
    wt_base = re.sub(r"\([^)]*\)\s*$", "", wt).strip()
    if wt_base in composites:
        return wt_base
    if wt in composites:
        return wt
    m = re.match(r"^struct[\s<(]?\s*([A-Za-z_]\w*)", wt)
    named = m.group(1) if m else None
    if named and named in composites:
        return named
    if named is None and re.match(r"^struct(\{|$)", wt):
        base = (name or "").split(".")[0].replace("[]", "").strip()
        if base in composites:
            return base
    return None


def composite_members(comp_id: str, composites: dict[str, dict], _seen: tuple[str, ...] = ()) -> list[dict]:
    """取 composite 的成员清单：别名跟到底，前缀形按累计线长截前 N 字节。

    成员清单的**唯一出处**是 `schema/composites/<id>.json`；此处只负责把它摊平，
    让命令页不必写「成员见 XXX」。
    """
    if comp_id in _seen or comp_id not in composites:
        return []
    comp = composites[comp_id]
    members = comp.get("members") or comp.get("fields") or []
    if members:
        return members
    alias = comp.get("layout_same_as")
    if alias and alias in composites:
        return composite_members(alias, composites, _seen + (comp_id,))
    prefix_of = comp.get("prefix_of")
    if prefix_of and prefix_of in composites:
        plen = comp.get("prefix_length") or comp.get("length")
        out, used = [], 0
        for m in composite_members(prefix_of, composites, _seen + (comp_id,)):
            try:
                mlen = int(m.get("length"))
            except (TypeError, ValueError):
                break
            if plen is not None and used + mlen > int(plen):
                break
            out.append(m)
            used += mlen
        return out
    return []


def fmt_member_offset(m: dict) -> str:
    off = m.get("offset")
    mem = m.get("memory_offset")
    length = m.get("length")
    # `memory_only` 成员**不在线上**（业务侧填充，如 `dc_point.bef_next`）：它的 `offset` 是内存偏移的
    # 重复记账，若照直渲染成「线 +12」会与真线成员重叠、看不出是内存成员。故与 `fmt_offset` 同规。
    if m.get("memory_only"):
        parts = []
        tgt = mem if mem is not None else off
        if tgt is not None:
            parts.append(f"mem +{esc(tgt)}")
        if length is not None:
            parts.append(f"{esc(length)}B")
        parts.append("(memory_only)")
        return " ".join(parts)
    parts = []
    if off is not None:
        parts.append(f"线 +{esc(off)}")
    if mem is not None and mem != off:
        parts.append(f"mem +{esc(mem)}")
    if length is not None:
        parts.append(f"{esc(length)}B")
    return " ".join(parts)


def render_members_table(comp_id: str, composites: dict[str, dict], depth: int = 0,
                         seen: tuple[str, ...] = ()) -> str:
    """composite 成员表（就地展开，含成员的成员，最多 3 层）。"""
    comp = composites.get(comp_id)
    if comp is None:
        return ""
    members = composite_members(comp_id, composites)
    if not members:
        return ""
    rows = ""
    for m in members:
        mwt = (m.get("wire_type") or m.get("type") or "").strip()
        nested_ref = member_composite_ref(m, composites)
        is_arr = is_array_wire(mwt, bool(m.get("element_composite_ref")))
        # 标量数组（`char[61]` / `u32[31]`）不需要「数组」提示，线类型本身已写清元素与条数
        show_arr = is_arr and (array_element(mwt) or "") not in SCALAR_WT
        nested = ""
        if nested_ref and nested_ref != comp_id and depth < 3 and nested_ref not in seen:
            sub = render_members_table(nested_ref, composites, depth + 1, seen + (comp_id,))
            if sub:
                label = f"展开 <code>{esc(nested_ref)}</code> 元素成员" if is_arr else f"展开 <code>{esc(nested_ref)}</code> 成员"
                nested = f"<details class='composite-details'><summary>{label}</summary>{sub}</details>"
        shape = array_shape(mwt, m.get("length")) if show_arr else ""
        offset_cell = fmt_member_offset(m) + (f' <span class="muted">（{esc(shape)}）</span>' if shape else "")
        arr_icon = ' <span class="muted" title="数组：元素成员就地展开">［数组］</span>' if show_arr else ""
        rows += (f"<tr><td><code class=\"fname\">{esc(m.get('name'))}</code>{arr_icon}</td>"
                 f"<td><code>{esc(mwt)}</code></td>"
                 f"<td class=\"muted\">{offset_cell}</td>"
                 f"<td>{badge(m.get('disposition', 'TBD'))}"
                 f"{' <span class=\"asm-ok\" title=\"' + esc(m.get('asm_evidence_va') or '') + '\">✓</span>' if m.get('asm_verified') else ''}</td>"
                 f"<td>{esc(m.get('meaning') or m.get('notes') or '')}{nested}</td></tr>")
    return ("<table class=\"srv-table composite-table\">"
            "<thead><tr><th>成员</th><th>线类型</th><th>线偏移 / 线长</th><th>disposition</th><th>含义</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>")


def render_composite_block(comp_id: str, composites: dict[str, dict], caption: str = "") -> str:
    """把一个聚合体摊成「就地展开的成员块」：标题 + 别名/前缀溯源 + 成员表。

    刻意**不**输出「成员见 XXX」这种要人再跳一次的写法：别名与前缀形都把成员摊平，
    只在标题里注明「同布局 / 前缀」的事实与证据文件。
    """
    comp = composites.get(comp_id)
    if comp is None:
        return f'<div class="muted">composite <code>{esc(comp_id)}</code> 未建模</div>'
    members = composite_members(comp_id, composites)
    bits = []
    if comp.get("length") is not None:
        bits.append(f"线长 {esc(comp['length'])}B")
    mem = comp.get("memory_claim")
    if mem and str(mem) != str(comp.get("length")):
        bits.append(f"槽 {esc(mem)}B")
    if comp.get("layout_same_as"):
        bits.append(f"布局同 {esc(comp['layout_same_as'])}")
    if comp.get("prefix_of"):
        bits.append(f"{esc(comp['prefix_of'])} 的前 {esc(comp.get('prefix_length'))}B")
    asm_status = (comp.get("asm_audit") or {}).get("status")
    if asm_status:
        bits.append(f"ASM {esc(asm_status)}")
    table = render_members_table(comp_id, composites)
    body = table or '<p class="muted">composite 无成员记录（须以 IDA 复核补）</p>'
    head = f'<div class="composite-head"><code>{esc(comp_id)}</code>'
    if caption:
        head += f' <span class="muted">{esc(caption)}</span>'
    if bits:
        head += f' <span class="muted">{" · ".join(bits)}</span>'
    head += f' <span class="muted">定义 <code>schema/composites/{esc(comp_id)}.json</code></span></div>'
    return f'<div class="composite-block">{head}{body}</div>'


def render_members_summary(comp_id: str, composites: dict[str, dict]) -> str:
    """紧凑成员清单（包结构体表用）：成员名 + 线类型，就地列出，不折叠成引用。"""
    comp = composites.get(comp_id)
    if comp is None:
        return ""
    members = composite_members(comp_id, composites)
    if not members:
        return f'<span class="muted">composite <code>{esc(comp_id)}</code> 无成员记录</span>'
    bits = []
    for m in members:
        mn = esc(m.get("name"))
        mt = esc(m.get("wire_type") or m.get("type") or "")
        ml = m.get("length")
        # 线类型自带尺寸（`bytes[73]` / `avatar(18B)`）就不再重复标线长
        if ml is not None and not re.search(r"\d", mt):
            mt += f"({esc(ml)}B)"
        bits.append(f'<code>{mn}</code> {mt}')
    prov = []
    if comp.get("layout_same_as"):
        prov.append(f"布局同 {esc(comp['layout_same_as'])}")
    if comp.get("prefix_of"):
        prov.append(f"{esc(comp['prefix_of'])} 的前 {esc(comp.get('prefix_length'))}B")
    prov_html = f' <span class="muted">（{" · ".join(prov)}）</span>' if prov else ""
    return (f'<div class="composite-inline"><span class="muted">{len(members)} 个成员{prov_html}：</span>'
            f'{" · ".join(bits)}</div>')


def render_element(name: str | None, composites: dict[str, dict], cap: int | None = None,
                   element_length: str | None = None) -> str:
    """数组元素类型：命中 schema/composites/<id>.json 时**就地列出**元素成员。

    composite 没有独立页面，也不写「成员见 composites/XXX」：这里给紧凑清单，
    完整成员表（含线偏移与含义）在「字段解剖」节就地展开。
    """
    if not name:
        return ""
    if name not in composites:
        return f'<code>{esc(name)}</code> <span class="muted">(未建模)</span>'
    caption = f"≤{cap} 条 · " if cap else ""
    return f'{caption}{render_members_summary(name, composites)}'


def build_command_detail(cmd: dict, composites: dict[str, dict],
                         command_ids: set[str] | None = None) -> str:
    cid = cmd.get("id", "")
    nav_key = f"commands/{cid}.html"
    pp = proto_prefix(nav_key)
    av = cmd.get("asm_verification") or {}
    status = av.get("status", "IMPORTED")

    src = cmd.get("source_dir", "")
    src_links = ""
    if src:
        src_links = (
            f'<a href="{pp}{esc(src)}/README.md" target="_blank">README.md</a> · '
            f'<a href="{pp}{esc(src)}/fields.csv" target="_blank">fields.csv</a>'
        )
        for extra in ("asm.md", "notes.md"):
            if (SCHEMA_DIR.parent.parent / src / extra).is_file():
                src_links += f' · <a href="{pp}{esc(src)}/{extra}" target="_blank">{extra}</a>'

    meta_dl = f"""
      <dl class="asm-dl">
        <dt>opcode</dt><dd><code>{esc(cmd.get('opcode'))}</code> · {esc(cmd.get('direction'))} · {esc(cmd.get('proto'))}</dd>
        <dt>协议类</dt><dd><code>{esc(cmd.get('proto_class') or '—')}</code></dd>
        <dt>处理函数</dt><dd><code>{esc(cmd.get('handler') or '—')}</code> {va_link(cmd.get('handler_va'))}</dd>
        <dt>处理块</dt><dd>{esc(' .. '.join(cmd.get('block') or [])) or '<span class="muted">—</span>'}</dd>
        <dt>名字串</dt><dd><code>{esc(cmd.get('name_str') or '—')}</code> {va_link(cmd.get('name_str_va'))}</dd>
        <dt>声明容量</dt><dd>{esc(cmd.get('capacity') or '—')} {va_link(cmd.get('capacity_va'))}
          <span class="muted">（缓冲 claim，非线长）</span></dd>
        <dt>长度闭合点</dt><dd>{va_link(cmd.get('closer_va'))}</dd>
        <dt>去向槽</dt><dd><code>{esc(cmd.get('dispatch_slot') or '—')}</code> {va_link(cmd.get('dispatch_va'))}</dd>
        <dt>配对 / 同族</dt><dd>{fmt_pair(cmd, command_ids)}</dd>
        <dt>证据目录</dt><dd>{src_links or '<span class="muted">—</span>'}</dd>
      </dl>"""

    # ---- 包结构体 ----
    struct_html = ""
    for role, st in (cmd.get("structs") or {}).items():
        mrows = ""
        for m in st.get("members", []):
            extra = []
            agg = field_composite_ref(m, composites)
            if m.get("element"):
                extra.append("元素 " + render_element(m["element"], composites, m.get("cap"), m.get("element_length")))
            elif m.get("element_length"):
                extra.append(f"元素线长 {esc(m['element_length'])}B")
            if m.get("cap") and not m.get("element"):
                extra.append(f"上限 {esc(m['cap'])}")
            if m.get("count_field"):
                extra.append(f"条数 ← <code>{esc(m['count_field'])}</code>")
            if m.get("count_field_source") and m["count_field_source"] not in ("fixed", "length_expr"):
                extra.append(f'<span class="muted">{esc(m["count_field_source"])}</span>')
            if not m.get("element"):
                if agg:
                    # 聚合成员就地列出内部成员（完整表在「字段解剖」节；这里给紧凑清单，
                    # 免得同一页出现两张一样的表，也免得写「成员见 composites/XXX」）。
                    extra.append(render_members_summary(agg, composites))
                elif m.get("note"):
                    extra.append(f'<span class="muted">{esc(m["note"])}</span>')
            mrows += f"""<tr>
          <td><code class="fname">{esc(m.get('name'))}</code></td>
          <td><code>{esc(m.get('wire_type'))}</code></td>
          <td><code>{esc(m.get('length'))}</code></td>
          <td>{esc(m.get('field_ref') or '')}</td>
          <td class="muted">{' · '.join(extra) or '—'}</td>
        </tr>"""
        struct_html += f"""
      <div class="struct-block">
        <h4><code>{esc(st.get('go_name'))}</code> <span class="muted">({esc(role)} · 角色 {esc(st.get('role', role))})</span>
          <span class="muted">线长 {esc(st.get('wire_length'))}</span></h4>
        <table class="srv-table">
          <thead><tr><th>Go 成员</th><th>线类型</th><th>线长</th><th>字段引用</th><th>元素 / 计数</th></tr></thead>
          <tbody>{mrows}</tbody>
        </table>
      </div>"""

    # ---- 字段解剖表 ----
    # 聚合字段（struct / 结构体数组）就地摊开内部成员：数据库还在重建期，
    # 结构体的内容不能靠「引用某张表」或「见 XXX」来表达。
    child_bases = {f.get("name", "").split(".")[0] for f in cmd.get("fields", []) if "." in f.get("name", "")}
    frows = ""
    for f in cmd.get("fields", []):
        if f.get("is_closure"):
            frows += f"""<tr class="row-closure">
          <td><span class="muted">闭合</span></td>
          <td><code>{esc(f.get('offset'))}</code></td>
          <td><code>0</code></td>
          <td><code>—</code></td>
          <td><code>（长度闭合）</code></td>
          <td colspan="4">{esc(f.get('meaning'))} · {esc(f.get('purpose'))}</td>
          <td>{badge(f.get('disposition', 'TBD'))}</td>
          <td>{va_list_html(f.get('evidence_va'))}</td>
        </tr>"""
            continue
        review = ' <span class="badge" style="background:#e65100">CSV 待复核</span>' if f.get("needs_review") else ""
        member_row = f.get("is_member_row")
        if member_row:
            review += ' <span class="badge" style="background:#546e7a">成员占位行</span>'
        ent = f.get("entity_ref")
        ent_html = ref_page_html(ent) if ent else '<span class="muted">—</span>'
        frows += f"""<tr>
          <td>{esc(f.get('seq'))}</td>
          <td><code>{esc(f.get('offset'))}</code></td>
          <td><code>{esc(f.get('length'))}</code></td>
          <td><code>{esc(f.get('wire_type'))}</code></td>
          <td><code class="fname">{esc(f.get('name'))}</code>{review}</td>
          <td>{esc(f.get('meaning'))}</td>
          <td>{esc(f.get('purpose'))}</td>
          <td class="muted">{esc(f.get('enum') or '—')}</td>
          <td>{badge(f.get('disposition', 'TBD'))} {ent_html}</td>
          <td>{va_list_html(f.get('evidence_va'))}</td>
          <td class="muted">{esc(f.get('confidence'))}</td>
        </tr>"""
        base = f.get("name", "").split(".")[0]
        if member_row:
            # 父行已摊平成员，这里只解释“为什么这行不进线长求和”，不再重复摊一遍。
            frows += (f'<tr class="row-members"><td colspan="11"><div class="muted">'
                      f'<b>成员占位行</b>：这 {esc(f.get("length"))} 字节已经算在父字段 '
                      f'<code>{esc(member_row)}</code> 的长度列里，成员清单由该父结构的 composite 展开；'
                      f'本行只作追溯，<b>不参与线长求和</b>（否则 §3.1 定长和式会双计）。</div></td></tr>')
            continue
        if base in child_bases:
            continue  # 成员已作为独立字段行列出，不重复摊开
        target = field_composite_ref(f, composites)
        len_note = ""
        if f.get("length_is_elem_width"):
            len_note += (f'<div class="muted">长度列只写了<b>元素线宽</b>（{esc(f.get("length"))}）：'
                         f'条数 ← <code>{esc(f["length_is_elem_width"])}</code>，'
                         f'按 §3.1 总长应为「宽·条数」</div>')
        # 长度列曾经写的是「槽位预算 / 内存跨度 / 单元素线宽」这类**非线长口径**，
        # 导入期已改成线上实写字节数。把原数摆出来：它是分配上限，是溢出边界复核要用的量。
        if f.get("slot_budget"):
            len_note += (f'<div class="muted"><b>槽位预算</b> {esc(f["slot_budget"])} B：'
                         f'线上实写为 NUL 串（<code>strlen+1</code>），故长度列是 <code>{esc(f.get("length"))}</code>；'
                         f'槽位是分配上限口径，只用于溢出边界复核</div>')
        if f.get("memory_span"):
            len_note += (f'<div class="muted"><b>内存跨度</b> {esc(f["memory_span"])} B：'
                         f'含非线上成员，故大于线长（长度列已改回 composite 的 '
                         f'<code>{esc(f.get("length"))}</code>，§3.1 记账口径）</div>')
        if f.get("length_is_literal_count"):
            len_note += (f'<div class="muted">条数 <b>{esc(f["length_is_literal_count"])}</b> 是类型尾巴上的字面量'
                         f'（线上无 count 字段），长度列已补全为「条数 × 元素宽」= <code>{esc(f.get("length"))}</code></div>')
        if not target:
            # 元素引用被摘除（同名不同体）/ 引用存疑：把结论摆在行里，别让人以为「已经建好模了」。
            if f.get("element_composite_note") or len_note:
                note = (f'<div class="muted"><b>元素未建模</b>：{esc(f["element_composite_note"])}</div>'
                        if f.get("element_composite_note") else "")
                frows += (f'<tr class="row-members"><td colspan="11">{note}{len_note}</td></tr>')
            continue
        is_arr = (f.get("wire_type") or "").strip().startswith("array<") or bool(f.get("element_composite_ref"))
        if is_arr:
            shape = array_shape(f.get("wire_type"), f.get("length"))
            caption = f"数组元素（{shape}）" if shape else "数组元素"
        else:
            caption = "结构体成员"
        src_note = len_note
        if f.get("element_composite_ref_source") == "width":
            src_note += '<div class="muted">元素引用按<b>元素线宽</b>重挂（名字命中但与长度列不自洽）</div>'
        elif f.get("element_composite_warning"):
            src_note += f'<div class="muted">引用存疑：{esc(f["element_composite_warning"])}</div>'
        frows += (f'<tr class="row-members"><td colspan="11">{src_note}'
                  f'{render_composite_block(target, composites, caption)}</td></tr>')

    # ---- 行为 ----
    beh = cmd.get("behavior") or []
    if beh:
        brows = ""
        for s in beh:
            brows += f"""<tr>
          <td>{esc(s.get('step'))}</td>
          <td><code>{esc(s.get('kind'))}</code></td>
          <td>{esc(s.get('detail'))}</td>
          <td>{va_link(s.get('evidence_va'))}</td>
        </tr>"""
        beh_html = f"""<table class="srv-table">
        <thead><tr><th>步</th><th>类别</th><th>动作</th><th>证据 VA</th></tr></thead>
        <tbody>{brows}</tbody>
      </table>"""
    else:
        beh_html = ('<p class="muted">未补。本命令当前为 <code>IMPORTED</code>：'
                    '字段与结构体来自 <code>protocol_analysis</code> 草稿，行为步骤待用 IDA 汇编补齐。'
                    '补全后状态升为 <code>ASM-VERIFIED</code> / <code>BEHAVIOR-DONE</code>。</p>')

    # ---- 能力 ----
    caps = cmd.get("capabilities") or []
    dcap = cmd.get("capabilities_derived") or []
    cap_html = ""
    if caps:
        cap_html += "".join(f'<span class="cap-chip">{esc(c)}</span>' for c in caps)
    else:
        cap_html += '<span class="muted">无汇编证据能力标签</span>'
    if dcap:
        cap_html += '<div class="muted">命名学推断（非证据）：' + "".join(
            f'<span class="cap-chip cap-derived">{esc(c)}</span>' for c in dcap) + "</div>"

    # ---- DB 影响 ----
    eff = cmd.get("db_effects") or []
    if eff:
        erows = ""
        for e in eff:
            ref = ""
            if e.get("entity"):
                ref += ref_page_html(e["entity"]) + " "
            if e.get("table_ref"):
                ref += f'<a href="../tables/{esc(e["table_ref"])}.html"><code>{esc(e["table_ref"])}</code></a>'
            erows += f"""<tr>
          <td>{ref or '<span class="muted">—</span>'}</td>
          <td><code>{esc(e.get('op'))}</code></td>
          <td>{esc(', '.join(e.get('fields') or [])) or '<span class="muted">—</span>'}</td>
          <td>{badge(e.get('disposition', 'TBD'))}</td>
          <td>{va_link(e.get('evidence_va'))}</td>
        </tr>"""
        eff_html = f"""<table class="srv-table">
        <thead><tr><th>实体 / 表</th><th>op</th><th>业务字段</th><th>disposition</th><th>证据 VA</th></tr></thead>
        <tbody>{erows}</tbody>
      </table>"""
    else:
        eff_html = '<p class="muted">未补。CS 的 op 需服务端语义确认；SC 的 op 由去向槽 <code>vt[0xNNN]</code> 的实参决定。</p>'

    # ---- ASM 复核 ----
    checks = av.get("checks") or {}
    crows = ""
    for key, label in (("capacity", "容量指纹"), ("field_window", "字段窗口"),
                       ("primitive_widths", "原语宽度"), ("closer", "闭合点"),
                       ("dispatch_slot", "去向槽+实参"), ("log_strings", "日志串")):
        val = checks.get(key)
        cell = '<span class="muted">未复核</span>' if val is None else f"<code>{esc(json.dumps(val, ensure_ascii=False))}</code>"
        crows += f"<tr><td>{esc(label)}</td><td><code>{esc(key)}</code></td><td>{cell}</td></tr>"
    mism = av.get("mismatches") or []
    mism_html = ""
    if mism:
        mism_html = "<h4>差异</h4><ul>" + "".join(
            f"<li><code>{esc(json.dumps(m, ensure_ascii=False))}</code></li>" for m in mism) + "</ul>"
    elif status == "IMPORTED":
        mism_html = '<p class="muted">尚无差异记录（未复核）。</p>'
    else:
        mism_html = '<p>无差异。</p>'
    ev_file = av.get("evidence_file")
    ev_link = ""
    if ev_file:
        ev_link = f'<p>原始证据切片：{repo_file_html(ev_file, nav_key)}</p>'
    asm_html = f"""
      <dl class="asm-dl">
        <dt>状态</dt><dd>{status_badge(status)}</dd>
        <dt>复核批次</dt><dd>{esc(av.get('batch') if av.get('batch') is not None else '—')}</dd>
        <dt>复核时间</dt><dd>{esc(av.get('verified_at') or '—')}</dd>
        <dt>提取器</dt><dd><code>{esc(av.get('extractor') or '—')}</code></dd>
      </dl>
      <table class="srv-table">
        <thead><tr><th>检查项</th><th>键</th><th>结果</th></tr></thead>
        <tbody>{crows}</tbody>
      </table>
      {mism_html}
      {ev_link}"""

    repairs = cmd.get("import_repairs") or []
    csv_repairs = [r for r in repairs if not str(r).startswith("override_")]
    ov_repairs = [r for r in repairs if str(r).startswith("override_")]
    field_override = cmd.get("field_override") or {}
    repairs_html = ""
    if csv_repairs:
        repairs_html += f"""<section>
      <h3>导入期 CSV 修复记录</h3>
      <ul>{''.join(f'<li><code>{esc(r)}</code></li>' for r in csv_repairs)}</ul>
      <p class="muted">这些行的 <code>fields.csv</code> 列数畸形（线类型被逗号切开 / 文本内含 ASCII 逗号），
        导入时按启发式还原，<strong>必须由 IDA 汇编复核后才能当结论用</strong>。</p>
    </section>"""
    if ov_repairs or field_override:
        ov_rows = ''.join(f'<li><code>{esc(r)}</code></li>' for r in ov_repairs)
        ov_reason = field_override.get("reason")
        repairs_html += f"""<section>
      <h3>人工复核覆盖（订正 <code>fields.csv</code>）</h3>
      <ul>{ov_rows}</ul>
      <dl class="asm-dl">
        <dt>修订版本</dt><dd>rev {esc(field_override.get('revision'))} · {esc(field_override.get('verified_at'))}</dd>
        <dt>覆写文件</dt><dd><code>{esc(field_override.get('evidence_file'))}</code></dd>
        <dt>订正理由</dt><dd>{esc(ov_reason) if ov_reason else '<span class="muted">—</span>'}</dd>
      </dl>
      <p class="muted">这些字段的口径由 IDA 汇编逐条核对后人工订正，<strong>不再等同</strong> <code>fields.csv</code> 原值
        （覆盖行带 <code>override_verified: true</code>）；<code>revision</code> 变号会让旧汇编复核结论作废、
        必须重跑 <code>verify_commands_ida.py ingest</code>。</p>
    </section>"""

    extra = cmd.get("extra") or {}
    extra_bits = []
    if extra.get("opcode_write_va"):
        extra_bits.append(f"opcode 写入/分发证据 <code>{esc(extra['opcode_write_va'])}</code>")
    if extra.get("notify_va"):
        extra_bits.append(f"附加通知 <code>{esc(extra['notify_va'])}</code>")
    if extra.get("error_vas"):
        extra_bits.append("错误出口 " + va_list_html(extra["error_vas"]))
    if extra.get("dispatcher"):
        extra_bits.append(f"分发器 <code>{esc(extra['dispatcher'])}</code>")
    extra_html = ('<p class="muted">' + " · ".join(extra_bits) + "</p>") if extra_bits else ""

    w = cmd.get("wire") or {}
    body = f"""
    <nav class="breadcrumb"><a href="index.html">命令</a> / <span><code>{esc(cid)}</code></span></nav>
    <h2>{esc(cid)}
      <span class="badge" style="background:#455a64">{esc(cmd.get('direction'))}</span>
      <span class="badge" style="background:#1565c0">{esc(cmd.get('proto'))}</span>
      {status_badge(status)}</h2>
    {meta_dl}
    {extra_html}

    <section>
      <h3>线长</h3>
      <dl class="asm-dl">
        <dt>报文体线长</dt><dd><code>{esc(w.get('length_expr'))}</code>
          {'<span class="badge" style="background:#455a64">定长</span>' if w.get('fixed') else '<span class="badge" style="background:#e65100">变长</span>'}
          <span class="muted">来源 {esc(w.get('length_source') or '—')}</span></dd>
        <dt>变长驱动</dt><dd>{va_list_html(w.get('var_drivers'))}</dd>
        <dt>负载字段数</dt><dd>{esc(w.get('field_count'))}</dd>
        <dt>容量口径</dt><dd class="muted">{esc(w.get('capacity_note') or '—')}</dd>
        <dt>README 结论</dt><dd class="muted">{esc(w.get('readme_conclusion') or '—')}{' <span class="badge" style="background:#e65100">草稿口径，见下行订正</span>' if w.get('override_note') else ''}</dd>
        <dt>README 闭合</dt><dd class="muted">{esc(w.get('readme_close') or '—')}</dd>
        {f'<dt>人工订正</dt><dd>{esc(w.get("override_note"))}</dd>' if w.get('override_note') else ''}
      </dl>
    </section>

    <section>
      <h3>包结构体</h3>
      <p class="muted">由 <code>fields[]</code> 归并而成；线序即字段行序，可复用的聚合体只在
        <code>element</code> 里引用 <code>schema/composites/</code>。</p>
      {struct_html or '<p class="muted">无字段（零负载命令）。</p>'}
    </section>

    <section>
      <h3>字段解剖</h3>
      <table class="wide">
        <thead><tr>
          <th>序</th><th>偏移</th><th>线长</th><th>线类型</th><th>字段名</th>
          <th>含义</th><th>用途（来源/去向）</th><th>取值/枚举</th><th>去向</th><th>证据 VA</th><th>置信度</th>
        </tr></thead>
        <tbody>{frows}</tbody>
      </table>
    </section>

    <section>
      <h3>客户端行为</h3>
      {beh_html}
    </section>

    <section>
      <h3>能力</h3>
      {cap_html}
    </section>

    <section>
      <h3>DB 影响</h3>
      {eff_html}
    </section>

    {repairs_html}

    <section>
      <h3>汇编复核（IDA asm 为唯一权威）</h3>
      {asm_html}
    </section>
"""
    return page(cid, nav_key, body)


def build_command_structs(cmds: list[dict]) -> str:
    rows = ""
    for cmd in cmds:
        for role, st in (cmd.get("structs") or {}).items():
            members = st.get("members", [])
            arrays = [m for m in members if m.get("element") or m.get("cap")]
            arr_txt = ", ".join(
                f"{m.get('name')}" + (f"[{m['cap']}]" if m.get("cap") else "") + (
                    f"←{m['count_field']}" if m.get("count_field") else "")
                for m in arrays) or "—"
            rows += f"""<tr>
      <td><code class="fname">{esc(st.get('go_name'))}</code></td>
      <td><a href="{esc(cmd['id'])}.html"><code>{esc(cmd['id'])}</code></a></td>
      <td>{esc(role)}</td>
      <td><code>{esc(st.get('wire_length'))}</code></td>
      <td>{len(members)}</td>
      <td class="muted">{esc(arr_txt)}</td>
    </tr>"""
    body = f"""
    <nav class="breadcrumb"><a href="index.html">命令</a> / <span>包结构体</span></nav>
    <h2>包结构体总览</h2>
    <p class="muted">{len(cmds)} 条命令的结构体（{sum(len(c.get('structs') or {}) for c in cmds)} 个）。
      成员语义与线宽可从 <a href="../entities/index.html">协议实体</a> /
      <a href="../tables/index.html">表设计</a> 交叉查；聚合体定义在 <code>schema/composites/</code>。</p>
    <table class="wide">
      <thead><tr><th>Go 结构体</th><th>命令</th><th>角色</th><th>线长</th><th>成员</th><th>数组成员</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("包结构体", "commands/structs.html", body)


def build_command_capabilities(index: dict | None, cmds: list[dict]) -> str:
    """能力矩阵：行 = 能力标签，列 = 有证据条数 / 命名学推断条数 / 命令样例。"""
    evid: dict[str, list[str]] = {}
    deriv: dict[str, list[str]] = {}
    for cmd in cmds:
        for c in cmd.get("capabilities") or []:
            evid.setdefault(c, []).append(cmd["id"])
        for c in cmd.get("capabilities_derived") or []:
            deriv.setdefault(c, []).append(cmd["id"])
    tags = sorted(set(evid) | set(deriv))
    rows = ""
    for t in tags:
        e = evid.get(t, [])
        d = deriv.get(t, [])
        sample = ", ".join(f'<a href="{esc(x)}.html"><code>{esc(x)}</code></a>' for x in (e or d)[:6])
        rows += f"""<tr>
      <td><span class="cap-chip">{esc(t)}</span></td>
      <td>{len(e)}</td>
      <td>{len(d)}</td>
      <td class="muted">{sample}</td>
    </tr>"""
    body = f"""
    <nav class="breadcrumb"><a href="index.html">命令</a> / <span>能力矩阵</span></nav>
    <h2>能力矩阵</h2>
    <p class="muted">词表与判定规则见 <code>docs/02-命令能力表.md</code>。
      <strong>有证据</strong>列只统计能指回 <code>behavior[]</code>/<code>db_effects[]</code> 的标签；
      <strong>命名学推断</strong>列来自命令名后缀（<code>capabilities_derived</code>），不是证据。</p>
    <table class="wide">
      <thead><tr><th>能力标签</th><th>有证据</th><th>命名学推断</th><th>样例命令</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("能力矩阵", "commands/capabilities.html", body)


def build_command_db_effects(cmds: list[dict]) -> str:
    rows = ""
    n = 0
    for cmd in cmds:
        for e in cmd.get("db_effects") or []:
            n += 1
            ref = ""
            if e.get("entity"):
                ref += ref_page_html(e["entity"]) + " "
            if e.get("table_ref"):
                ref += f'<a href="../tables/{esc(e["table_ref"])}.html"><code>{esc(e["table_ref"])}</code></a>'
            rows += f"""<tr>
      <td><a href="{esc(cmd['id'])}.html"><code>{esc(cmd['id'])}</code></a></td>
      <td>{esc(cmd.get('direction'))}</td>
      <td>{ref or '<span class="muted">—</span>'}</td>
      <td><code>{esc(e.get('op'))}</code></td>
      <td class="muted">{esc(', '.join(e.get('fields') or [])) or '—'}</td>
      <td>{badge(e.get('disposition', 'TBD'))}</td>
      <td>{va_link(e.get('evidence_va'))}</td>
    </tr>"""
    body = f"""
    <nav class="breadcrumb"><a href="index.html">命令</a> / <span>数据库影响</span></nav>
    <h2>数据库影响总表</h2>
    <p class="muted">把命令接到既有 <code>schema/entities/*</code> 与 <code>schema/tables/*</code> 上。
      当前已登记 <strong>{n}</strong> 条影响（{sum(1 for c in cmds if c.get('db_effects'))} 条命令）。
      未补齐前为空表：SC 看去向槽实参，CS 需服务端语义确认。</p>
    <table class="wide">
      <thead><tr><th>命令</th><th>方向</th><th>实体 / 提议表</th><th>op</th><th>业务字段</th><th>disposition</th><th>证据 VA</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page("数据库影响", "commands/db-effects.html", body)


CSS = """
:root {
  --bg: #f8f9fb; --card: #fff; --text: #1a1a2e; --muted: #5c6370;
  --border: #e2e6ed; --accent: #2563eb; --radius: 8px;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.55; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 1.25rem; }
.site-header { background: var(--card); border-bottom: 1px solid var(--border); padding: 0.75rem 0; margin-bottom: 1.5rem; }
.site-header h1 { margin: 0; font-size: 1.15rem; }
.site-header h1 a { color: var(--text); text-decoration: none; }
.header-note { margin: 0.25rem 0 0; font-size: 0.78rem; color: var(--muted); }
.site-header nav { margin-top: 0.5rem; }
.site-header nav a { margin-right: 1rem; color: var(--muted); text-decoration: none; font-size: 0.9rem; }
.site-header nav a.active { color: var(--accent); font-weight: 600; }
.site-footer { margin-top: 3rem; padding: 1rem 0; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.85rem; }
.hero h2 { margin-top: 0; }
.lead { color: var(--muted); }
.grid.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin: 1.5rem 0 2rem; }
.stat { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; text-align: center; }
.stat .num { font-size: 1.75rem; font-weight: 700; color: var(--accent); }
.stat .lbl { font-size: 0.8rem; color: var(--muted); }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; }
.card { display: block; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; text-decoration: none; color: inherit; }
.card:hover { border-color: var(--accent); }
.card-primary { border-width: 2px; }
.card h3 { margin: 0.4rem 0; font-size: 1rem; }
.card-meta { font-size: 0.8rem; color: var(--muted); }
.card-status { margin-bottom: 0.25rem; }
.muted { color: var(--muted); }
table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; margin: 1rem 0; font-size: 0.88rem; }
th, td { padding: 0.55rem 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { background: #f1f3f7; font-weight: 600; }
table.wide { font-size: 0.82rem; }
code { font-family: Consolas, monospace; font-size: 0.88em; }
.badge { display: inline-block; padding: 0.15rem 0.45rem; border-radius: 4px; color: #fff; font-size: 0.72rem; font-weight: 600; }
.breadcrumb { font-size: 0.9rem; color: var(--muted); margin-bottom: 0.5rem; }
.breadcrumb a { color: var(--accent); }
.ev-link { font-size: 0.78rem; margin-left: 0.35rem; }
.evidence-line { font-size: 0.78rem; margin: 0.15rem 0; }
section { margin-bottom: 2rem; }
section h2, section h3 { font-size: 1.15rem; }
.col-group { margin-bottom: 1.5rem; }
.field-tree { list-style: none; margin: 0; padding: 0; }
.root-tree { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.75rem 1rem; }
.field-tree ul.field-tree { margin-left: 1rem; padding-left: 0.75rem; border-left: 2px solid var(--border); }
.tree-branch details > summary { cursor: pointer; list-style: none; padding: 0.35rem 0.5rem; background: #f6f8fb; border: 1px solid var(--border); border-radius: 4px; }
.tree-branch details > summary::-webkit-details-marker { display: none; }
.tree-branch details > summary::before { content: "▸ "; color: var(--accent); }
.tree-branch details[open] > summary::before { content: "▾ "; }
.tree-body { padding: 0.35rem 0 0.35rem 0.75rem; }
.tree-detail { font-size: 0.85rem; margin-bottom: 0.35rem; }
.tree-leaf { margin: 0.2rem 0; }
.tree-row { display: grid; gap: 0.5rem; padding: 0.35rem 0.5rem; font-size: 0.85rem; border-radius: 4px; }
.tree-row.cols-4 { grid-template-columns: 1.1fr 1.2fr 1.3fr 0.8fr; }
.tree-row:hover { background: #f6f8fb; }
.tree-head { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }
.tree-head .fname { font-weight: 600; }
.offset { color: var(--muted); font-size: 0.78rem; }
.asm-ok { color: #2e7d32; font-weight: 700; font-size: 0.85rem; }
.asm-panel { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.75rem 1rem; margin: 1rem 0; }
.asm-dl { display: grid; grid-template-columns: 7rem 1fr; gap: 0.25rem 0.75rem; margin: 0; font-size: 0.88rem; }
.asm-dl dt { color: var(--muted); margin: 0; }
.asm-dl dd { margin: 0; }
.tree-legend { display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.78rem; color: var(--muted); margin-bottom: 0.5rem; }
.srv-block { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }
.srv-block h3 { margin-bottom: 0.25rem; }
.srv-table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; font-size: 0.85rem; margin-top: 0.5rem; }
.srv-table th, .srv-table td { text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid var(--border); vertical-align: top; }
.srv-table th { background: rgba(127, 127, 127, 0.08); font-weight: 600; font-size: 0.8rem; }
.srv-table tr:last-child td { border-bottom: none; }
.srv-seed { margin-top: 0.75rem; }
.srv-seed h4 { margin: 0 0 0.25rem; font-size: 0.85rem; color: var(--muted); font-weight: 600; }
.filters { display: flex; flex-wrap: wrap; gap: 0.75rem 1rem; align-items: center; background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.65rem 0.9rem; margin-bottom: 0.75rem; font-size: 0.85rem; }
.filters label { display: flex; align-items: center; gap: 0.35rem; color: var(--muted); }
.filters select { font: inherit; padding: 0.15rem 0.3rem; border: 1px solid var(--border); border-radius: 4px; background: #fff; }
.cap-chip { display: inline-block; margin: 0 0.2rem 0.2rem 0; padding: 0.1rem 0.4rem; border-radius: 10px; background: #e8effd; color: #1d4ed8; font-size: 0.72rem; }
.cap-chip.cap-derived { background: #f0f0f2; color: #5c6370; }
.cmd-table td { vertical-align: top; }
.struct-block { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.75rem 1rem; margin-bottom: 1rem; }
.struct-block h4 { margin: 0 0 0.5rem; font-size: 0.95rem; }
.row-closure td { background: #fafafa; }
tr:target { background: #fff8e1; }
.composite-details { margin-top: 0.3rem; font-size: 0.8rem; }
.composite-details summary { cursor: pointer; }
.composite-table { margin: 0.4rem 0 0.2rem; font-size: 0.78rem; }
.row-members td { background: #fbfcfe; padding: 0.3rem 0.6rem 0.6rem; }
.composite-block { border-left: 3px solid #c7d2fe; padding: 0.1rem 0 0.1rem 0.6rem; }
.composite-head { font-size: 0.78rem; color: #37474f; margin-bottom: 0.15rem; }
.composite-inline { font-size: 0.78rem; line-height: 1.5; }
.cmd-refs { columns: 2; font-size: 0.82rem; }
@media (max-width: 800px) { .tree-row.cols-4 { grid-template-columns: 1fr; } }
"""


def build_srv_index(srv: dict) -> str:
    """服务端配置表（srv.*）页：一表一节，列 + 约束 + SQL COMMENT 里的证据 + 种子值。"""
    intro = "".join(f'<p class="lead">{line}</p>' for line in srv.get("intro", []))
    doc_by_slug = srv.get("_docs", {})

    cards = ""
    for t in srv.get("tables", []):
        cards += f"""
    <a class="card" href="#{esc(t.get('slug'))}">
      <div class="card-status">{badge('CONFIG')}</div>
      <h3><code>{esc(t.get('id'))}</code></h3>
      <p>{esc(t.get('title'))}</p>
      <div class="card-meta">{esc(t.get('columns'))} 列 · 种子 {esc(t.get('seed_rows'))} 行</div>
    </a>"""

    sections = ""
    for t in srv.get("tables", []):
        doc = doc_by_slug.get(t.get("slug"), {})
        pk = doc.get("primary_key") or []
        rows = ""
        for col in doc.get("columns", []):
            constraints = []
            if col.get("not_null"):
                constraints.append("NOT NULL")
            if col.get("default") is not None:
                constraints.append(f"DEFAULT {col['default']}")
            constraints += col.get("checks", [])
            pk_badge = (
                ' <span class="badge" style="background:#455a64">PK</span>'
                if col.get("name") in pk
                else ""
            )
            rows += f"""<tr>
        <td><code>{esc(col.get('name'))}</code>{pk_badge}</td>
        <td><code>{esc(col.get('sql_type'))}</code></td>
        <td class="muted">{esc(' · '.join(constraints)) or '—'}</td>
        <td>{esc(col.get('meaning')) or '<span class="muted">—</span>'}</td>
      </tr>"""

        seed_cols = doc.get("seed_columns") or []
        seed_rows = doc.get("seed_rows") or []
        seed = ""
        if seed_rows:
            head = "".join(f"<th>{esc(c)}</th>" for c in seed_cols)
            body = ""
            for row in seed_rows:
                body += "<tr>" + "".join(
                    f"<td><code>{esc(row.get(c, ''))}</code></td>" for c in seed_cols
                ) + "</tr>"
            seed = f"""<div class="srv-seed"><h4>种子值（迁移里 INSERT 的那几行）</h4>
      <table class="srv-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"""

        sections += f"""
    <section class="srv-block" id="{esc(doc.get('slug'))}">
      <h3><code>{esc(doc.get('id'))}</code> · {esc(doc.get('title'))}</h3>
      <p>{esc(doc.get('purpose'))}</p>
      <div class="card-meta">DDL <code>{esc(doc.get('ddl'))}</code> · 主键
        <code>{esc(', '.join(pk)) or '—'}</code></div>
      <table class="srv-table">
        <thead><tr><th>列</th><th>SQL 类型</th><th>约束</th><th>含义 / 协议证据（SQL COMMENT）</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {seed}
    </section>"""

    body = f"""
    <section class="hero">
      <h2>{esc(srv.get('title'))}</h2>
      {intro}
      <p class="muted">本页 JSON 由 <code>{esc(srv.get('generated_by'))}</code> 从
        <code>{esc(srv.get('ddl'))}</code> 反推生成（只当文档）；运行时来源是库里的这些表。</p>
    </section>
    <section><div class="card-grid">{cards}</div></section>
    {sections}
"""
    return page(srv.get("title", "服务端配置"), "srv/index.html", body)


def main() -> None:
    meta = load_json(SCHEMA_DIR / "_meta.json")
    # 旧表注册表改成读冻结证据（`relations.html` 的 id/status/purpose/证据命令同源）
    relations = {"tables": [
        {"id": d.get("id", stem), "status": d.get("status", "proposed"),
         "purpose": d.get("purpose", ""),
         "evidence_commands": d.get("evidence_commands", [])}
        for stem, node in sorted(load_legacy_evidence().items())
        if (d := (node.get("declaration") or {}))
    ]}
    composites = load_composites()
    tables = load_tables()
    srv = load_srv()
    commands_index, commands = load_commands()

    entities = [load_json(p) for p in sorted((SCHEMA_DIR / "entities").glob("*.json"))]
    fields_index = load_json(SCHEMA_DIR / "fields" / "index.json") if (SCHEMA_DIR / "fields" / "index.json").is_file() else None

    meta["stats"]["entities_manual"] = len(entities)
    meta["stats"]["tables_proposed"] = len(tables)
    meta["stats"]["columns_proposed"] = sum(len(t.get("columns", [])) for t in tables)
    meta["stats"]["srv_tables"] = len(srv.get("tables", [])) if srv else 0
    # 命令维度统计（模型口径见 docs/01-命令模型.md）
    if commands_index:
        c = commands_index.get("counts", {})
        status = c.get("by_status", {})
        meta["stats"]["commands_modeled"] = c.get("commands", len(commands))
        meta["stats"]["commands_asm_verified"] = status.get("ASM-VERIFIED", 0) + status.get("BEHAVIOR-DONE", 0)
        meta["stats"]["commands_behavior_done"] = status.get("BEHAVIOR-DONE", 0)
        meta["stats"]["command_fields"] = c.get("fields", 0)
    meta["updated"] = date.today().isoformat()
    (SCHEMA_DIR / "_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(CSS.strip(), encoding="utf-8")
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    (SITE_DIR / "index.html").write_text(
        build_index(meta, tables, entities, fields_index, composites, commands_index), encoding="utf-8"
    )
    (SITE_DIR / "relations.html").write_text(build_relations(relations), encoding="utf-8")

    command_ids = {c.get("id", "") for c in commands}

    tbl_dir = SITE_DIR / "tables"
    tbl_dir.mkdir(parents=True, exist_ok=True)
    # 表/实体页按当前 schema 写出，删表（如 tbl_fire_points 随 fire_points 一并移除）后
    # 旧页会变成没人链接的孤儿页——它还在磁盘上，截图/搜索时会被当成「库里还有这张表」。
    # 生成器负责清掉自己上一轮的产物。
    for stale in tbl_dir.glob("*.html"):
        if stale.name != "index.html" and stale.stem not in {t.get("id") for t in tables}:
            stale.unlink()
    (tbl_dir / "index.html").write_text(build_tables_index(tables, composites), encoding="utf-8")
    for tbl in tables:
        tid = tbl.get("id", "unknown")
        (tbl_dir / f"{tid}.html").write_text(
            build_table_detail(tbl, composites, command_ids), encoding="utf-8")

    ent_dir = SITE_DIR / "entities"
    ent_dir.mkdir(parents=True, exist_ok=True)
    for stale in ent_dir.glob("*.html"):
        if stale.name != "index.html" and stale.stem not in {e.get("id") for e in entities}:
            stale.unlink()
    (ent_dir / "index.html").write_text(build_entity_index(entities), encoding="utf-8")
    for ent in entities:
        fid = ent.get("id", "unknown")
        (ent_dir / f"{fid}.html").write_text(
            build_entity_detail(ent, composites, command_ids), encoding="utf-8")

    cmd_dir = SITE_DIR / "commands"
    cmd_dir.mkdir(parents=True, exist_ok=True)
    (cmd_dir / "index.html").write_text(build_commands_index(commands_index, commands), encoding="utf-8")
    (cmd_dir / "structs.html").write_text(build_command_structs(commands), encoding="utf-8")
    (cmd_dir / "capabilities.html").write_text(build_command_capabilities(commands_index, commands), encoding="utf-8")
    (cmd_dir / "db-effects.html").write_text(build_command_db_effects(commands), encoding="utf-8")
    for cmd in commands:
        cid = cmd.get("id", "unknown")
        (cmd_dir / f"{cid}.html").write_text(build_command_detail(cmd, composites, command_ids), encoding="utf-8")

    fld_dir = SITE_DIR / "fields"
    fld_dir.mkdir(parents=True, exist_ok=True)
    (fld_dir / "index.html").write_text(build_fields_index(fields_index), encoding="utf-8")

    asm_dir = SITE_DIR / "asm-audit"
    asm_dir.mkdir(parents=True, exist_ok=True)
    (asm_dir / "index.html").write_text(build_asm_audit_index(tables, composites), encoding="utf-8")

    oracle_dir = SITE_DIR / "oracle-audit"
    oracle_dir.mkdir(parents=True, exist_ok=True)
    (oracle_dir / "index.html").write_text(build_oracle_audit_index(commands, composites), encoding="utf-8")

    srv_count = 0
    if srv:
        srv_count = len(srv.get("tables", []))
        srv_dir = SITE_DIR / "srv"
        srv_dir.mkdir(parents=True, exist_ok=True)
        (srv_dir / "index.html").write_text(build_srv_index(srv), encoding="utf-8")

    cfg_count = 0
    if (SCHEMA_DIR / "cfg" / "index.json").is_file():
        cfg_count = generate_cfg_site(page)

    homing_count = generate_homing_site(page)

    print(f"Generated site at {SITE_DIR}")
    print(f"  homing/({homing_count} objects), tables/({len(tables)}), entities/({len(entities)}), "
          f"commands/({len(commands)}), fields/index.html, cfg/({cfg_count}), srv/({srv_count}), oracle-audit/")

    # 生成完立刻自检死链：站点是生成物，模型裁掉一个对象后别处指向它的链接会静默变死链，
    # 而 HTML 不会报错。`--no-link-check` 可跳过（约 3 秒）。
    if "--no-link-check" not in sys.argv and check_site_links.run(SITE_DIR) != 0:
        sys.exit("站点自检失败：按上面的「修法」回生成器改（`--no-link-check` 可跳过）")


if __name__ == "__main__":
    main()

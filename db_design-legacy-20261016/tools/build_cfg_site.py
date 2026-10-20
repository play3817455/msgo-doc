"""Generate db_design/site/cfg/* from schema/cfg/*.json"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from cfg_enum_registry import anchor_id, build_registry, conv_slug

SCHEMA_CFG = Path(__file__).resolve().parents[1] / "schema" / "cfg"
SITE_CFG = Path(__file__).resolve().parents[1] / "site" / "cfg"
SITE_ENUMS = SITE_CFG / "enums"

CFG_STATUS_COLORS = {
    "confirmed": "#2e7d32",
    "partial": "#1565c0",
    "pending": "#757575",
    "gap": "#e65100",
}

CFG_STATUS_ZH = {
    "confirmed": "确证",
    "partial": "已映射",
    "pending": "待定",
    "gap": "间隙",
}

CFG_DISP_COLORS = {
    "DOWNLOAD": "#1565c0",
    "LOCAL": "#6a1b9a",
    "SCRIPT": "#455a64",
}

CONVERTER_KIND_ZH = {
    "enum": "字符串枚举",
    "string_copy": "窄串拷贝",
    "string_equal": "字符串比较",
    "int_parse": "整型解析",
    "float_parse": "浮点解析",
    "table_lookup": "表键查表",
    "banner_row_lookup": "行索引查资源",
}

CONVERTER_KIND_COLORS = {
    "enum": "#2e7d32",
    "string_copy": "#455a64",
    "string_equal": "#546e7a",
    "int_parse": "#6a1b9a",
    "float_parse": "#1565c0",
    "table_lookup": "#e65100",
    "banner_row_lookup": "#757575",
}

# 同一函数多种 CSV 语义，禁止在表详情页展开全量 registry 取值
MULTI_CONTEXT_CONVERTERS = {
    "sub_40CE20",
    "sub_402310",
    "sub_47A920",
    "sub_CC6CA8",
    "sub_CC7056",
    "sub_BBB4F0",
    "sub_5812E0",
}

ENUM_CHIP_INLINE_MAX = 12


def esc(s) -> str:
    return html.escape("" if s is None else str(s))


def cfg_badge(kind: str, label: str) -> str:
    color = CFG_STATUS_COLORS.get(kind) or CFG_DISP_COLORS.get(kind, "#757575")
    return f'<span class="badge" style="background:{color}">{esc(label)}</span>'


def status_badge(status: str) -> str:
    st = status or "pending"
    return cfg_badge(st, CFG_STATUS_ZH.get(st, st))


def fmt_offset(c: dict) -> str:
    parts = []
    if c.get("csv_index") is not None:
        parts.append(f"csv {c['csv_index']}")
    if c.get("memory_offset") is not None:
        parts.append(f"+{c['memory_offset']}")
    if c.get("asm_va"):
        parts.append(str(c["asm_va"]))
    return " · ".join(parts) if parts else "—"


def _enum_label(conv: str, name: str, registry: dict) -> str:
    entry = registry.get(conv, {})
    for v in entry.get("values_list") or []:
        if v.get("name") == name:
            return v.get("label_zh") or name
    return name


def fmt_enum_block(c: dict, registry: dict) -> str:
    conv = c.get("enum_converter", "")
    vals = c.get("enum_values") or []
    entry = registry.get(conv, {}) if conv else {}
    if not vals and conv and conv not in MULTI_CONTEXT_CONVERTERS:
        if entry.get("kind", "enum") == "enum":
            vals = [
                {"name": v.get("name"), "value": v.get("value")}
                for v in (entry.get("values_list") or [])
            ]
    if not vals and not conv:
        return ""
    slug = conv_slug(conv) if conv else ""
    chips = []
    show_vals = vals[:ENUM_CHIP_INLINE_MAX]
    for ev in show_vals:
        name = ev.get("name", "")
        val = ev.get("value", "")
        zh = _enum_label(conv, name, registry) if conv else name
        if conv:
            href = f"enums/{slug}.html#{anchor_id(name)}"
            chips.append(
                f'<a class="enum-chip" href="{esc(href)}" title="{esc(zh)}">'
                f"<code>{esc(name)}</code>={esc(val)}"
                f'<span class="enum-zh">{esc(zh)}</span></a>'
            )
        else:
            chips.append(
                f'<span class="enum-chip enum-chip-static">'
                f"<code>{esc(name)}</code>={esc(val)}</span>"
            )
    link = ""
    if conv:
        title = entry.get("title_zh") or conv
        more = ""
        if len(vals) > len(show_vals):
            more = f' <span class="muted">…共 {len(vals)} 项</span>'
        link = (
            f' <a class="enum-conv-link" href="enums/{esc(slug)}.html" '
            f'title="{esc(title)}">↗ {esc(conv)}</a>{more}'
        )
    inner = " ".join(chips) if chips else ""
    return f'<div class="enum-vals">{inner}{link}</div>'


def fmt_meaning_cell(c: dict, registry: dict) -> str:
    meaning = re.sub(r"\*+", "", c.get("meaning") or "").strip()
    meaning = re.sub(r"（待定）|\(待定\)", "", meaning).strip()
    enum_html = fmt_enum_block(c, registry)
    if enum_html:
        return f"{esc(meaning)}{enum_html}"
    return esc(meaning)


def load_cfg_tables() -> tuple[dict, list[dict]]:
    index = json.loads((SCHEMA_CFG / "index.json").read_text(encoding="utf-8"))
    tables = []
    for p in sorted((SCHEMA_CFG / "tables").glob("*.json")):
        tables.append(json.loads(p.read_text(encoding="utf-8")))
    return index, tables


def build_cfg_index_page(index: dict, tables: list[dict], page_fn) -> str:
    rows = ""
    for t in sorted(index.get("tables", []), key=lambda x: x["id"]):
        tid = t["id"]
        asm = t.get("asm_status", "partial")
        partial_n = 0
        gap_n = t.get("column_gap", 0)
        tbl_path = SCHEMA_CFG / "tables" / f"{tid}.json"
        if tbl_path.is_file():
            td = json.loads(tbl_path.read_text(encoding="utf-8"))
            partial_n = td.get("column_partial", 0)
            gap_n = td.get("column_gap", gap_n)
        rows += f"""
    <tr>
      <td><a href="{esc(tid)}.html"><code>{esc(tid)}</code></a></td>
      <td>{status_badge('confirmed' if asm == 'complete' else 'partial') if asm == 'complete' else cfg_badge('partial', asm)}</td>
      <td>{cfg_badge(t.get('disposition', 'DOWNLOAD'), t.get('disposition', ''))}</td>
      <td><code>{esc(t.get('csv_path', ''))}</code></td>
      <td>{t.get('column_count', 0)}</td>
      <td>{t.get('column_confirmed', 0)}</td>
      <td>{partial_n}</td>
      <td>{gap_n}</td>
      <td><code>{esc(t.get('reader_func', ''))}</code></td>
      <td><a href="../../../{esc(t.get('source_md', ''))}" target="_blank">MD</a></td>
    </tr>"""

    body = f"""
    <section class="hero">
      <h2>配置表 79 张 · ASM 列定案</h2>
      <p class="lead">IDA 反编译逐列读取函数 · 订案字段名写入 <code>db_column</code> · 证据 <code>datatables/01-列注释/</code> · <a href="enums/index.html">配置枚举</a></p>
    </section>
    <section class="grid stats">
      <div class="stat"><div class="num">{index.get('total', 79)}</div><div class="lbl">总表数</div></div>
      <div class="stat"><div class="num">{index.get('asm_complete', 0)}</div><div class="lbl">ASM 完成</div></div>
      <div class="stat"><div class="num">{index.get('column_confirmed_total', 0)}</div><div class="lbl">确证列</div></div>
      <div class="stat"><div class="num">{index.get('column_partial_total', 0)}</div><div class="lbl">已映射列</div></div>
    </section>
    <section>
      <h3>状态说明</h3>
      <ul>
        <li><strong>确证</strong> — 枚举/字符串/主键，语义 + ASM 双确证</li>
        <li><strong>已映射</strong> — 类型 + CSV列 + 内存偏移 + asm_va 已确认；语义可能仍为 unknown_*</li>
        <li><strong>间隙</strong> — CSV 有列位但读表函数未读（默认 0）</li>
      </ul>
    </section>
    <table class="wide">
      <thead>
        <tr>
          <th>表</th><th>ASM</th><th>类型</th><th>CSV 路径</th><th>列数</th>
          <th>确证</th><th>已映射</th><th>间隙</th><th>读表函数</th><th>证据</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page_fn("配置表79", "cfg/index.html", body)


def build_cfg_detail_page(tbl: dict, page_fn, registry: dict) -> str:
    tid = tbl["id"]
    col_rows = ""
    for c in tbl.get("columns", []):
        col_rows += f"""
    <tr>
      <td><code>{esc(c.get('csv_index'))}</code></td>
      <td><code>{esc(c.get('db_column'))}</code></td>
      <td><code>{esc(c.get('name'))}</code></td>
      <td>{esc(c.get('display_name', ''))}</td>
      <td><code>{esc(c.get('type'))}</code></td>
      <td>{status_badge(c.get('status', 'pending'))}</td>
      <td><code>{esc(c.get('asm_reader', tbl.get('asm_reader', '')))}</code></td>
      <td class="muted">{esc(fmt_offset(c))}</td>
      <td class="meaning-cell">{fmt_meaning_cell(c, registry)}</td>
    </tr>"""

    partial_n = tbl.get("column_partial", 0)
    gap_n = tbl.get("column_gap", 0)
    asm_st = tbl.get("asm_status", "partial")
    body = f"""
    <p class="breadcrumb"><a href="index.html">配置表79</a> / <code>{esc(tid)}</code></p>
    <h2><code>{esc(tid)}</code> {cfg_badge(tbl.get('disposition', ''), tbl.get('disposition', ''))} {status_badge('confirmed' if asm_st == 'complete' else 'partial')}</h2>
    <dl class="asm-dl">
      <dt>CSV</dt><dd><code>{esc(tbl.get('csv_path'))}</code></dd>
      <dt>用途</dt><dd>{esc(tbl.get('purpose', ''))}</dd>
      <dt>读表函数</dt><dd><code>{esc(tbl.get('asm_reader', '—'))}</code></dd>
      <dt>表ID</dt><dd>{esc(tbl.get('table_id', '—'))}</dd>
      <dt>下载序</dt><dd>{esc(tbl.get('download_order', '—'))}</dd>
      <dt>类名</dt><dd><code>{esc(tbl.get('class_name', '—'))}</code></dd>
      <dt>列统计</dt><dd>{tbl.get('column_count', 0)} 列 · 确证 {tbl.get('column_confirmed', 0)} · 已映射 {partial_n} · 间隙 {gap_n}</dd>
      <dt>证据</dt><dd><a href="../../../{esc(tbl.get('source_md', ''))}" target="_blank">{esc(tbl.get('source_md', ''))}</a></dd>
    </dl>
    <section>
      <h3>列定案</h3>
      <p class="muted"><code>db_column</code> = PostgreSQL 列名（确证/有语义的 partial 用订案名；<code>unknown_*</code> 暂保留 colN）</p>
      <table class="wide">
        <thead>
          <tr>
            <th>CSV#</th><th>DB列</th><th>订案名</th><th>中文摘要</th><th>类型</th>
            <th>状态</th><th>读表</th><th>偏移/VA</th><th>语义详情</th>
          </tr>
        </thead>
        <tbody>{col_rows or '<tr><td colspan="9" class="muted">无列定义</td></tr>'}</tbody>
      </table>
    </section>
"""
    return page_fn(tid, f"cfg/{tid}.html", body)


def kind_badge(kind: str) -> str:
    k = kind or "enum"
    color = CONVERTER_KIND_COLORS.get(k, "#757575")
    label = CONVERTER_KIND_ZH.get(k, k)
    return f'<span class="badge" style="background:{color}">{esc(label)}</span>'


def build_enum_index_page(registry: dict, page_fn) -> str:
    rows = ""
    for conv, entry in registry.items():
        slug = entry["slug"]
        n_vals = len(entry.get("values_list") or [])
        n_use = len(entry.get("usages") or [])
        rows += f"""
    <tr>
      <td><a href="{esc(slug)}.html"><code>{esc(conv)}</code></a></td>
      <td>{kind_badge(entry.get('kind', 'enum'))}</td>
      <td>{esc(entry.get('title_zh') or '—')}</td>
      <td>{n_vals}</td>
      <td>{n_use}</td>
      <td class="muted enum-desc">{esc(entry.get('desc_zh') or '')}</td>
    </tr>"""
    body = f"""
    <p class="breadcrumb"><a href="../index.html">配置表79</a> / 配置枚举</p>
    <section class="hero">
      <h2>配置枚举 · {len(registry)} 个转换函数</h2>
      <p class="lead">由 schema 列 <code>enum_values</code> + <code>enums.json</code> 汇总；每项含中文语义说明</p>
    </section>
    <table class="wide">
      <thead>
        <tr><th>转换函数</th><th>类型</th><th>中文名</th><th>取值数</th><th>引用列</th><th>说明</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
"""
    return page_fn("配置枚举", "cfg/enums/index.html", body)


def build_enum_detail_page(entry: dict, page_fn) -> str:
    conv = entry["converter"]
    slug = entry["slug"]
    kind = entry.get("kind", "enum")
    asm_va = entry.get("asm_va", "")
    ida_note = entry.get("ida_note", "")
    data_refs = entry.get("data_refs") or []
    val_rows = ""
    for v in entry.get("values_list") or []:
        nm = v.get("name", "")
        val_rows += f"""
    <tr id="{esc(anchor_id(nm))}">
      <td><code>{esc(nm)}</code></td>
      <td><code>{esc(v.get('value'))}</code></td>
      <td>{esc(v.get('label_zh') or '—')}</td>
    </tr>"""
    refs_html = ""
    if data_refs:
        refs_html = "<ul>" + "".join(
            f"<li><code>{esc(r)}</code></li>" for r in data_refs
        ) + "</ul>"
    ida_panel = f"""
    <section class="asm-panel enum-ida-panel">
      <h3>IDA 证据</h3>
      <dl class="asm-dl">
        <dt>函数</dt><dd><code>{esc(conv)}</code> {kind_badge(kind)}</dd>
        <dt>VA</dt><dd><code>{esc(asm_va or '—')}</code></dd>
        <dt>数据段</dt><dd>{refs_html or '—'}</dd>
      </dl>
      <p class="muted enum-ida-note">{esc(ida_note or entry.get('desc_zh') or '')}</p>
    </section>"""
    empty_vals_msg = {
        "string_copy": "此函数为 std::string 字段读取，无符号名/数值对。",
        "int_parse": "此函数为 strtol 整型解析，CSV 直接写数字。",
        "float_parse": "此函数为 strtod 浮点解析，CSV 直接写角度/小数。",
        "banner_row_lookup": "按 banner 表行号取图片路径，非固定枚举。",
    }.get(kind, "无命名取值。")
    use_rows = ""
    seen = set()
    for u in entry.get("usages") or []:
        key = (u.get("table"), u.get("column"))
        if key in seen:
            continue
        seen.add(key)
        tbl = u.get("table", "")
        use_rows += f"""
    <tr>
      <td><a href="../{esc(tbl)}.html"><code>{esc(tbl)}</code></a></td>
      <td><code>{esc(u.get('column'))}</code></td>
      <td>{esc(u.get('display_name') or '')}</td>
      <td><code>{esc(u.get('csv_index'))}</code></td>
    </tr>"""
    body = f"""
    <p class="breadcrumb"><a href="../index.html">配置表79</a> / <a href="index.html">配置枚举</a> / <code>{esc(conv)}</code></p>
    <h2><code>{esc(conv)}</code> {kind_badge(kind)}</h2>
    <p class="lead">{esc(entry.get('title_zh') or conv)}</p>
    <p class="muted">{esc(entry.get('desc_zh') or '')}</p>
    {ida_panel}
    <section>
      <h3>取值 · {len(entry.get('values_list') or [])}</h3>
      <table class="wide enum-value-table">
        <thead><tr><th>符号名</th><th>数值</th><th>中文语义</th></tr></thead>
        <tbody>{val_rows or f'<tr><td colspan="3" class="muted">{esc(empty_vals_msg)}</td></tr>'}</tbody>
      </table>
    </section>
    <section>
      <h3>引用列 · {len(seen)}</h3>
      <table class="wide">
        <thead><tr><th>表</th><th>列名</th><th>中文摘要</th><th>CSV#</th></tr></thead>
        <tbody>{use_rows or '<tr><td colspan="4" class="muted">—</td></tr>'}</tbody>
      </table>
    </section>
"""
    return page_fn(conv, f"cfg/enums/{slug}.html", body)


def generate_cfg_site(page_fn) -> int:
    index, tables = load_cfg_tables()
    registry = build_registry(tables)
    SITE_CFG.mkdir(parents=True, exist_ok=True)
    SITE_ENUMS.mkdir(parents=True, exist_ok=True)
    (SITE_CFG / "index.html").write_text(
        build_cfg_index_page(index, tables, page_fn), encoding="utf-8"
    )
    for tbl in tables:
        tid = tbl.get("id", "unknown")
        (SITE_CFG / f"{tid}.html").write_text(
            build_cfg_detail_page(tbl, page_fn, registry), encoding="utf-8"
        )
    (SITE_ENUMS / "index.html").write_text(
        build_enum_index_page(registry, page_fn), encoding="utf-8"
    )
    for conv, entry in registry.items():
        (SITE_ENUMS / f"{entry['slug']}.html").write_text(
            build_enum_detail_page(entry, page_fn), encoding="utf-8"
        )
    return len(tables)


if __name__ == "__main__":
    from build_site import page as _page

    n = generate_cfg_site(_page)
    print(f"Generated {n} cfg pages -> {SITE_CFG}")

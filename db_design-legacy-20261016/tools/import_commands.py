#!/usr/bin/env python3
"""把 protocol_analysis 的 915 条命令导入为 db_design 的命令模型。

口径见 `db_design/docs/01-命令模型.md`；模型契约见
`db_design/schema/commands/_schema.json`。

产物
====
  db_design/schema/commands/<CMD-id>.json   一条命令一份（915 份）
  db_design/schema/commands/index.json      按方向/协议类/状态/能力索引

幂等规则（重要）
================
本脚本**只补不覆盖**：
  * `asm_verification.status != "IMPORTED"` 的命令，其 `asm_verification`
    原样保留（复核结论不能被重跑冲掉）；
  * 非空的 `behavior` / `capabilities` / `db_effects` / `structs` 覆盖结果
    一律保留；
  * `fields` 每次重跑都从 fields.csv 重建（那是导入层的投影，规则确定）。

人工复核覆盖
============
`schema/commands/_overrides/<CMD-id>.json` 是唯一的例外：当 IDA 汇编证明
fields.csv 的口径有误（漏字段 / 宽度错 / 把内存槽当成线长）时，在那里写
`drop` / `patch` / `add` / `wire_length_expr`，由本脚本在 `build_struct`
之前套用。**改动必须附证据 VA**（覆写文件的 `evidence[]`）。

README 元信息里的**具体地址/槽位**记错（不是「同一处的另一种记法」，而是指到了
另一个语义点，如把闭合点写成校验失败后的报错调用点）时，用该文件的 `meta`
覆盖 `capacity` / `closer_va` / `dispatch_slot` / `dispatch_va` 等 —— 这些不是
线长量，改它们不会动 `wire_fingerprint`。

覆写带 `revision`：revision 变化会判定字段口径已变，旧 `asm_verification`
作废（回到 `IMPORTED`），必须重跑 IDA 复核——避免「改了字段却留着旧结论」。

CSV 修复
========
`protocol_analysis/.../fields.csv` 存在两类畸形行（历史遗留，见坑 ⑲/㉓）：

1. 线类型被 ASCII 逗号切开：`array<item` + `A1>` ⇒ 需按尖括号配平合并为
   `array<item,A1>`；
2. 文本列内含 ASCII 逗号（`含义` 里写 `` `cmp edi,36h` ``）⇒ 该行多出若干列。

修复策略：先按尖括号配平把线类型合并，再用「用途列的起始特征」
（`经`/`交`/`来源`/`→`/`vt[`…）从右往左切出 `用途/取值/证据/置信` 四列，
中间全部并回 `含义`；缺 `取值或枚举` 列的 9 列行补空串。
每一处修复都记入该命令的 `import_repairs`，可被站点显示，便于复核。
"""

from __future__ import annotations

import csv
import fnmatch
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTO_COMMANDS = ROOT / "protocol_analysis" / "commands"
SCHEMA = Path(__file__).resolve().parents[1] / "schema"
OUT_DIR = SCHEMA / "commands"
OVERRIDE_DIR = OUT_DIR / "_overrides"
COMPOSITES_DIR = SCHEMA / "composites"
INDEX_PATH = OUT_DIR / "index.json"

CSV_HEADER = ["序号", "偏移", "长度", "线类型", "字段名", "含义", "用途", "取值或枚举", "证据VA", "置信度"]

TODAY = date.today().isoformat()

VA_RE = re.compile(
    r"0[xX][0-9A-Fa-f]{4,9}"
    # 部分 README 的 VA 写成**裸十六进制**（`处理块范围 | B6B8C8..B6BB52`）：
    #   要求「6~9 位、至少含一个字母、两侧不是标识符字符」，避免把纯数字当 VA。
    r"|(?<![0-9A-Za-z_])(?=[0-9A-Fa-f]*[A-Fa-f])[0-9A-Fa-f]{6,9}(?![0-9A-Za-z_])"
)
FUNC_RE = re.compile(r"\bsub_[0-9A-Fa-f]{5,8}\b")
CMD_ID_RE = re.compile(r"(?:SC|CS)-0x[0-9A-Fa-f]{4}-[a-z_]+-[A-Za-z0-9_]+")
VT_RE = re.compile(r"vt\[(0x[0-9A-Fa-f]+)\]")
# 「无容量申请」的判定（坑㉞）：README 明说没有申请解码缓冲时，`声明容量` 行里**不该**
# 再抠出数字。实测写法：`（无容量申请：块内无 vt[0x78] 分配器调用）` / `**无**（零负载）` /
# `无（未申请解码缓冲）` / `—`。判据只认「行首就是『无』」和「整行只有一个破折号」，
# 以及明确的「无容量申请」字样 —— 不用「零负载」这类可能出现在正常行里的词。
NOCAP_RE = re.compile(r"^[（(]?\s*\**\s*无|^\s*[—–]\s*$|无容量申请")
# 散文回填的去向槽过滤（口径同判定层 `verify_commands_ida.py` 的 `MAX_SLOT`/`ERROR_SLOT`）：
# 超上限的是对象成员（`[X+2C5Ch]` 这类），`0x64` 是报错槽 —— 都不是业务去向。
PROSE_MAX_SLOT = 0x1000
PROSE_ERROR_SLOT = 0x64
VAR_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# `用途` 列的起始特征：命中即认为「这一列起是用途」。
PURPOSE_START = re.compile(
    r"^(经|交|来源|去向|发往|同|仅|走|由|按|把|用|作|给|存|读|写|提交|发送|分发|"
    r"数组基址|数组元素|元素成员|元素读取|结构体|结构成员|指针|复合写入|整块|整体|单元|"
    r"NUL 串|预留|槽位|游标|容量|日志|打印器|克隆|拷贝|回显|填充|填充值|"
    r"→|->|=>|=>|vt\[|`→|`vt\[|\*\*)"
)

# 文本列里出现 ASCII 逗号时，多余列最常见落在「证据VA」（如 `cmp edi,7`）。
# 这条正则用来判断一个片段是否像证据。
EVIDENCE_ISH = re.compile(r"(0x[0-9A-Fa-f]{4,}|sub_[0-9A-Fa-f]{5,}|^\s*-\s*$)")

# README §1 元信息表的键（含历史变体）；前缀匹配处理「（…）」后缀变体。
META_KEYS = {
    "opcode", "方向", "协议类", "命令名", "处理块范围", "名字符串引用点", "名字符串",
    "处理函数", "声明容量", "声明容量（解码缓冲）", "长度闭合点", "去向", "代码位置",
    "发送去向", "opcode 写入证据", "opcode 写入/分发证据", "分发器", "配对命令",
    "配对命令（同 opcode 反向）", "关联命令", "同族", "错误码", "容量旁证证据",
    "提交", "附加通知", "附加通知回调", "收尾函数", "分发路径", "名字符串引用点/路径",
    # 后续批次 README 的**拼写变体**（同义，只是换了字）。不认下来就会被静默丢掉：
    # `名字串引用点`（少「符」，500 例）`名字字符串`（多一个「字」，20 例）
    # `报错码`（200 例）`容量申请证据`（163 例）。
    "名字串引用点", "名字字符串", "报错码", "容量申请证据",
}
META_KEY_PREFIXES = (
    "处理函数", "名字符串", "名字串", "配对命令", "关联命令", "声明容量", "opcode 写入",
    "附加通知", "错误码", "报错码", "容量旁证", "容量申请",
)

SCALAR_WIDTH = {"u8": 1, "i8": 1, "u16": 2, "i16": 2, "u32": 4, "i32": 4, "u64": 8, "f32": 4, "f64": 8}

# 标量线类型：数组元素命中这些名字时不算结构体（避免 `array<u32,N>` 的字段名被误当结构）
SCALAR_WT = {"u8", "i8", "u16", "i16", "u32", "i32", "u64", "f32", "f64", "str", "bytes", "char", "pad"}

SCALAR_ARR_RE = re.compile(r"^(?P<elem>u8|i8|u16|i16|u32|i32|u64|f32|f64|str)\s*\[\s*(?P<tail>[^\]]+)\s*\]$")
# `struct config` / `struct<ms>` / `struct(pilot)` / `struct{12}` 四种写法；前三种带结构名
STRUCT_WT_RE = re.compile(r"^struct[\s<(]\s*(?P<name>[A-Za-z_]\w*)")
ELEM_LEN_RE = re.compile(r"^\s*(\d+)\s*[·*×]")
PURE_INT_RE = re.compile(r"^\d+$")
# 线长是否**恒定**：只由字面量算术构成（无驱动变量）即恒定。
# 旧口径只认单一字面量，把 `4 + 73 + 4 + 1` 这类定长和式误判成变长（538 条命令受影响）。
FIXED_EXPR_RE = re.compile(r"^[\d\s+()]+$")
CJK_RE = re.compile(r"[\u3400-\u9FFF]")
# 线长表达式里允许出现的字符（用于判断 README 摘出来的串是不是真的线长）
LEN_EXPR_RE = re.compile(r"^[\d\sA-Za-z_+*·×()（）]+$")

COUNT_WORD_RE = re.compile(r"(num|count|cnt|len|条数|个数|数量|计数|上限)")


# ------------------------------------------------------------------ 工具

def split_top_level(text: str) -> list[str]:
    """按顶层分隔符（`,` 或空白）切分，忽略 `<>`/`{}`/`[]` 内部的分隔符。"""
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in text:
        if ch in "<{[":
            depth += 1
        elif ch in ">}]":
            depth = max(0, depth - 1)
        if depth == 0 and (ch == "," or ch.isspace()):
            if buf:
                out.append("".join(buf).strip())
                buf = []
            continue
        buf.append(ch)
    if buf:
        out.append("".join(buf).strip())
    return [p for p in out if p]

def vas(text: str) -> list[str]:
    out = []
    for m in VA_RE.findall(text or ""):
        out.append(m if m[:2].lower() == "0x" else "0x" + m)
    return out


def first_va(text: str) -> str | None:
    found = vas(text)
    return found[0] if found else None


def unquote_ticks(text: str) -> str:
    return (text or "").replace("`", "").strip()


def go_name(raw: str, fallback: str) -> str:
    """`item_id[]` -> `ItemId`；无可用名时用 fallback（如 `F3`）。"""
    s = unquote_ticks(raw)
    s = s.replace("[]", "").replace("[", "_").replace("]", "")
    s = re.sub(r"[^0-9A-Za-z_]", "_", s).strip("_")
    if not s or s in {"-", "?"} or s[0].isdigit():
        return fallback
    parts = [p for p in s.split("_") if p]
    name = "".join(p[:1].upper() + p[1:] for p in parts)
    if not name or not name[0].isalpha():
        return fallback
    # 与 Go 关键字冲突的极端情况：加后缀
    if name in {"Type", "Map", "Range", "Func", "Struct", "Interface", "Break", "Default", "Select", "Chan", "Go", "Defer", "Var", "Const"}:
        name += "_"
    return name


# ------------------------------------------------------------------ CSV 修复

def looks_like_purpose(cell: str) -> bool:
    """粗判一个单元格是否像 `用途` 列（用于标出切分可疑的行）。"""
    if not cell:
        return False
    if cell.strip() == "-":
        return True
    if PURPOSE_START.match(cell):
        return True
    return any(k in cell for k in ("vt[", "来源", "→", "经", "交", "日志", "数组", "元素", "结构", "指针", "预留", "提交", "发送", "分发", "读取", "写入", "回显"))


def repair_row(cells: list[str]) -> tuple[list[str] | None, list[str]]:
    """把畸形 CSV 行修成 10 列；返回 (行, 修复标记)。修不出来返回 (None, ...)。"""
    repairs: list[str] = []
    cells = [c.strip() for c in cells]
    if len(cells) < 5:
        return None, repairs

    # ① 线类型被逗号切开：按尖括号配平合并（第 4 列 = index 3）
    guard = 0
    while len(cells) > 4 and cells[3].count("<") > cells[3].count(">") and guard < 4:
        cells[3] = f"{cells[3]},{cells[4]}"
        del cells[4]
        guard += 1
    if guard:
        repairs.append(f"wire_type_comma_merge_x{guard}")

    n = len(cells)
    if n == 10:
        return cells, repairs

    if n == 9:
        # 9 列行有两种成因：
        #  a) `struct <名>` 行省了「字段名」列（结构名就写在线类型里）
        #  b) 其余行缺「取值或枚举」列（闭合行常见）
        sm = STRUCT_WT_RE.match(cells[3])
        if sm and CJK_RE.search(cells[4] or ""):
            cells.insert(4, sm.group("name"))
            repairs.append("missing_name_col_from_struct_wt")
        else:
            cells.insert(7, "")
            repairs.append("missing_enum_col")
        return cells, repairs

    if n > 10:
        # 多出的列是文本里的 ASCII 逗号。先扫出「用途」的起点（index i），
        # 中间的列并回 `含义`；再用「置信 = 最后一列、证据 = 中间几列」切尾，
        # 这样 `含义` 与 `证据VA`（如 `cmp edi,7`）里的逗号都能还原。
        i = 5
        while i < n - 4:
            if i > 5 and PURPOSE_START.match(cells[i]):
                break
            i += 1
        meaning = ",".join(cells[5:i])
        rest = cells[i:]
        if len(rest) < 4:
            return None, repairs + ["unrepairable"]
        purpose, enum = rest[0], rest[1]
        evidence = ",".join(rest[2:-1])
        confidence = rest[-1]
        cells = cells[:5] + [meaning, purpose, enum, evidence, confidence]
        extras = len(rest) - 4
        repairs.append(f"text_comma_merge_x{n - 10}")
        if extras > 0:
            repairs.append(f"evidence_comma_merge_x{extras}")
        if not looks_like_purpose(purpose):
            # 切分点可能落在错的列上：标出来供 IDA 复核（信息不丢，但边界可疑）
            repairs.append("ambiguous_comma_split")
        return cells, repairs

    return None, repairs + ["too_few_cols"]


def read_fields_csv(path: Path) -> tuple[list[dict], list[str]]:
    """返回 (行列表, 修复记录)；行字典带 `_line`（CSV 行号）与 `_fixed`（该行被修过）。"""
    rows: list[dict] = []
    repairs: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        if header is None:
            return rows, repairs
        if [h.strip() for h in header] != CSV_HEADER:
            repairs.append("header_unexpected")
        for line_no, raw in enumerate(reader, start=2):
            if not any(c.strip() for c in raw):
                continue
            cells, fix = repair_row(raw)
            if cells is None:
                repairs.append(f"line{line_no}:{'/'.join(fix)}")
                continue
            for f in fix:
                repairs.append(f"line{line_no}:{f}")
            row = dict(zip(CSV_HEADER, cells))
            row["_line"] = line_no
            row["_fixed"] = bool(fix)
            row["_raw_cols"] = len(raw)
            rows.append(row)
    return rows, repairs


def to_field(row: dict, seq: int) -> dict:
    name = unquote_ticks(row["字段名"])
    evidence = [v for v in (row["证据VA"] or "").replace("，", "|").split("|") if v.strip()]
    evidence = [e.strip() for e in evidence]
    is_closure = "闭合" in name
    offset = unquote_ticks(row["偏移"])
    field = {
        "seq": -1 if is_closure else seq,
        "offset": offset or "?",
        "length": unquote_ticks(row["长度"]),
        "wire_type": unquote_ticks(row["线类型"]),
        "name": name or f"f_{offset}",
        "meaning": (row["含义"] or "").strip(),
        "purpose": (row["用途"] or "").strip(),
        "enum": None if unquote_ticks(row["取值或枚举"]) in ("", "-") else unquote_ticks(row["取值或枚举"]),
        "evidence_va": evidence or ["?"],
        "confidence": (row["置信度"] or "").strip() or "?",
        "disposition": "TBD",
        "entity_ref": None,
        "csv_line": row.get("_line"),
    }
    if row.get("_fixed"):
        # 该行 CSV 列数畸形（线类型被逗号切开 / 文本内含 ASCII 逗号）：
        # 导入期按启发式还原，必须由 IDA 汇编复核后才能当结论用。
        field["needs_review"] = True
        field["csv_raw_cols"] = row.get("_raw_cols")
    if is_closure:
        field["is_closure"] = True
    return field


# ------------------------------------------------------------------ README 元信息

def read_meta(readme: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    text = readme.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
        if not m:
            continue
        key = m.group(1).strip()
        if key in {"项", "序号", "字段名"} or re.fullmatch(r":?-+:?", key):
            continue
        if key in META_KEYS or key.startswith(META_KEY_PREFIXES):
            if key not in meta:
                meta[key] = m.group(2).strip()
    return meta


def meta_first(meta: dict[str, str], *keys: str) -> str | None:
    for k in keys:
        if k in meta:
            return meta[k]
    for k in keys:
        for mk, mv in meta.items():
            if mk.startswith(k):
                return mv
    return None


# ------------------------------------------------------------------ 结构体推导

def parse_array(wire_type: str) -> tuple[str | None, str | None, int | None]:
    """解析数组线类型，返回 (元素类型, 尾标记, 字面上限)。

    支持 `array<X>` / `array<X,N>` / `array<X N>` / `array<struct<N>,N>` /
    `array<{u32,u32},N>` / `array<elem 58>` / `u32[10]` / `u32[N]`。
    元素类型为 `struct`/`elem` 这类占位时按字面返回，由调用方再归类。
    """
    wt = (wire_type or "").strip()
    m = SCALAR_ARR_RE.match(wt)
    if m:
        tail = m.group("tail").strip()
        return m.group("elem"), tail, int(tail) if tail.isdigit() else None
    if wt.startswith("array<") and wt.endswith(">"):
        parts = split_top_level(wt[len("array<"):-1])
        if not parts:
            return None, None, None
        elem = parts[0]
        tail = parts[1] if len(parts) > 1 else None
        if elem.startswith("struct<") and elem.endswith(">"):
            elem = elem[len("struct<"):-1].strip()
        elif elem == "struct":
            elem = "struct"
        return elem, tail, int(tail) if (tail and tail.isdigit()) else None
    return None, None, None


def parse_struct_wt(wire_type: str) -> str | None:
    """`struct config` / `struct<ms>` / `struct(pilot)` -> 结构名；`struct{12}` / `struct` -> None。"""
    m = STRUCT_WT_RE.match((wire_type or "").strip())
    return m.group("name") if m else None


_COMPOSITE_IDS: set[str] | None = None


def composite_ids() -> set[str]:
    """`schema/composites/` 的 id 集合（进程内缓存）。"""
    global _COMPOSITE_IDS
    if _COMPOSITE_IDS is None:
        _COMPOSITE_IDS = {
            (json.loads(p.read_text(encoding="utf-8")).get("id") or p.stem)
            for p in COMPOSITES_DIR.glob("*.json")
        } if COMPOSITES_DIR.is_dir() else set()
    return _COMPOSITE_IDS


def resolve_composite_ref(name: str, wire_type: str = "", element: str | None = None) -> str | None:
    """把聚合体挂到 `schema/composites/<id>.json`：线类型里的结构名优先，其次字段名/元素名。

    命令模型**不复制**成员清单（composites 是唯一出处）；这里只落一个 id，
    站点与代码生成据此内联展开成员，免得出现「成员见 XXX」这种要人再跳一次的写法。
    标量数组（`array<u32,N>`）不参与，避免把 `missionunit_set` 这类字段名误当结构。
    """
    ids = composite_ids()
    if element and element in ids:
        return element
    wt = (wire_type or "").strip()
    elem = array_elem_name(wt)
    if elem and elem in ids:
        return elem
    # `avatar(18B)` 这类把尺寸写进括号的写法：剥掉再看
    wt_base = re.sub(r"\([^)]*\)\s*$", "", wt).strip()
    if wt_base in ids:
        return wt_base
    named = parse_struct_wt(wt)
    if named and named in ids:
        return named
    anon = named is None and (
        re.match(r"^struct(\{|\(|$)", wt)
        or (elem is not None and elem not in SCALAR_WT))
    if anon:
        base = (name or "").split(".")[0].replace("[]", "").strip()
        if base in ids:
            return base
    return None


def array_elem_name(wire_type: str) -> str | None:
    """数组线类型的元素名（`array<X,N>` / `array<struct<X>,N>`）。占位符 `struct` 原样返回。"""
    m = re.match(r"^array<\s*(?:struct<\s*)?\s*([A-Za-z_]\w*)", (wire_type or "").strip())
    return m.group(1) if m else None


def elem_length_of(length_expr: str) -> str | None:
    m = ELEM_LEN_RE.match(length_expr or "")
    return m.group(1) if m else None


def implied_elem_width(length_expr: str) -> int | None:
    """长度列里**元素线宽**的数值：`6×14=84` → 6、`23N` → 23、`113·N1` → 113。

    纯数字长度（`79`）看不出是元素宽还是总长，返回 None（由调用方按「总长 == 元素线长」兜底）。
    """
    s = (length_expr or "").strip()
    m = re.match(r"^(\d+)\s*(?:[×x*·]|(?=[A-Za-z_]))", s)
    return int(m.group(1)) if m else None


def array_count_token(length_expr: str, tail_hint: str = "") -> str:
    """数组条数记号：`6×14=84` → `14`、`23N` → `N`、`113·N1` → `N1`；纯数字长度用草稿尾巴兜底。

    条数只能来自**长度列**（或草稿尾巴的字面条数），不能来自草稿的元素名
    （`array<score_ranking,104>` 里的 104 是槽步进）。
    """
    s = (length_expr or "").strip()
    m = re.match(r"^\d+\s*[×x*·]\s*([^\s=]+)", s)
    if m:
        return m.group(1)
    toks = [t for t in VAR_TOKEN_RE.findall(s) if not t.isdigit()]
    if toks:
        return toks[0]
    m = re.match(r"^\d+\s*([^\s\d].*)$", s)
    if m:
        return m.group(1).strip()
    hint = (tail_hint or "").strip()
    return hint if hint.isdigit() else "1"


_COMPOSITE_LEN: dict[str, int | None] | None = None
_COMPOSITE_MEMBERS: dict[str, set[str]] | None = None


def composite_lengths() -> dict[str, int | None]:
    """`schema/composites/` 的 id → 元素线长（`length`），进程内缓存。"""
    global _COMPOSITE_LEN, _COMPOSITE_MEMBERS
    if _COMPOSITE_LEN is None:
        out: dict[str, int | None] = {}
        mem: dict[str, set[str]] = {}
        if COMPOSITES_DIR.is_dir():
            for p in COMPOSITES_DIR.glob("*.json"):
                try:
                    d = json.loads(p.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                cid = d.get("id") or p.stem
                ln = d.get("length")
                if isinstance(ln, str) and ln.strip().isdigit():
                    ln = int(ln.strip())
                out[cid] = ln if isinstance(ln, int) else None
                mem[cid] = {m.get("name") for m in d.get("members") or [] if m.get("name")}
        _COMPOSITE_LEN = out
        _COMPOSITE_MEMBERS = mem
    return _COMPOSITE_LEN


def composite_member_names(ref: str) -> set[str]:
    composite_lengths()
    return (_COMPOSITE_MEMBERS or {}).get(ref, set())


LOG_TMPL_RE = re.compile(r"([A-Za-z_]\w*)\s*=\s*\{([^}]*)\}")


def log_template_members(*texts: str) -> set[str]:
    """从「日志 `ranking={score,pilot_id,…}`」这类文本里抠出成员名，用作宽度的旁证。"""
    out: set[str] = set()
    for t in texts:
        m = LOG_TMPL_RE.search(t or "")
        if not m:
            continue
        for tok in re.split(r"[,\s]+", m.group(2)):
            tok = tok.strip().rstrip("=")
            if re.match(r"^[A-Za-z_]\w*$", tok):
                out.add(tok)
    return out


def elem_width_of(length_expr: str, wire_type: str) -> int | None:
    """长度列隐含的**元素线宽**：`8×15=120` → 8、`73N` → 73；纯数字时用条数反除（`648`+`2` → 324）。"""
    w = implied_elem_width(length_expr)
    if w is not None:
        return w
    lit = (length_expr or "").strip()
    if not PURE_INT_RE.match(lit):
        return None
    parts = wire_type[len("array<"):-1].split(",", 1) if wire_type.startswith("array<") else []
    if len(parts) > 1 and parts[1].strip().isdigit():
        cnt = int(parts[1].strip())
        if cnt and int(lit) % cnt == 0:
            return int(lit) // cnt
    return None


def ref_matches_elem_width(ref: str, length_expr: str, wire_type: str = "") -> bool:
    """元素引用与长度列是否自洽：`array<X,N>` 的 X 线长必须等于长度列里的元素线宽。

    不自洽说明**按名字挂错了结构**（同名不同体，如两个域都有 `ranking`/`item_list`），
    这时改按线宽重挂、或摘除引用让站点显示「元素未建模」，都不能展开一份错的成员清单。
    """
    comp_len = composite_lengths().get(ref)
    if comp_len is None:
        return True
    width = elem_width_of(length_expr, wire_type)
    if width is not None:
        return width == comp_len
    lit = (length_expr or "").strip()
    if PURE_INT_RE.match(lit):
        return int(lit) == comp_len
    return True


def pick_ref_by_width(width: int | None, members_hint: set[str]) -> tuple[str | None, list[str]]:
    """按元素线宽找候选 composite（唯一，或日志成员名 ≥2 命中）；返回 (id, 全部候选)。"""
    if width is None:
        return None, []
    cands = sorted(cid for cid, ln in composite_lengths().items() if ln == width)
    if members_hint:
        hits = [cid for cid in cands if len(composite_member_names(cid) & members_hint) >= 2]
        if len(hits) == 1:
            return hits[0], cands
        return None, hits or cands
    return (cands[0], cands) if len(cands) == 1 else (None, cands)


def is_count_like(name: str, meaning: str, wire_type: str) -> bool:
    if wire_type not in {"u8", "u16", "u32", "i8", "i16", "i32"}:
        return False
    blob = f"{name} {meaning}"
    return bool(COUNT_WORD_RE.search(blob))


def guess_count_field(payload: list[dict], idx: int, length_expr: str) -> tuple[str | None, str | None]:
    """推断驱动条数的字段；返回 (字段名, 依据)。依据 ∈ {length_expr, heuristic, nearest_scalar}。"""
    toks = [t for t in VAR_TOKEN_RE.findall(length_expr or "") if not t.isdigit()]
    for t in toks:
        for prev in payload[:idx]:
            if prev["name"] == t or prev["name"].replace("[]", "") == t:
                return prev["name"], "length_expr"
    for prev in reversed(payload[:idx]):
        if is_count_like(prev["name"], prev["meaning"], prev["wire_type"]):
            return prev["name"], "heuristic"
    for prev in reversed(payload[:idx]):
        if prev["wire_type"] in {"u32", "u16", "u8"}:
            return prev["name"], "nearest_scalar"
    return None, None


def fix_wire_len_for_elem_width_cells(cmd: dict) -> list[str]:
    """长度列把**元素线宽**当总长记时，线长表达式要重算成 `宽·条数`。

    草稿在数组行的长度列只写元素线宽（`130`），条数另在线上字段里。这种行会被打上
    `length_is_elem_width`（见 `build_command`）。若不改线长表达式，`field_sum` 会把
    `4 + 4 + 4 + 130` 当成**定长总长**，与 README 的 `12 + 130N` 直接打架，容量/闭合
    复核也跟着错。按 §3.1，数组项的线长记账必须是「宽·条数」。
    """
    w = cmd["wire"]
    payload = [f for f in cmd["fields"]
               if f["seq"] >= 0 and f["seq"] != 0 and not f.get("is_closure") and not f.get("is_member_row")]
    if not any(f.get("length_is_elem_width") for f in payload):
        return []
    return rebuild_field_sum_len(cmd, "wire_len_elem_width_cells")


UNNAMED_CLAUSE_RE = re.compile(
    r"(?:[；;，,、]\s*)?内部成员未逐一命名\s*(?:（[^）)]*）|\([^）)]*\))?"
)

MEMBER_ROW_RE = re.compile(r"^(?P<parent>.+)\.(?P<member>[^.]+)$")

# 草稿把「这串有多少字节」写成**非线长口径**时的自述措辞。三类坑共用这套判据：
# 长度列写的是槽位预算 / 内存跨度 / 只写了单个元素的线宽，而不是 §3.1 的线上实写字节数。
SLOT_BUDGET_RE = re.compile(r"槽位预算|线长\s*=\s*串长\s*\+\s*1")
STRUCT_SPAN_RE = re.compile(r"跨度")

# 线长口径**纪元**：任何会改变字段字节数的导入规则调整都必须 +1。
# 它进 `wire_fingerprint`，所以 bump 一次 = 全部已复核命令指纹失配 = 复核作废重跑
# （原始切片留在 `_verify/_raw/`，重跑 `ingest --batch N` 即可，不必回 IDA）。
#   1 —— 槽位预算 `str` → `var(≤N)`；struct 内存跨度 → composite 线长；
#        字面量条数数组补全 `N × 元素宽`。此前这些长度被当成线上字节数，复核结论不成立。
WIRE_EPOCH = 1


def wire_fingerprint(cmd: dict) -> str:
    """字段口径指纹：任何字段的**线上字节数**变化都会改它。

    `merge_previous` 用它判断旧 `asm_verification` 还能不能沿用——复核结论认的是
    「这些字段就是这个宽度、这条长度表达式」，字节数一变结论就不再成立。只取影响线长的量
    （名字/线类型/长度/闭合标记/成员行标记），不含 `meaning` 等语义文字，
    免得改一句描述就把复核打回重做。

    指纹里带 `WIRE_EPOCH`，所以规则口径整体一换（epoch +1）就**全部失配**，
    已复核命令自动作废——不必逐个去比字节数。
    """
    parts = [f"epoch={WIRE_EPOCH}"]
    parts += [
        "|".join([
            f.get("name") or "",
            f.get("wire_type") or "",
            str(f.get("length") or ""),
            "C" if f.get("is_closure") else "",
            "M" if f.get("is_member_row") else "",
            str(f.get("length_is_elem_width") or ""),
        ])
        for f in cmd.get("fields", [])
    ]
    w = cmd.get("wire") or {}
    parts.append("expr=" + str(w.get("length_expr") or ""))
    parts.append("fixed=" + str(bool(w.get("fixed"))))
    return hashlib.sha1("\n".join(parts).encode("utf-8")).hexdigest()[:16]


# 复核**输入**口径纪元：任何会改变「判定层拿什么去对位」的模型字段调整都必须 +1。
# 与 `WIRE_EPOCH` 分开，因为这两类变化是**独立**的：`wire_fingerprint` 只管字节数，
# 而 capacity/closer/dispatch 这些点位的 VA 改了并不动字节数，却同样让旧结论失效。
#   1 —— `dispatch_slot`/`dispatch_va` 支持从 README 散文回填（坑㉛）：
#        此前 50 条命令的 `dispatch_slot` 是空的、判定层按 `absent` 跳过而去向检查从未真正跑过；
#        回填后这些命令的检查输入变了，旧「通过」不成立。
CHECK_EPOCH = 1

# 进 `check_fingerprint` 的键：判定层对位要用到的**全部**点位/槽位输入。
CHECK_INPUT_KEYS = (
    "handler_va", "block", "capacity", "capacity_va", "closer_va",
    "dispatch_slot", "dispatch_va", "name_str_va", "notify_va", "opcode_write_va",
)

# 其中**由复核器回填进模型**的那几个（`verify_commands_ida.py` 的 `_set(...)`）：
# 导入层只能从 README 推导，推不出来时不能把复核器的结论冲掉（坑㉟）。
POINT_FIELDS = ("capacity", "capacity_va", "closer_va", "dispatch_slot", "dispatch_va", "block")


def check_fingerprint(cmd: dict) -> str:
    """复核输入指纹：点位/槽位输入一变就失配，旧 `asm_verification` 作废。

    单独存在的原因：`wire_fingerprint` 只覆盖线长，而「去向槽」「闭合点」「容量点」
    这些输入可以独立变化（例如坑㉛ 从散文回填 `dispatch_slot`，
    文件一个字节都没变，但判定层从此会真的去比对去向）。
    """
    parts = [f"epoch={CHECK_EPOCH}"]
    for k in CHECK_INPUT_KEYS:
        parts.append(f"{k}={cmd.get(k)!r}")
    parts.append("error_vas=" + repr(sorted((cmd.get("extra") or {}).get("error_vas") or [])))
    return hashlib.sha1("\n".join(parts).encode("utf-8")).hexdigest()[:16]


def rebuild_field_sum_len(cmd: dict, tag: str) -> list[str]:
    """按 §3.1 口径重算 `field_sum` 线长表达式（任何字段长度被改写后都必须重算）。

    数组项按「宽·条数」记账（`length_is_elem_width`）——只写元素宽会把总和压小；
    成员占位行不算（父字段的 composite 已摊平成员）；闭合行不算。
    原先两个定向修（元素宽 / 成员占位行）各自重算一遍，逻辑与这里重复，
    统一收口到一个函数，避免新增长度改写时漏掉重算。
    """
    w = cmd["wire"]
    if w.get("length_source") != "field_sum":
        return []
    terms: list[str] = []
    for f in cmd["fields"]:
        if f["seq"] < 0 or f["seq"] == 0 or f.get("is_closure") or f.get("is_member_row"):
            continue
        lit = (f.get("length") or "").strip()
        if not lit or lit == "-":
            continue
        cnt = f.get("length_is_elem_width")
        terms.append(f"{lit}·{cnt}" if cnt else lit)
    if not terms:
        return []
    expr = " + ".join(terms)
    if expr == w.get("length_expr"):
        return []
    before = w.get("length_expr")
    w["length_expr"] = expr
    w["fixed"] = bool(FIXED_EXPR_RE.match(expr))
    w["var_drivers"] = sorted(
        {t for t in VAR_TOKEN_RE.findall(expr) if not t.isdigit()} - {"L", "Len", "var"}
    )
    return [f"{tag}:{before} → {expr}"]


def fix_slot_budget_str_lengths(cmd: dict) -> list[str]:
    """`str` 字段的长度列写成了**槽位预算**时，改成变长写法 `var(≤N)`。

    草稿对 C 串常把「缓冲区槽位」记进长度列（`body=766`、`battlesv_host=129`），
    而线上实写的是 `strlen+1`。这样 `field_sum` 会把变长串当定长：
    `SC-0x5383` 于是成了 `4+4+129+4+4+41=186`（`fixed=True`），
    而同形的 `SC-0xFB85` 早就写成了 `var + ... + var`，README 也明写 `22 + L1 + L2`。

    判据只用草稿自己的话（「槽位预算」或「线长 = 串长+1」）——全库 34 处整数长度的
    `str` 无一例外都写了「槽位预算」，没有误伤空间。预算不丢，落到 `slot_budget`。
    """
    out: list[str] = []
    for f in cmd["fields"]:
        if f.get("wire_type") != "str" or f.get("is_closure") or f["seq"] == 0:
            continue
        lit = (f.get("length") or "").strip()
        if not PURE_INT_RE.match(lit):
            continue
        text = f"{f.get('meaning') or ''} {f.get('purpose') or ''}"
        if not SLOT_BUDGET_RE.search(text):
            continue
        f["slot_budget"] = int(lit)
        f["length"] = f"var(≤{lit})"
        out.append(f"str_slot_budget:{f['name']}({lit} → var(≤{lit})；线上实写 strlen+1)")
    return out


def fix_struct_span_lengths(cmd: dict) -> list[str]:
    """`struct` 字段的长度列写成**内存跨度**时，改回 composite 的线长。

    草稿对结构体常把对象内存跨度记进长度列，它含非线上成员，比线长大：
    `pcard` 跨度 424 / 线长 398、`bracket` 212/166、`AI` 168/165。
    跨度是分配口径，线长才是记账口径（README 也写「pcard 段定长 398」）。
    跨度与线长相等时（`order` 10/10、`rankself` 40/40）不动。
    """
    out: list[str] = []
    for f in cmd["fields"]:
        if f.get("is_closure") or f["seq"] == 0:
            continue
        ref = f.get("composite_ref")
        if not ref:
            continue
        lit = (f.get("length") or "").strip()
        if not PURE_INT_RE.match(lit):
            continue
        wire_len = composite_lengths().get(ref)
        if wire_len is None or int(lit) == wire_len:
            continue
        text = f"{f.get('meaning') or ''} {f.get('purpose') or ''}"
        if not STRUCT_SPAN_RE.search(text):
            continue
        f["memory_span"] = int(lit)
        f["length"] = str(wire_len)
        out.append(f"struct_span_to_wire:{f['name']}(跨度 {lit} → 线长 {wire_len}；ref {ref})")
    return out


def fix_literal_count_array_lengths(cmd: dict) -> list[str]:
    """`array<X,N>`（N 字面量、线上无 count 字段）的长度列只写了**单元素线宽**时，补成 `N × 宽`。

    条数不在线上，所以 `length_is_elem_width` 那条路走不到（它要求有线上条数字段）：
    `SC-0xF0AF.bonus_info` 写 29 而实为 40×29=1160，`CS-0x3C13.mailids` 写 8 而实为 50×8=400。
    元素宽取自 composite 线长或标量宽度表。
    """
    out: list[str] = []
    for f in cmd["fields"]:
        if f.get("is_closure") or f["seq"] == 0 or f.get("is_member_row"):
            continue
        if f.get("length_is_elem_width"):
            continue
        m = re.fullmatch(r"array<([^,>]+),(\d+)>", f.get("wire_type") or "")
        lit = (f.get("length") or "").strip()
        if not (m and PURE_INT_RE.match(lit)):
            continue
        elem, n = m.group(1), int(m.group(2))
        if n <= 1 or int(lit) == 0:
            continue
        width = SCALAR_WIDTH.get(elem) or composite_lengths().get(elem)
        if not width or width != int(lit):
            continue
        f["length_is_literal_count"] = n
        f["length"] = str(width * n)
        out.append(f"literal_count_array:{f['name']}({lit} → {width}×{n}={width * n}；{elem}[{n}])")
    return out


SCALAR_ARR_VAR_RE = re.compile(
    r"^(?P<elem>u8|i8|u16|i16|u32|i32|u64|f32|f64|str)\s*\[\s*(?P<tok>[A-Za-z_]\w*)\s*\]$"
)


def fix_scalar_array_var_count_lengths(cmd: dict) -> list[str]:
    """标量数组写成 `u16[N]`（N 是**变量**条数）而长度列只写了元素宽时，补成 `宽·条数`。

    条数写在类型尾巴上、且是变量（不是 `array<...>`，也不是字面量），所以坑㉖ 的
    `length_is_elem_width` 判据（要求尾巴为空）够不着：`CS-0xBCB4.ent_ids` 写 2 而线上是
    `2·N`，于是 `fixed` 被误判成 `True`、线长求和把变长数组当成 2 字节。同库的正确写法是
    长度列直接带变量（`SC-0xE4DB` 的 `2N (N≤6)`、`SC-0x2775` 的 `N`）。
    """
    out: list[str] = []
    for f in cmd["fields"]:
        if f.get("is_closure") or f["seq"] == 0 or f.get("is_member_row"):
            continue
        m = SCALAR_ARR_VAR_RE.match((f.get("wire_type") or "").strip())
        lit = (f.get("length") or "").strip()
        if not (m and PURE_INT_RE.match(lit)):
            continue
        elem, tok = m.group("elem"), m.group("tok")
        width = SCALAR_WIDTH.get(elem)
        if not width or width != int(lit):
            continue
        # 1 字节元素的房子写法就是裸变量（`N`），不写成 `1N`。
        f["length"] = f"{width}{tok}" if width > 1 else tok
        out.append(f"scalar_arr_var_count:{f['name']}({lit} → {f['length']}；{elem}[{tok}])")
    return out


def mark_member_rows(cmd: dict) -> list[str]:
    """`父.成员` 行是**成员占位行**，不是独立的线上负载字段。

    `fields.csv` 在写出 `missionunit_set`（`struct{12}` + 引用）之后，又逐行摊了
    `missionunit_set.deck_type` / `.deck_set` / `.missionunit_id`（2+2+8=12）。这 12 字节
    **已经算在父行的长度列里**，`field_sum` 再相加就是双计：
    `SC-0x1908` 于是得出 `4 + 12 + 2 + 2 + 8 = 28`，与 README 的 `4 + 12 = 16` 直接打架，
    站点还会把同一批成员摊两遍（父行的 composite 一张表 + 三行占位行）。

    成员清单的唯一出处是 `composites/<ref>.json`（§4.1），所以这些行只作**追溯用**：
    打 `is_member_row: <父字段名>`，从线长求和与包结构体里剔除，字段解剖表里仍保留并标注。
    判定要三道同时成立，避免误伤真负载：父行存在、父行带 `composite_ref`/`element_composite_ref`、
    尾巴名（最后一段 `.` 之后）确实是该 composite 的成员名（写 `*` 表示草稿没记下成员名，同样算）。
    """
    by_name = {f["name"]: f for f in cmd["fields"] if f.get("seq") != 0}
    out: list[str] = []
    for f in cmd["fields"]:
        if f.get("seq", 0) == 0 or f.get("is_closure") or f.get("is_member_row"):
            continue
        m = MEMBER_ROW_RE.match(f.get("name") or "")
        if not m:
            continue
        parent = by_name.get(m.group("parent"))
        if not parent:
            continue
        ref = parent.get("composite_ref") or parent.get("element_composite_ref")
        if not ref:
            continue
        # 尾巴写 `*`（`ms.*`）= 草稿自己也不知道成员名，只记「这里是父结构的成员」；
        # 成员清单由 composite 承载，这种行同样只作追溯，不能进线长求和。
        if m.group("member") != "*" and m.group("member") not in composite_member_names(ref):
            continue
        f["is_member_row"] = parent["name"]
        out.append(f"member_row_folded:{f['name']}(父 {parent['name']} = {ref}，成员已由 composite 展开)")
    return out


def fix_wire_len_after_member_rows(cmd: dict) -> list[str]:
    """成员占位行剔除后重算线长表达式（否则双计）。

    与 `fix_wire_len_for_elem_width_cells` 同一目的（让 `wire.length_expr` 等于真实线长），
    只是触发原因不同：这里是分母（占位行）多算，那里是数组项只写了元素线宽。两者可叠加，
    故统一按「payload 去掉成员行 → 每项按 `宽·条数`」重建（见 `rebuild_field_sum_len`）。
    """
    return rebuild_field_sum_len(cmd, "wire_len_member_rows_folded")


def strip_stale_unnamed_clause(cmd: dict) -> list[str]:
    """草稿写「内部成员未逐一命名（见 `notes.md`）」时，成员补齐后这句就成了**过期结论**。

    `protocol_analysis` 是只读输入，它写下这句话的时候确实还没下钻读取器，不算错；
    但现在 `composites/<ref>.json` 已有命名成员、站点又会在该字段下**就地展开成员表**，
    两句并排就是自相矛盾（口径：结构体一律摊平成员，不写「见 XXX」）。
    故导入期摘掉这句与 `notes.md` 指针，记 `stale_unnamed_clause_stripped:<字段>`。
    只在**该字段引用的 composite 确有命名成员**时摘；摘空了就原样保留（说明确实没成员可展）。
    """
    out: list[str] = []
    for f in cmd["fields"]:
        ref = f.get("composite_ref") or f.get("element_composite_ref")
        if not ref or not composite_member_names(ref):
            continue
        for key in ("purpose", "meaning"):
            text = f.get(key)
            if not text or "内部成员未逐一命名" not in text:
                continue
            new = UNNAMED_CLAUSE_RE.sub("", text).strip().strip("；;，,、 ").strip()
            if new and new != text:
                f[key] = new
                out.append(f"stale_unnamed_clause_stripped:{f['name']}")
    return out


def build_struct(cmd: dict) -> dict:
    """把 fields[] 的负载字段折成包结构体成员。

    定长 / 变长的判定口径（与 docs/01-命令模型.md §3.1 一致）：
    只有**长度列是纯数字**且 `元素宽 × 条数 == 长度` 时才算定长数组（无线上计数）；
    长度列是表达式（`54·n`、`4*A`）时是变长数组，必须给出 `count_field`。
    """
    fields = cmd["fields"]
    payload = [f for f in fields
               if f["seq"] >= 0 and f["seq"] != 0 and not f.get("is_closure") and not f.get("is_member_row")]
    members: list[dict] = []
    for idx, f in enumerate(payload):
        wt = f["wire_type"]
        length = f["length"]
        member: dict = {
            "name": go_name(f["name"], f"F{f['seq']}"),
            "wire_type": wt,
            "length": length,
            "field_ref": f["name"],
        }
        elem, tail, _ = parse_array(wt)
        if elem:
            # `array<elem 58>` 这类写法：元素无名，只有元素线长
            if elem == "elem" and tail and tail.isdigit():
                elem, tail, forced_elen = None, None, tail
            else:
                forced_elen = None
            member["wire_type"] = wt
            member["element"] = elem if (elem and elem != "struct") else None
            if member["element"] in composite_ids():
                member["element_composite_ref"] = member["element"]
            member["element_length"] = forced_elen or elem_length_of(length)
            member["cap"] = int(tail) if (tail and tail.isdigit()) else None
            if member["element_length"] is None and member["cap"] and PURE_INT_RE.match(length or ""):
                member["element_length"] = str(int(length) // member["cap"])
            if member["element"] in SCALAR_WIDTH and member["element_length"] is None:
                member["element_length"] = str(SCALAR_WIDTH[member["element"]])

            total = int(length) if PURE_INT_RE.match(length or "") else None
            elen = int(member["element_length"]) if member["element_length"] else None
            fixed = bool(total is not None and elen and member["cap"] and total == elen * member["cap"])
            if fixed:
                member["count_field"] = None
                member["count_field_source"] = "fixed"
            else:
                cand, src = guess_count_field(payload, idx, length)
                member["count_field"] = cand
                member["count_field_source"] = src
                if src == "nearest_scalar":
                    member["note"] = "计数字段为最近标量字段推断（未取证），须以 IDA 复核确认"
                elif src is None:
                    member["note"] = "未找到计数字段（须以 IDA 复核确认）"
            if member.get("note") is None:
                if not member["cap"] and tail:
                    member["count_var"] = tail
                    member["note"] = None
            members.append(member)
            continue
        if wt in {"struct", "bytes", "str", "string", "-", ""} or wt.startswith("struct"):
            sname = parse_struct_wt(wt)
            fixed_len = bool(PURE_INT_RE.match((length or "").strip()))
            member["element"] = sname or None
            member["element_length"] = length if fixed_len else None
            member["cap"] = None
            composite = resolve_composite_ref(f["name"], wt)
            if composite:
                member["composite_ref"] = composite
            if fixed_len:
                # 线长是字面量 ⇒ 该成员在报文里只出现一次（变长数组的线长必是表达式，见
                # docs/01-命令模型.md §3.1），不能拿邻近的计数字段当条数——否则站点会显示
                # 「条数 ← is_new」这种把无关字段当重复次数的假信息。
                member["count_field"] = None
                member["count_field_source"] = "fixed"
            elif wt in {"bytes", "str", "string"} or sname is None:
                cand, src = guess_count_field(payload, idx, length)
                member["count_field"] = cand
                member["count_field_source"] = src
            else:
                member["count_field"] = None
                member["count_field_source"] = None
            if composite:
                # 成员清单在 composites/<id>.json（唯一出处），站点就地展开，不写「见…」。
                member["members_source"] = "composite"
            elif wt in {"bytes", "str", "string"} or sname is None:
                member["note"] = "元素成员未建模（composites/ 无此结构），须以 IDA 复核补"
            else:
                member["note"] = None
        members.append(member)

    role = "response" if cmd["direction"] == "SC" else "request"
    go_struct = go_name(cmd["name"].replace("recv_", "").replace("send_", "") or cmd["proto"], "Msg")
    return {
        role: {
            "go_name": go_struct,
            "role": role,
            "wire_length": cmd["wire"]["length_expr"],
            "members": members,
        }
    }


# ------------------------------------------------------------------ 元信息归一

def dispatch_from_prose(prose: str) -> tuple[str | None, str | None]:
    """从 README 散文里取业务去向（`vt[槽]` + 调用点 VA）。

    只在 §1 表格格子里没有 `vt[...]` 时兜底 —— 那说明该命令的 README 用了
    「路径叙述」写法，真去向落在 §2 关键结论或 §3 的 `**去向**` 段里。常见句式：

      * `交 `vt[0x5A4]`（`0xB530F6`）`            —— 槽后括号**只有**调用点
      * `交 `vt[0x5A4]`（`0xB530ED` 取虚表项、`0xB530F6` 调用，实参即本值）`
                                                 —— 括号里有**多个** VA（取项 / 调用）
      * `⇒ `call vt[0x174](ent_id)`               —— 段尾箭头句，调用点须回段里找

    括号里多个 VA 时**取最后一个**（叙述顺序是「先取虚表项、再 call」）。这一点不必太较真：
    判定层对手向点的两种写法都认（`mov R,[H+NNNh]` 的 `mov_va` 与随后的 `call` 的 `va`），
    所以取项点或调用点都能对上。

    槽值超 `PROSE_MAX_SLOT` 或等于 `0x64` 报错槽的直接丢弃 —— 那些是对象成员/报错槽，
    不是去向（与判定层 `MAX_SLOT`/`ERROR_SLOT` 同口径）。
    """
    if not prose:
        return None, None
    # 坑㊱：**必须先剔掉元信息表格行**。表格里 `关联命令` / `配对命令` 格常写「同族退出类：…
    # `vt[0xE0]()`」，那是**别的命令**的去向。整篇扫会把它的 `vt[槽]()`（括号内为空，恰好
    # 命中下面 ① 的配对式）当成自己的去向 —— `SC-0x14C5` 的真去向是 `vt[0xAC]`，
    # 却因 `SC-0x0EC5` 的 `vt[0xE0]` 写在 `关联命令` 格而落了 `vt[0xE0]`。
    # 表格格子的去向另由 `meta_first(meta, "去向"…)` 处理，这一步只该看散文。
    prose = "\n".join(l for l in prose.splitlines() if not l.lstrip().startswith("|"))
    # ① 槽 + 紧随其后的括号（`vt[槽]`、`` `vt[槽]` ``、`vt[槽]（…）` 皆可；括号内可有多个 VA）
    pair = re.compile(r"vt\[(0x[0-9A-Fa-f]+)\][`'\"\s]*[（(]([^）)]*)[）)]")
    for m in pair.finditer(prose):
        slot = int(m.group(1), 16)
        if not (0 < slot <= PROSE_MAX_SLOT) or slot == PROSE_ERROR_SLOT:
            continue
        inner = vas(m.group(2))
        return f"vt[{m.group(1)}]", (inner[-1] if inner else None)
    # ② 段落写法：定位 `**去向**` 段，段内的 `vt[槽]` + 段内最后一个 VA
    for seg in re.split(r"\n\s*\n", prose):
        if not re.search(r"\*\*去向\*\*|去向\s*[:：]", seg):
            continue
        slots = [s for s in VT_RE.findall(seg)
                 if 0 < int(s, 16) <= PROSE_MAX_SLOT and int(s, 16) != PROSE_ERROR_SLOT]
        if not slots:
            continue
        seg_vas = vas(seg)
        return f"vt[{slots[-1]}]", (seg_vas[-1] if seg_vas else None)
    return None, None


def normalize_meta(cmd_id: str, meta: dict[str, str], prose: str | None = None) -> dict:
    parts = cmd_id.split("-", 3)
    direction, opcode, proto, name = parts[0], parts[1], parts[2], parts[3]

    block_cell = meta_first(meta, "处理块范围") or ""
    block_vas = vas(block_cell)
    block = block_vas[:2] if len(block_vas) >= 2 and block_vas[0] != block_vas[1] else None

    handler_cell = meta_first(meta, "处理函数", "代码位置") or ""
    handler_m = FUNC_RE.search(handler_cell)
    handler = handler_m.group(0) if handler_m else None
    handler_vas = vas(handler_cell)
    handler_va = handler_vas[0] if handler_vas else None
    if handler and not handler_va:
        # `sub_B51930` 自带的地址就是 VA（拿不到 @ 显式 VA 时按名字还原）
        m = re.fullmatch(r"sub_([0-9A-Fa-f]{5,8})", handler)
        if m:
            handler_va = "0x" + m.group(1)

    # 「名字串」行有几种写法：`<串>`、`<串>` @ `<址>`、`<串>`，引用点 `<址>`（早期批次）。
    # 只有前两种用 `@` 分隔，第三种要用「，引用点」切，否则整句会当成名字串显示。
    name_str_cell = meta_first(meta, "名字符串", "名字字符串") or ""
    name_txt = re.split(r"\s*@\s*|，\s*引用点|,\s*引用点", name_str_cell)[0]
    name_str = unquote_ticks(name_txt).strip() or None
    name_str_va = first_va(name_str_cell)
    ref_cell = meta_first(meta, "名字符串引用点", "名字串引用点") or ""
    if not name_str_va:
        name_str_va = first_va(ref_cell)

    cap_cell = meta_first(meta, "声明容量") or ""
    cap_vas = vas(cap_cell)
    # 坑㉞：容量数值不能从 `vt[...]` 槽位里抠。
    #   `| 声明容量（解码缓冲） | （无容量申请：块内无 `vt[0x78]` 分配器调用） |`
    #   旧写法直接 `re.search("0x...")`，把**分配器槽号** `0x78` 当成了容量落库，
    #   同一行明说「无容量申请」、模型里却出现 `capacity=0x78`。
    #   ⚠ 只剔 `vt[..]`，**不能**顺手剔地址：`VA_RE` 是 `0x`+4~9 位，会把 4 位以上的
    #     **容量本身**（`0x1004` / `0x9FC4` / `0xCA90` …）一起删掉，那是更坏的错。
    cap_probe = unquote_ticks(VT_RE.sub(" ", cap_cell)).strip()
    capacity = None
    if not NOCAP_RE.search(cap_probe):
        m = re.search(r"0x[0-9A-Fa-f]+", cap_probe)
        if m:
            capacity = m.group(0)
        else:
            m2 = re.search(r"\b(\d+)\b", cap_probe)
            capacity = m2.group(1) if m2 else None
    capacity_va = None
    for v in cap_vas:
        # `声明容量` 行有两种写法：`0x784`（`0xB864BB`）→ 两个 VA；`0x27`（`B23F9D`）→
        # 只有分配点一个（容量值 `0x27` 位数不够，不进 VA 正则）。所以取「第一个不是容量值本身」的 VA。
        if capacity and v.lower() == capacity.lower():
            continue
        capacity_va = v
        break
    if capacity_va is None:
        # 后续批次的 README 把「分配点」单列一行：`容量申请证据`（`push 0x000A` @ `0xB95896`）。
        # 这时 `声明容量` 行只有数值 —— 不补这一步 `capacity_va` 就是空的。
        cap_ev_cell = meta_first(meta, "容量申请证据", "容量旁证证据") or ""
        capacity_va = first_va(cap_ev_cell)

    dispatch_cell = meta_first(meta, "去向", "发送去向", "分发路径") or ""
    vt = VT_RE.findall(dispatch_cell)
    dispatch_slot = f"vt[{vt[-1]}]" if vt else None
    dispatch_vas = vas(dispatch_cell)
    dispatch_va = dispatch_vas[-1] if dispatch_vas else None
    if dispatch_slot is None and prose:
        # §1 的「分发路径 / 去向」格有两种写法：
        #   ① 直接给去向：`` `vt[0x1D4]` @ `0xB5B...` ``；
        #   ② **路径叙述**：列出分发器、默认分支、跳转表、调用点，末位才是块内 `cmp ax,<opcode>h`
        #      自检（`SC-0x20F5` 即此形）。
        # 写法②下「取最后一个 VA」会取到自检点，而**真去向写在 §3 散文**里
        # （`**去向**：… mov edx,[edx+174h] → push ecx ⇒ call vt[0x174](ent_id)`）。
        # 只扫表格的解析器读不到散文 ⇒ 去向被静默丢掉（全库 50 条，见 坑㉛）。
        # 这里补一层散文回填，并**同时覆盖写法②留下的错 VA**：自检点不是去向。
        slot, va = dispatch_from_prose(prose)
        if slot:
            dispatch_slot = slot
            dispatch_va = va

    closer_cell = meta_first(meta, "长度闭合点", "提交") or ""
    closer_va = first_va(closer_cell)

    write_cell = meta_first(meta, "opcode 写入证据", "opcode 写入/分发证据") or ""
    opcode_write_va = first_va(write_cell)

    pair_cell = meta_first(meta, "配对命令", "关联命令", "同族") or ""
    pairs = [p for p in CMD_ID_RE.findall(pair_cell) if p != cmd_id]

    notify_cell = meta_first(meta, "附加通知", "附加通知回调") or ""
    notify = first_va(notify_cell)

    err_cell = meta_first(meta, "错误码", "报错码") or ""
    err_vas = vas(err_cell)

    return {
        "direction": direction,
        "opcode": opcode.upper().replace("0X", "0x"),
        "proto": proto,
        "proto_name": name,
        "proto_class": unquote_ticks(meta_first(meta, "协议类") or "") or None,
        "block": block,
        "handler": handler,
        "handler_va": handler_va,
        "name_str": name_str,
        "name_str_va": name_str_va,
        "capacity": capacity,
        "capacity_va": capacity_va,
        "dispatch_slot": dispatch_slot,
        "dispatch_va": dispatch_va,
        "dispatch_raw": dispatch_cell or None,
        "closer_va": closer_va,
        "opcode_write_va": opcode_write_va,
        "notify_va": notify,
        "error_vas": err_vas,
        "pair_candidates": pairs,
        "dispatcher": unquote_ticks(meta_first(meta, "分发器") or "") or None,
    }


# ------------------------------------------------------------------ 派生能力（命名学，非证据）

def derive_capabilities(name: str) -> list[str]:
    n = name.lower()
    out: list[str] = []
    if re.search(r"(_get_r|_get|_list_init|_init_get_r|_search|_info_get|_select_r|_request)$", n):
        out.append("query")
    if re.search(r"(_notice|_notify|_update|_broadcast|_announce)", n):
        out.append("notify")
    if re.search(r"(_create|_add|_post|_entry|_new|_buy|_shop|_gacha)", n):
        out.append("create")
    if re.search(r"(_edit|_set|_store|_change|_apply|_rename|_unlock|_equip)", n):
        out.append("update")
    if re.search(r"(_delete|_del|_leave|_kick|_discard|_refuse|_cancel)", n):
        out.append("delete")
    if re.search(r"(_check|_verify|_validate|_auth|_probe)", n):
        out.append("validate")
    if re.search(r"(_begin|_end|_start|_stop|_enter|_exit|_suspend|_resume|_ready)", n):
        out.append("flow")
    if re.search(r"(_result|_settle|_reward|_ranking|_score)", n):
        out.append("settle")
    if re.search(r"(_chat|_msg|_mail|_board|_message)", n):
        out.append("communicate")
    if re.search(r"(_fire|_attack|_damage|_spawn|_snapshot|_battle|_combat|_weapon|_respawn|_hp)", n):
        out.append("battle")
    return sorted(set(out)) or ["unclassified"]


# ------------------------------------------------------------------ 单条命令

def build_command(cmd_dir: Path) -> tuple[dict, list[str]]:
    cmd_id = cmd_dir.name
    meta = read_meta(cmd_dir / "README.md")
    norm = normalize_meta(cmd_id, meta, (cmd_dir / "README.md").read_text(encoding="utf-8", errors="replace"))
    raw_rows, repairs = read_fields_csv(cmd_dir / "fields.csv")

    fields: list[dict] = []
    opcode_row = None
    closure_row = None
    seq = 0
    for row in raw_rows:
        if "闭合" in unquote_ticks(row["字段名"]):
            f = to_field(row, -1)
            closure_row = f
            fields.append(f)
            continue
        if unquote_ticks(row["字段名"]) == "opcode":
            f = to_field(row, 0)
            opcode_row = f
            fields.append(f)
            continue
        seq += 1
        f = to_field(row, seq)
        # 有的行把「含义/描述」写进了字段名格（尤其 `struct <名>` 行）：
        # 字段名必须是标识符，描述回流到含义，名字从线类型里取。
        if CJK_RE.search(f["name"]):
            desc = f["name"]
            f["meaning"] = desc if not f["meaning"] else f"{desc}；{f['meaning']}"
            derived = parse_struct_wt(f["wire_type"]) or parse_array(f["wire_type"])[0]
            if derived and derived != "struct" and not CJK_RE.search(derived):
                f["name"] = derived
            else:
                f["name"] = f"f_{f['offset']}"
            f["name_derived"] = True
        fields.append(f)

    # 线长表达式：优先闭合行的「偏移」列（SOP §5.3 的收口表达式）
    length_expr = closure_row["offset"] if closure_row is not None else ""
    length_source = "closure_row" if length_expr else None
    if not length_expr:
        # 退路①：把各负载字段的线长直接相加（保留变量名，得到 `4 + data_len` 这种表达式）
        terms = [
            f["length"] for f in fields
            if not f.get("is_closure") and f["seq"] != 0 and f["length"] and f["length"] != "-"
        ]
        if terms:
            length_expr = " + ".join(terms)
            length_source = "field_sum"
        elif not [f for f in fields if f["seq"] > 0 and not f.get("is_closure")]:
            # 零负载命令：只有 opcode，无任何字段（capacity == 2）
            length_expr = "0"
            length_source = "zero_load"
    if not length_expr:
        # 退路②：README §2 结论摘要里的「报文体线长 / 报文体总长」（必须是线长形态的串）
        text = (cmd_dir / "README.md").read_text(encoding="utf-8", errors="replace")
        m = re.search(r"##\s*2[^\n]*\n(.*?)(?=\n##\s)", text, re.S)
        blk = m.group(1) if m else text
        m = re.search(r"(?:报文体线长|报文体总长|负载线长|线长)\**\s*[:：]?\s*\**\s*`?([^`\n，,；;]+)", blk)
        if m and LEN_EXPR_RE.match(m.group(1).strip()) and re.search(r"\d", m.group(1)):
            length_expr = m.group(1).strip()
            length_source = "readme"
    if not length_expr:
        length_expr = "?"
        length_source = "unknown"
        repairs.append("length_expr_unknown")

    # README 的人读结论：留作复核交叉印证（§2 结论 / §4.2 长度闭合）
    readme_text = (cmd_dir / "README.md").read_text(encoding="utf-8", errors="replace")
    readme_conclusion = None
    m = re.search(r"##\s*2[^\n]*\n(.*?)(?=\n##\s)", readme_text, re.S)
    if m:
        for line in m.group(1).splitlines():
            s = line.strip().lstrip("-").strip()
            if s and not s.startswith(">") and not s.startswith("（与"):
                readme_conclusion = unquote_ticks(s)[:300]
                break
    readme_close = None
    m = re.search(r"长度闭合\**\s*\n+((?:[^\n]*\n){0,3}?)(?=\n#|\Z)", readme_text)
    if m:
        for line in m.group(1).splitlines():
            s = line.strip().lstrip("-").strip()
            if s:
                readme_close = unquote_ticks(s)[:300]
                break

    drivers = sorted({t for t in VAR_TOKEN_RE.findall(length_expr) if not t.isdigit()} - {"L", "Len", "var"})
    if "L" in length_expr or "Len" in length_expr:
        drivers.append("L")

    payload_fields = [f for f in fields if f["seq"] >= 0 and f["seq"] != 0 and not f.get("is_closure")]

    cmd: dict = {
        "id": cmd_id,
        "opcode": norm["opcode"],
        "direction": norm["direction"],
        "proto": norm["proto"],
        "proto_class": norm["proto_class"],
        "name": norm["proto_name"],
        "source_dir": f"protocol_analysis/commands/{cmd_id}",
        "meta": meta,
        "handler": norm["handler"],
        "handler_va": norm["handler_va"],
        "block": norm["block"],
        "name_str": norm["name_str"],
        "name_str_va": norm["name_str_va"],
        "capacity": norm["capacity"],
        "capacity_va": norm["capacity_va"],
        "closer_va": norm["closer_va"],
        "dispatch": norm["dispatch_raw"],
        "dispatch_slot": norm["dispatch_slot"],
        "dispatch_va": norm["dispatch_va"],
        "wire": {
            "length_expr": length_expr,
            "fixed": bool(FIXED_EXPR_RE.match((length_expr or "").strip())),
            "var_drivers": drivers,
            "capacity_note": norm["capacity"] and f"声明容量 {norm['capacity']}（容量记账口径，非线长）",
            "field_count": len(payload_fields),
            "length_source": length_source,
            "readme_conclusion": readme_conclusion,
            "readme_close": readme_close,
        },
        "fields": fields,
        "behavior": [],
        "capabilities": [],
        "capabilities_derived": derive_capabilities(norm["proto_name"]),
        "db_effects": [],
        "pair": norm["pair_candidates"][0] if norm["pair_candidates"] else None,
        "related": norm["pair_candidates"][1:],
        "asm_verification": {
            "status": "IMPORTED",
            "verified_at": None,
            "batch": None,
            "extractor": None,
            "checks": {
                "capacity": None,
                "field_window": None,
                "primitive_widths": None,
                "closer": None,
                "dispatch_slot": None,
                "log_strings": None,
            },
            "mismatches": [],
            "evidence_file": None,
        },
        "extra": {
            "opcode_write_va": norm["opcode_write_va"],
            "notify_va": norm["notify_va"],
            "error_vas": norm["error_vas"],
            "dispatcher": norm["dispatcher"],
            "closure_field": closure_row["name"] if closure_row else None,
            "opcode_field_va": opcode_row["evidence_va"] if opcode_row else [],
        },
    }
    override = load_override(cmd_id)
    if override:
        repairs.extend(apply_field_override(cmd, override))

    # 聚合字段挂 composites/<id>.json 引用：成员清单不在本层复制，站点/代码生成就地展开。
    for fi, f in enumerate(cmd["fields"]):
        if f.get("is_closure") or f.get("seq") == 0:
            continue
        wt = f.get("wire_type") or ""
        length_expr = f.get("length") or ""
        ref = resolve_composite_ref(f.get("name", ""), wt)
        if not ref:
            continue
        if wt.startswith("array<"):
            name = f.get("name")
            parts = wt[len("array<"):-1].split(",", 1)
            tail_num = parts[1].strip() if len(parts) > 1 else ""
            if not ref_matches_elem_width(ref, length_expr, wt):
                # 同名不同体：先按元素线宽（日志成员名作旁证）重挂，再退到「摘除引用」。
                width = elem_width_of(length_expr, wt)
                if width is None and not tail_num and PURE_INT_RE.match(length_expr.strip()):
                    # `array<ms>` + 长度 `401`：条数没写进长度列时，纯数字是**元素线宽**（不是总长，
                    # 总长由 override 补成 `宽·count`）。据此重挂到同线宽的 composite——
                    # 这正是「同名不同体」的又一种形态：`ms`（battle 244B）vs `ms_rokaku`（络格 401B）。
                    width = int(length_expr.strip())
                hint = log_template_members(f.get("meaning") or "", f.get("purpose") or "")
                alt, cands = pick_ref_by_width(width, hint)
                if alt and alt != ref:
                    repairs.append(f"elem_ref_rebound:{name}({ref} → {alt}；元素线宽 {width})")
                    f["element_composite_ref_source"] = "width"
                    ref = alt
                elif width is None:
                    # 长度列拆不出条数×元素宽（纯数字且无条数、或表达式很怪）：
                    # 名字对得上就留着，但把两个数都摆出来，标成待核。
                    f["element_composite_ref"] = ref
                    f["element_composite_warning"] = (
                        f"长度列 `{length_expr}` 拆不出条数×元素宽，暂按名字挂 `{ref}`"
                        f"（线长 {composite_lengths().get(ref)}），两数不符处待 IDA 核。"
                    )
                    repairs.append(f"elem_ref_unchecked:{name}({ref} @ {length_expr})")
                    continue
                else:
                    repairs.append(
                        f"elem_ref_mismatch:{name}(草稿挂 {ref} 线长 {composite_lengths().get(ref)}"
                        f" ≠ 长度列 {length_expr}）"
                    )
                    f["element_composite_ref"] = None
                    f["element_composite_note"] = (
                        f"按名字挂到 `{ref}`（线长 {composite_lengths().get(ref)}）与长度列 `{length_expr}` 不符，"
                        f"已摘除引用并置为未建模（候选：{('、'.join(cands) or '无，同线宽 composite 不存在')}）："
                        "同名不同体，须进 IDA 下钻元素读取器再建 composite。"
                    )
                    continue
            tok = array_count_token(length_expr, tail_num)
            elem_head = array_elem_name(wt)
            # 只规范「匿名元素」（`array<struct,84>` / `array<elem 58>`）：草稿把元素宽或槽步进写进了
            # 元素名，条数得从长度列取；已写好元素名但尾巴是槽步进的（`array<item_list,24>`）同样规范。
            stale_tail = elem_head in {"struct", "elem"} or (
                tail_num.isdigit() and composite_lengths().get(ref) != int(tail_num)
            )
            if stale_tail and wt != f"array<{ref},{tok}>":
                f["wire_type_draft"] = wt
                f["wire_type"] = f"array<{ref},{tok}>"
                repairs.append(f"elem_wt_normalized:{name}({wt} → {f['wire_type']})")
            if not f.get("element_composite_ref_source"):
                f["element_composite_ref_source"] = "name"
            f["element_composite_ref"] = ref
            # 长度列只写了**元素线宽**、条数另有线上字段（§3.1 要求写 `宽·条数`）：
            # 这是长度列的记账坑，不是元素建模问题——标出来，别让站点把 `113` 当成总长。
            lit = length_expr.strip()
            if (not tail_num and PURE_INT_RE.match(lit)
                    and composite_lengths().get(ref) == int(lit)):
                cnt, cnt_src = guess_count_field(cmd["fields"], fi, length_expr)
                if cnt and cnt_src in {"length_expr", "heuristic"}:
                    f["length_is_elem_width"] = cnt
                    repairs.append(f"len_is_elem_width:{name}({lit} → {lit}·{cnt})")
        elif wt.startswith("struct"):
            f["composite_ref"] = ref

    # 三类「长度列不是线长」的改写必须先于成员占位行折叠：它们改的是单个字段的字节数，
    # 折叠改的是「哪些行参与求和」，顺序反了会把新字节数漏进上一轮的表达式里。
    repairs.extend(fix_slot_budget_str_lengths(cmd))
    repairs.extend(fix_struct_span_lengths(cmd))
    repairs.extend(fix_literal_count_array_lengths(cmd))
    repairs.extend(fix_scalar_array_var_count_lengths(cmd))
    repairs.extend(mark_member_rows(cmd))
    repairs.extend(strip_stale_unnamed_clause(cmd))
    repairs.extend(fix_wire_len_after_member_rows(cmd))
    repairs.extend(fix_wire_len_for_elem_width_cells(cmd))
    cmd["structs"] = build_struct(cmd)
    # 指纹必须最后算：它要覆盖上面所有长度改写（含三类新修与成员行折叠）后的最终字节数。
    cmd["wire_fingerprint"] = wire_fingerprint(cmd)
    cmd["check_fingerprint"] = check_fingerprint(cmd)
    if repairs:
        cmd["import_repairs"] = repairs
    return cmd, repairs


# ------------------------------------------------------------------ 人工复核覆盖

def load_override(cmd_id: str) -> dict | None:
    """读 `schema/commands/_overrides/<CMD-id>.json`（人工复核结论）。"""
    path = OVERRIDE_DIR / f"{cmd_id}.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _override_field(entry: dict) -> dict:
    f = {
        "seq": -1,
        "offset": "?",
        "length": "?",
        "wire_type": "?",
        "name": entry["name"],
        "meaning": "",
        "purpose": "",
        "enum": None,
        "evidence_va": ["?"],
        "confidence": "?",
        "disposition": "TBD",
        "entity_ref": None,
        "csv_line": None,
        "override_verified": True,
    }
    f.update(entry)
    return f


def apply_field_override(cmd: dict, ov: dict) -> list[str]:
    """把人工复核结论覆盖到 `fields[]` / `wire` 上（在 `build_struct` 之前调用）。

    只认 `drop`（删行）/ `patch`（改行）/ `add`（补行，可带 `after` 定位）/
    `wire_length_expr`。每条改动都必须带 IDA 证据 VA，写在覆写文件的 `evidence[]`。
    """
    notes: list[str] = []
    fields: list[dict] = cmd["fields"]

    drop = {n for n in (ov.get("drop") or []) if isinstance(n, str)}
    if drop:
        # 既支持精确名字，也支持通配（`news.*` / `roominfo.*` / `clan_*.*`），
        # 便于一次性删掉某个结构的「成员占位行」——成员改由 composites 承载。
        def _dropped(name: str) -> bool:
            return name in drop or any(fnmatch.fnmatchcase(name, pat) for pat in drop if "*" in pat)

        kept = [f for f in fields if not _dropped(f.get("name") or "")]
        notes.append(f"override_drop:{len(fields) - len(kept)}")
        fields = kept
        cmd["fields"] = fields

    patch = ov.get("patch") or {}
    hit = 0
    for f in fields:
        p = patch.get(f.get("name"))
        if not isinstance(p, dict):
            continue
        for k, v in p.items():
            f[k] = v
        f["override_verified"] = True
        hit += 1
    if hit:
        notes.append(f"override_patch:{hit}")

    add = 0
    for entry in ov.get("add") or []:
        if not isinstance(entry, dict) or not entry.get("name"):
            continue
        if any(f.get("name") == entry["name"] for f in fields):
            continue
        new_field = _override_field(entry)
        # `after` / `before` 都是**定位锚**：补「父结构行」时通常要插在它的成员占位行**之前**
        # （`before: "<父>.<第一个成员>"`），否则父行会落到成员后面、线序读起来是倒的。
        anchor_name = entry.get("before") or entry.get("after")
        at = None
        if anchor_name:
            at = next((i for i, f in enumerate(fields) if f.get("name") == anchor_name), None)
        if at is None:
            at = len([f for f in fields if not f.get("is_closure")])
        elif entry.get("before"):
            at -= 1
        fields.insert(at + 1, new_field)
        add += 1
    if add:
        notes.append(f"override_add:{add}")

    # 线序重排：opcode=0、闭合=-1、其余按列表次序
    seq = 0
    for f in fields:
        if f.get("is_closure"):
            f["seq"] = -1
        elif f.get("name") == "opcode":
            f["seq"] = 0
        else:
            seq += 1
            f["seq"] = seq

    payload = [f for f in fields if f["seq"] > 0 and not f.get("is_closure")]
    cmd["wire"]["field_count"] = len(payload)
    if ov.get("wire_length_expr"):
        cmd["wire"]["length_expr"] = ov["wire_length_expr"]
        cmd["wire"]["fixed"] = bool(FIXED_EXPR_RE.match(ov["wire_length_expr"].strip()))
        cmd["wire"]["var_drivers"] = sorted({
            t for t in VAR_TOKEN_RE.findall(ov["wire_length_expr"]) if not t.isdigit()
        } - {"L", "Len", "var"})
        cmd["wire"]["length_source"] = "override"
    if ov.get("wire_note"):
        cmd["wire"]["override_note"] = ov["wire_note"]
    notes.extend(apply_meta_override(cmd, ov))
    cmd["field_override"] = {
        "revision": ov.get("revision"),
        "verified_at": ov.get("verified_at"),
        "reason": ov.get("reason"),
        "evidence_file": f"schema/commands/_overrides/{cmd['id']}.json",
        # 显式钉住的元字段（`meta` 里认账的那几个）。`merge_previous` 要靠它区分
        # 「人写覆写把容量定成空」与「README 根本没写容量」——前者不可被旧值复活。
        "meta_keys": sorted(k for k in (ov.get("meta") or {}) if k in META_OVERRIDE_KEYS),
        "notes": notes,
    }
    return notes


# 覆盖层可改的**元字段**（都不是线长量，改它们不会动 `wire_fingerprint`）
META_OVERRIDE_KEYS = ("capacity", "capacity_va", "closer_va", "dispatch_slot", "dispatch_va",
                      "handler_va", "opcode_write_va", "notify_va", "name_str_va", "block")


def apply_meta_override(cmd: dict, ov: dict) -> list[str]:
    """`meta`：覆盖 README 元信息里的**具体地址/槽位**（人工复核结论）。

    只用于「README 记的地址本身错了」这种情形（区别于 §8.1 的等价记法：那是同一个点的
    另一种写法，属判定层认账；这里是把**指错点**的结论改对）。
    例：`SC-0x6FF7` 的「长度闭合点」写成了闭合校验**失败后**的 `vt[0x64]` 报错调用点，
    真闭合点在 `cmp <游标>,<末尾>` 处 —— 这类必须改模型，不能在判定层再认一种「记法」。
    """
    meta = ov.get("meta")
    if not isinstance(meta, dict) or not meta:
        return []
    notes: list[str] = []
    for k, v in meta.items():
        if k not in META_OVERRIDE_KEYS:
            notes.append(f"override_meta_ignored:{k}")
            continue
        old = cmd.get(k)
        if old == v:
            continue
        cmd[k] = v
        notes.append(f"override_meta:{k} {old} → {v}")
    return notes


# ------------------------------------------------------------------ 合并（幂等）

def merge_previous(new: dict, old: dict | None) -> dict:
    if not isinstance(old, dict):
        return new
    # 人工复核覆盖改了字段口径（revision 变化）⇒ 旧汇编复核结论作废，必须重跑
    rev_changed = (
        (new.get("field_override") or {}).get("revision")
        != (old.get("field_override") or {}).get("revision")
    )
    # 导入规则改了字段字节数（槽位预算/内存跨度/字面量条数三类改写）⇒ 同样作废。
    # 复核结论认的是「这些字段就是这个宽度」，字节数一变，旧结论就不再是对这份模型的结论；
    # 沿用等于拿旧口径的章给新模型背书。指纹只覆盖线长相关量，改 `meaning` 不会触发。
    #
    # 旧文件没有 `wire_fingerprint`（本键是后加的）时按**不能证明未变**处理 —— 缺失即作废。
    # 首轮会因此把全部已复核命令打回 `IMPORTED`，这是有意的：那些结论是在旧长度口径下得的，
    # 而原始切片都留在 `_verify/_raw/` 里，重跑 `ingest --batch N`（不必回 IDA）即可在新口径下重判。
    old_fp = old.get("wire_fingerprint")
    new_fp = new.get("wire_fingerprint")
    fp_changed = old_fp != new_fp
    old_status = (old.get("asm_verification") or {}).get("status")
    verified = bool(old_status) and old_status != "IMPORTED"
    # 坑㉟：复核器回填的点位字段是**汇编结论**，本脚本只能从 README 表行/CSV 推导 ——
    # README 没写该行（或写在散文里）时本脚本推不出来，照旧写回就等于把复核器辛苦回填的
    # 值冲成空。实测：`SC-0x00C7` 的容量 `0xC`（汇编 `push 0Ch` @ `0xB51CB1`）被冲成 `None`，
    # 而 `checks.capacity` 里那份结论还在，模型与自己的复核存根互相矛盾。
    # 口径与全库一致：**只补不覆盖**（同 `behavior`/`asm_verification`）——旧模型有值就沿用，
    # 想改这些点必须走 `_overrides/` 的 `meta`（`meta_keys` 里显式钉住的键以覆写为准，
    # 否则 `SC-0xD94A` 这种「README 明说无容量、却被旧值复活」的情况无法纠正）。
    if verified:
        pinned = set((new.get("field_override") or {}).get("meta_keys") or [])
        touched = False
        for key in POINT_FIELDS:
            if key in pinned or old.get(key) in (None, "", []):
                continue
            if new.get(key) != old.get(key):
                new[key] = old[key]
                touched = True
        if touched:
            # `wire.capacity_note` 是 `capacity` 的同义呈现（站上两条并排显示），必须一起改，
            # 否则会出现「容量 0xC」与「未声明容量」并存。
            w = new.get("wire")
            if isinstance(w, dict):
                if new.get("capacity"):
                    w["capacity_note"] = f"声明容量 {new['capacity']}（容量记账口径，非线长）"
                else:
                    w.pop("capacity_note", None)
            # `check_fingerprint` 覆盖上面这些键：沿用后必须重算，否则存根声明的输入
            # 与实际模型不符 —— 下次复核会拿一个错误的输入指纹去比，判定的前提就没了。
            new["check_fingerprint"] = check_fingerprint(new)
    old_cfp = old.get("check_fingerprint")
    new_cfp = new.get("check_fingerprint")
    cfp_changed = old_cfp != new_cfp
    if verified and not rev_changed and not fp_changed and not cfp_changed:
        new["asm_verification"] = old["asm_verification"]
    elif verified and not rev_changed:
        if old_cfp and cfp_changed and not fp_changed:
            new["asm_verification"]["invalidated_by"] = f"check_fingerprint_changed:{old_cfp} → {new_cfp}"
        elif old_fp:
            new["asm_verification"]["invalidated_by"] = f"wire_fingerprint_changed:{old_fp} → {new_fp}"
        else:
            new["asm_verification"]["invalidated_by"] = (
                f"wire_fingerprint_absent(旧模型无此键，无法证明字节数未变；新指纹 {new_fp})"
            )
    for key in ("behavior", "capabilities", "db_effects"):
        if old.get(key):
            new[key] = old[key]
    # 结构体：人工补过成员语义（note/name 非自动）就保留
    if old.get("structs") and old.get("structs_manual") is True:
        new["structs"] = old["structs"]
    # 字段级人工修订：disposition / entity_ref / meaning 覆写
    old_fields = {f.get("name"): f for f in old.get("fields", []) if isinstance(f, dict)}
    for f in new["fields"]:
        prev = old_fields.get(f["name"])
        if not prev:
            continue
        if prev.get("disposition") and prev["disposition"] != "TBD":
            f["disposition"] = prev["disposition"]
        if prev.get("entity_ref"):
            f["entity_ref"] = prev["entity_ref"]
        if prev.get("meaning_verified"):
            f["meaning"] = prev["meaning"]
            f["meaning_verified"] = True
            f["is_closure"] = f.get("is_closure", False) or prev.get("is_closure", False)
    return new


# ------------------------------------------------------------------ main

def main() -> int:
    # Windows 控制台默认 GBK：修复备注里有 `₁`/`→` 这类字符时，末行统计的 print 会抛
    # UnicodeEncodeError —— 文件其实已全部落盘，却让整个脚本以非 0 退出，掩盖真实失败。
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if not PROTO_COMMANDS.is_dir():
        print(f"找不到 {PROTO_COMMANDS}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    repair_counter: Counter[str] = Counter()
    repaired_commands: list[str] = []
    commands: list[dict] = []
    status_counter: Counter[str] = Counter()
    dir_counter: Counter[str] = Counter()
    proto_counter: Counter[str] = Counter()
    cap_counter: Counter[str] = Counter()

    for cmd_dir in sorted(p for p in PROTO_COMMANDS.iterdir() if p.is_dir()):
        if not (cmd_dir / "fields.csv").is_file():
            continue
        cmd, repairs = build_command(cmd_dir)
        out_path = OUT_DIR / f"{cmd['id']}.json"
        old = None
        if out_path.is_file():
            try:
                old = json.loads(out_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                old = None
        cmd = merge_previous(cmd, old)
        out_path.write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        commands.append(cmd)
        status_counter[cmd["asm_verification"]["status"]] += 1
        dir_counter[cmd["direction"]] += 1
        proto_counter[cmd["proto"]] += 1
        for c in cmd.get("capabilities") or cmd.get("capabilities_derived") or []:
            cap_counter[c] += 1
        if repairs:
            repaired_commands.append(cmd["id"])
            for r in repairs:
                repair_counter[r.split(":", 1)[-1]] += 1

    # 同 opcode 反向 / 跨协议类：补 pair / related
    by_opcode: dict[str, list[dict]] = defaultdict(list)
    for c in commands:
        by_opcode[c["opcode"]].append(c)
    for opcode, group in by_opcode.items():
        if len(group) < 2:
            continue
        for c in group:
            others = [o for o in group if o["id"] != c["id"]]
            opposite = [o for o in others if o["direction"] != c["direction"]]
            if opposite and not c.get("pair"):
                c["pair"] = opposite[0]["id"]
            rel = {o["id"] for o in others if o["proto"] != c["proto"] or o["direction"] == c["direction"]}
            c["related"] = sorted(set(c.get("related") or []) | rel)

    # 重写一遍（pair/related 是全局推导，必须回写）
    for c in commands:
        (OUT_DIR / f"{c['id']}.json").write_text(
            json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    field_total = sum(len([f for f in c["fields"] if not f.get("is_closure") and f["seq"] != 0]) for c in commands)
    needs_review = sum(1 for c in commands for f in c["fields"] if f.get("needs_review"))
    review_commands = sorted({c["id"] for c in commands for f in c["fields"] if f.get("needs_review")})
    length_source_counter = Counter(c["wire"].get("length_source") for c in commands)
    # 坑㉟ 的索引面（同因同果）：`index.json` 是**三个写者共用**的文件 —— 本脚本写命令门面，
    # `derive_behavior.py` 写 `db_effects`/`behavior_steps`/`capabilities_evidence` 与
    # `counts.commands_with_db_effects`，`verify_commands_ida.py` 写 `asm_mismatches`。
    # 整份重写会把另外两家的键悄悄抹掉：实测重跑一次导入，`已映射 DB 影响` 从 81 掉到 0
    # （模型里 `db_effects` 好好地在，只是索引那一格没了）。所以**只覆盖自己产出的键**，
    # 旧索引里认不出的键一律原样沿用（顶层与逐条两级都要）。
    old_index: dict = {}
    if INDEX_PATH.is_file():
        try:
            old_index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            old_index = {}
    old_entries = {e.get("id"): e for e in old_index.get("commands", []) if isinstance(e, dict)}
    OWN_ENTRY_KEYS = {
        "id", "opcode", "direction", "proto", "name", "wire_length", "length_source",
        "fixed", "field_count", "status", "capacity", "closer_va", "dispatch_slot",
        "pair", "capabilities", "capabilities_derived", "struct_go_name", "struct_role",
    }

    def _entry(c: dict) -> dict:
        e = {
            "id": c["id"],
            "opcode": c["opcode"],
            "direction": c["direction"],
            "proto": c["proto"],
            "name": c["name"],
            "wire_length": c["wire"]["length_expr"],
            "length_source": c["wire"].get("length_source"),
            "fixed": c["wire"]["fixed"],
            "field_count": c["wire"]["field_count"],
            "status": c["asm_verification"]["status"],
            "capacity": c["capacity"],
            "closer_va": c["closer_va"],
            "dispatch_slot": c["dispatch_slot"],
            "pair": c.get("pair"),
            "capabilities": c.get("capabilities") or [],
            "capabilities_derived": c.get("capabilities_derived") or [],
            "struct_go_name": next(iter(c["structs"].values()))["go_name"] if c.get("structs") else None,
            "struct_role": next(iter(c["structs"])) if c.get("structs") else None,
        }
        for k, v in (old_entries.get(c["id"]) or {}).items():
            if k not in OWN_ENTRY_KEYS:
                e[k] = v
        return e

    counts = dict(old_index.get("counts") or {})
    counts.update({
        "commands": len(commands),
        "fields": field_total,
        "by_direction": dict(sorted(dir_counter.items())),
        "by_proto": dict(sorted(proto_counter.items())),
        "by_status": dict(sorted(status_counter.items())),
        "by_capability": dict(sorted(cap_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "by_length_source": dict(sorted(length_source_counter.items(), key=lambda kv: (-kv[1], str(kv[0])))),
        "csv_repaired_commands": len(repaired_commands),
        "fields_needing_review": needs_review,
        "commands_needing_review": len(review_commands),
    })
    index = dict(old_index)
    index.update({
        "generated": TODAY,
        "source": "../protocol_analysis/commands",
        "schema": "_schema.json",
        "model_doc": "../docs/01-命令模型.md",
        "counts": counts,
        "repairs": dict(sorted(repair_counter.items(), key=lambda kv: (-kv[1], kv[0]))),
        "fields_needing_review": [
            {"command": c["id"], "seq": f["seq"], "name": f["name"], "csv_line": f.get("csv_line"),
             "csv_raw_cols": f.get("csv_raw_cols")}
            for c in commands for f in c["fields"] if f.get("needs_review")
        ],
        "commands": [_entry(c) for c in commands],
    })
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"导入命令 {len(commands)} 条 / 字段 {field_total} 条")
    print(f"  方向 {dict(sorted(dir_counter.items()))}")
    print(f"  协议类 {dict(sorted(proto_counter.items()))}")
    print(f"  状态 {dict(sorted(status_counter.items()))}")
    print(f"  CSV 修复过的命令 {len(repaired_commands)} 条；修复类型 {dict(repair_counter)}")
    print(f"  CSV 畸形行还原出的字段（待 ASM 复核）{needs_review} 条 / 涉及 {len(review_commands)} 条命令")
    print(f"  索引 {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

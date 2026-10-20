#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_commands_ida.py —— 交互命令模型的 **IDA 汇编复核器**（批次化）。

口径唯一来源：`db_design/docs/01-命令模型.md`；
IDA 汇编是类型与去向的**唯一权威**（伪代码只用于导航）。

流水线（四步，跨 IDA 与本地两端）
--------------------------------
    python tools/verify_commands_ida.py plan   --batch 1 [--size 50] [--proto ...] [--only ID...]
    python tools/verify_commands_ida.py emit   --batch 1
        → 写 schema/commands/_meta/_verify_job.json
        → 在 IDA 里执行 tools/ida_verify_batch.py（IDA MCP 的 py_exec_file）
        → 产出 schema/commands/_verify/_raw/<ID>.json（原始证据切片）
    python tools/verify_commands_ida.py ingest --batch 1 [--apply]
    python tools/verify_commands_ida.py status

六项复核（全部带 VA，写回 `asm_verification.checks`）
----------------------------------------------------
    1. capacity         容量指纹：`mov R,[H+78h]` 分配器槽 + 紧随 `push IMM; call R`
    2. field_window     字段窗口：按协议类守卫（battle `sub_B05DA0` / lounge `sub_B41120` /
                        auth `sub_B02C90`）到闭合点/收尾
    3. primitive_widths 逐字段读写原语宽度序列（与 `fields[].wire_type` 贪心对位）
    4. closer           闭合点（`cmp <游标>,<末尾>` + `jz/je` **或** `jnz/jne`；C→S 为提交/发送）
    5. dispatch_slot    去向虚表槽 + 实参个数（以「分支/调用」为边界向前清点 push）
    6. log_strings      块内日志串（`xxx=` / `xxx={` 与字段名对位）

已知坑（全部来自 `protocol_analysis/_meta/长期记忆.md`，抽取规则必须绕开）
--------------------------------------------------------------------
* 第 ⑲ 坑：IDA 行尾 ASCII 注释（`push 4Ch ; char`）—— IDA 侧已剥离。
* 容量指纹四约束：① 只认 `[X+78h]` 分配器（守卫的 `push 0xCAh` 是模块 id）；
  ② 寄存器不一定是 `edx`；③ 行尾注释；④ 立即数须同时接受 `h` 后缀与十进制。
* `vt[0x78]` 双宿主：分配器读 `[X+0Ch]` 的 `vt[0x78]`、业务去向读 `[X]` 的 `vt[0x78]`。
* 第 ② 条：闭合点 `jz` 与 `jnz` 都要认（成功分支可能落在跳转上）。
* `vt[0x64]` 是报错槽，不是业务去向。
* 复合读取器消费量必须**整函数扫描 + 循环展开**；本工具只在「无回跳」时才给数字。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # db_design/
SCHEMA = ROOT / "schema"
CMD_DIR = SCHEMA / "commands"
META_DIR = CMD_DIR / "_meta"
VERIFY_DIR = CMD_DIR / "_verify"
RAW_DIR = VERIFY_DIR / "_raw"
JOB_PATH = META_DIR / "_verify_job.json"

# 回填改了判定输入就重算 `check_fingerprint`，口径必须与导入层**同一份实现**——
# 复制一份迟早会漂移。导入层有 `__main__` 守卫，可安全导入。
sys.path.insert(0, str(Path(__file__).resolve().parent))
from import_commands import check_fingerprint as _recompute_check_fingerprint  # noqa: E402

EXTRACTOR = "tools/verify_commands_ida.py"
IDA_SCRIPT = "db_design/tools/ida_verify_batch.py"

# ---------------------------------------------------------------- 汇编常量表

# 读原语（游标 = {cur@+0, end@+4}）；宽度以「原语自身游标步进」为准
PRIM_READ = {
    0xB02DD0: "u32",
    0xB02DF0: "u16",
    0xB06230: "u8",
    0xB06200: "u64",
    0xB06250: "f32",
    0xB06270: "f64",
    0xB02BA0: "str",     # NUL 结尾串，长度 = 串长 + 1
}
# 写原语（C→S）
PRIM_WRITE = {
    0xB02D80: "u32",
    0xB02DA0: "u16",
    0xB061C0: "u8",
    0xB06190: "u64",
    0xB061E0: "f32",
    0xB02B40: "str",     # NUL 结尾串，maxlen 即槽预算
}
# 守卫 / 收尾（按协议类不同，批次-7 固化；auth 无收尾函数）
GUARD = {
    "battle": (0xB05DA0, 0xB05D90),
    "lounge": (0xB41120, 0xB41110),
    "auth": (0xB02C90, None),
}
COMMIT = 0xB02FF0        # C→S 提交/发送（第 ㉑ 坑：不是绝对判据）
CURSOR_INIT = 0xABB2F0   # 用传输层缓冲初始化 {cur,end}
CURSOR_RESET = 0xCA0CE0  # 复位临时游标/结构
MEMCPY = 0xCC56B0        # 串拷贝（blob 判据）
ERROR_SLOT = 0x64        # vt[0x64](1, 错误码) —— 报错槽，不是业务去向
# 虚表槽值上限：槽都在低偏移；`[X+2C5Ch]`/`[X+79A8h]` 是对象成员/通知回调，不是去向槽
MAX_SLOT = 0x1000

WIDTH_OF_TYPE = {"u8": 1, "i8": 1, "char": 1, "bool": 1, "u16": 2, "i16": 2,
                 "u32": 4, "i32": 4, "u64": 8, "i64": 8, "f32": 4, "f64": 8}

# 寄存器名 → 宽度（内联写线宽度按源寄存器/内存前缀判定）
REG_WIDTH = {}
for _n in ("al", "ah", "bl", "bh", "cl", "ch", "dl", "dh"):
    REG_WIDTH[_n] = 1
for _r in ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp"):
    REG_WIDTH[_r] = 2
for _n in ("eax", "ebx", "ecx", "edx", "esi", "edi", "ebp", "esp"):
    REG_WIDTH[_n] = 4
for _n in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"):
    REG_WIDTH[_n] = 8


def reg_width(name: str | None) -> int | None:
    if not name:
        return None
    return REG_WIDTH.get(str(name).strip().lower().split(".")[0])

# 不改标志位：允许出现在 cmp 与 jcc 之间
NS_MNEM = frozenset({"mov", "movzx", "movsx", "lea", "push", "pop", "nop", "xchg",
                     "movsd", "movss", "movdqu", "movaps", "movups", "prefetchnta"})
JCC = frozenset({"jg", "ja", "jge", "jae", "jl", "jb", "jle", "jbe",
                 "jz", "je", "jnz", "jne"})
JZ = frozenset({"jz", "je"})
JNZ = frozenset({"jnz", "jne"})

O_REG, O_MEM, O_PHRASE, O_DISPL, O_IMM, O_NEAR, O_FAR = 1, 2, 4, 3, 5, 7, 8


# ---------------------------------------------------------------- 基础读取

def load_json(path: Path):
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=1)


def as_int(v) -> int | None:
    """`0x784` / `784h` / `1924` / `?` → int（第 ⑲ 坑：两种立即数写法都要认）。"""
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip().strip("`").replace("`", "").strip()
    s = re.sub(r"\s*\(.*$", "", s).strip()
    if not s or s in ("?", "-", "—"):
        return None
    m = re.match(r"^(0[xX][0-9A-Fa-f]+|[0-9A-Fa-f]+[hH]|[0-9]+)$", s)
    if not m:
        # 形如 `0x784（容量记账…）`：取最前面的数字 token
        m2 = re.search(r"0[xX][0-9A-Fa-f]+|[0-9A-Fa-f]+[hH]|[0-9]+", s)
        if not m2:
            return None
        s = m2.group(0)
    if s.lower().startswith("0x"):
        return int(s, 16)
    if s.lower().endswith("h"):
        return int(s[:-1], 16)
    try:
        return int(s, 10)
    except ValueError:
        return None


def hx(v) -> str | None:
    n = as_int(v)
    return "0x%X" % n if n is not None else None


def norm_slot(s) -> str | None:
    """`vt[0x0CC]` / `vt[0xCC]` / `vt[76]` → `vt[0xCC]`（README 的零填充写法不一）。"""
    if not s:
        return None
    m = re.search(r"0x([0-9A-Fa-f]+)|\[(\d+)\]", str(s))
    if not m:
        return str(s).strip().lower()
    n = int(m.group(1), 16) if m.group(1) else int(m.group(2))
    return "vt[0x%X]" % n


def scalar_width(wire_type: str | None) -> int | None:
    """线类型 → 定宽字节数；聚合/变长/未知一律 None。

    `bytes[73]` / `char[73]` / `u8[73]` 这类**定长数组**也是定宽（= 73），
    必须能算出宽度，否则模型里明明写了长度却永远对不上（批次 1 的 `room_name`）。
    **整型定长数组同族**：`u16[7]` = 14、`u32[10]` = 40、`u64[N]` = 8N —— 复核批次 23
    的㉝坑一：这里原先只认 `char/byte/u8/i8/bool/bytes[N]`，`u16[7]` 这类**没有宽度**，
    于是 `wire_shape()` 回落 `agg`、字段**不进 `checkable`**，定宽对位时当它不存在
    （静默跳过，比报错更危险）。
    """
    if not wire_type:
        return None
    t = str(wire_type).strip().strip("`").lower()
    if t in WIDTH_OF_TYPE:
        return WIDTH_OF_TYPE[t]
    m = re.match(r"^(u|i|f)(8|16|32|64)$", t)
    if m:
        return int(m.group(2)) // 8
    m = re.match(r"^(?:char|byte|u8|i8|bool|bytes)\s*\[\s*(\d+)\s*\]$", t)
    if m:
        return int(m.group(1))
    m = INT_ARR_RE.match(t)
    if m:
        return int(m.group(3)) * (int(m.group(2)) // 8)
    return None


# 整型定长数组：`u16[7]` / `i32[5]` / `f32[4]`。宽度 = 元素宽 × 元素数。
INT_ARR_RE = re.compile(r"^(u|i|f)(8|16|32|64)\s*\[\s*(\d+)\s*\]$")


STR_LIKE_RE = re.compile(r"^str(?![a-z])|^string(?![a-z])|^blob(?![a-z])|^char\[")
VAR_INT_RE = re.compile(r"^(u|i)(8|16|32|64)_var\b|^varint")


def wire_shape(wire_type: str | None) -> str:
    """线类型 → 形状：`scalar` / `fixed_arr`（N 字节定长数组）/ `str`（NUL 结尾变长串）
    / `agg`（聚合、变长数组、未知）。

    ⚠ `str` 的判定必须用**词边界**：`struct pilot_detail` 也以 "str" 开头，
    用 `startswith("str")` 会把结构体误判成变长串（批次 1 里的假阳性来源）。
    """
    t = str(wire_type or "").strip().strip("`").lower()
    if not t:
        return "agg"
    if re.match(r"^(?:char|byte|u8|i8|bool|bytes)\s*\[\s*\d+\s*\]$", t):
        return "fixed_arr"
    if INT_ARR_RE.match(t):
        return "fixed_arr"      # 整型定长数组也是 fixed_arr（宽度见 `scalar_width`）
    if STR_LIKE_RE.match(t) and not t.startswith("struct"):
        return "str"
    if t.startswith("array<") or t.startswith("struct") or re.search(r"\[\d+\]$", t):
        return "agg"
    return "scalar" if scalar_width(t) is not None else "agg"


# ---------------------------------------------------------------- 指令切片解析

class Insn:
    __slots__ = ("ea", "mnem", "text", "ops", "sidx")

    def __init__(self, rec):
        self.ea = int(rec[0])
        self.mnem = rec[1] or ""
        self.text = rec[2] or ""
        self.ops = rec[3] or []
        self.sidx = rec[4] if len(rec) > 4 else -1

    # -- 操作数访问 ------------------------------------------------------
    def ot(self, i):
        return self.ops[i][0] if i < len(self.ops) else 0

    def ov(self, i):
        return self.ops[i][1] if i < len(self.ops) else 0

    def ox(self, i):
        return self.ops[i][2] if i < len(self.ops) else ""

    def is_reg(self, i):
        return self.ot(i) == O_REG

    def is_imm(self, i):
        return self.ot(i) == O_IMM

    def is_mem(self, i):
        return self.ot(i) in (O_MEM, O_DISPL, O_PHRASE)

    def imm(self, i):
        return self.ov(i) if self.is_imm(i) else None

    def nops(self):
        return len(self.ops)

    def __repr__(self):
        return "%s %s" % (hex(self.ea), self.text)


class Slice:
    """一份原始切片（一个命令块 + 其一级被调函数体）。"""

    def __init__(self, doc: dict):
        self.doc = doc
        self.id = doc.get("id")
        self.direction = doc.get("direction")
        self.proto = doc.get("proto")
        self.opcode = doc.get("opcode")
        self.block = [int(str(x), 16) for x in doc.get("block", [])] or [0, 0]
        self.insns = [Insn(r) for r in doc.get("insns", [])]
        self.strings = doc.get("strings", [])
        self.callees = {}
        for k, v in (doc.get("callees") or {}).items():
            self.callees[int(k, 16) if str(k).startswith("0x") else int(k)] = v
        self.range_from = doc.get("range_from")
        self.block_truncated = bool(doc.get("block_truncated"))

    # -- 工具 ------------------------------------------------------------
    def text(self, i: int) -> str:
        return self.insns[i].text if 0 <= i < len(self.insns) else ""

    def find_call_index(self, target: int) -> int | None:
        for i, ins in enumerate(self.insns):
            if ins.mnem == "call" and ins.ov(0) == target and ins.ot(0) == O_NEAR:
                return i
        return None

    def callee_body(self, va: int):
        for key, rec in self.callees.items():
            if int(key) == int(va):
                return [Insn(r) for r in rec.get("insns", [])], rec
        return None, None

    def call_site_of(self, func_va: int) -> int | None:
        """块内对某函数的**调用点** EA（不是函数入口 VA）。"""
        i = self.find_call_index(func_va)
        return self.insns[i].ea if i is not None else None


# ---------------------------------------------------------------- 被调函数分类

def classify_body(insns: list[Insn]) -> dict:
    """按函数体形态分类（等价 `ida_draft_wire.io_width()`，但跑在本地切片上）。"""
    has_call = False
    has_memcpy = False
    has_cmp = False
    widths = []
    calls = []
    for ins in insns:
        if ins.mnem == "call":
            has_call = True
            t = ins.ov(0)
            calls.append(t)
            if ins.ot(0) == O_NEAR and t == MEMCPY:
                has_memcpy = True
        if ins.mnem == "cmp":
            has_cmp = True
        if (ins.mnem == "add" and ins.is_mem(0) and ins.is_imm(1)
                and ins.ov(1) in (1, 2, 4, 8)):
            widths.append(ins.ov(1))
    if has_memcpy:
        return {"kind": "blob", "width": None, "calls": calls}
    if not has_call and len(widths) == 1:
        return {"kind": "bounded" if has_cmp else "reserve",
                "width": widths[0], "calls": calls}
    return {"kind": "composite" if calls else "opaque", "width": None, "calls": calls}


def _cursor_step_by_register(insns: list[Insn]) -> int:
    """识别「游标值经寄存器推进」惯用法，返回累加的步进字节数。

    读数器有两族写法，`consumed_bytes` 原本只认第一族：

      * **就地推进**：`add dword ptr [CO], IMM`
      * **取值推进**（本函数，批次 17 的 `sub_B060E0` 一族）：
        ```
        mov edx, [ecx]      ; 取游标当前值
        add edx, 36h        ; 推进 54 —— 定长数组 `u8[54]` 的整块步进
        mov [ecx], edx      ; 写回游标
        ```
    这一族**没有** `add [mem], IMM`，所以旧口径算出 `consumed = 0`：
    定长数组字段（`u8[54]` / `u32[54]` / `str` 的槽）于是在定宽对位里
    「找不到读写点」而误报缺口（`SC-0x54C6` 的 `order_all_number` 等 3 条）。

    判据收紧到「同一内存操作数的取值—推进—写回」三段式且该操作数是**简单 `[reg]`**：
    `add REG,IMM` 前有 `mov REG,[reg]`、后有 `mov [reg],REG`。游标对象一定是直接解引用
    （`mov ecx,[esp+arg_0]` 取到游标对象，再 `mov edx,[ecx]`），故限定简单 `[reg]` 形态
    能排除「普通字段自增」那种 `mov edx,[esi+8]; add edx,4; mov [esi+8],edx` 的误伤。

    不限制 IMM 大小：步进量就是**数组总字节数**（54/216/51 都是合法步进），
    旧口径把它限死在 `(1,2,4,8)` 正是漏掉 `u8[54]` 这类的原因。
    """
    SIMPLE_DEREF = re.compile(r"^\[[a-z][a-z0-9_]*\]$")
    steps, WIN = 0, 8
    for i, ins in enumerate(insns):
        if ins.mnem != "add" or not ins.is_reg(0) or not ins.is_imm(1):
            continue
        imm = ins.ov(1)
        if not (0 < imm < 0x100000):
            continue
        reg = ins.ox(0).strip().lower()
        src = None
        for k in range(i - 1, max(i - 1 - WIN, -1), -1):
            ik = insns[k]
            if ik.mnem == "mov" and ik.is_reg(0) and ik.is_mem(1) \
                    and ik.ox(0).strip().lower() == reg:
                cand = ik.ox(1).strip().lower()
                if SIMPLE_DEREF.match(cand):
                    src = cand
                break
            if ik.mnem in ("call", "ret", "retn", "jmp") or ik.is_mem(0):
                break
        if src is None:
            continue
        for k in range(i + 1, min(i + 1 + WIN, len(insns))):
            ik = insns[k]
            if ik.mnem == "mov" and ik.is_mem(0) and ik.is_reg(1) \
                    and ik.ox(0).strip().lower() == src \
                    and ik.ox(1).strip().lower() == reg:
                steps += imm
                break
            if ik.mnem in ("call", "ret", "retn", "jmp") or ik.is_reg(0):
                break
    return steps


def consumed_bytes(insns: list[Insn], slice_: Slice, depth: int = 0,
                   seen: set | None = None) -> tuple[int | None, str, int]:
    """复合读取器消费量：整函数扫描 + 内联 `add [cur],IMM` 累加。

    返回 `(总字节数 | None, 说明, 其中「区域切分」字节数)`。含回跳（循环）或变长串时
    返回 None —— 因为「循环必须按次数展开」（批次-8 铁律），本地不猜。

    为什么要把「区域切分」单独报出来（批次 17 的坑）：`sub_B060E0` 一族
    （IDA 反编译即 `*dest = *holder; *holder += N;`）不是线读取器，而是**把刚申请的
    解码缓冲切块发给字段**——它推进的是「解码缓冲写指针」，不是报文游标。它们
    **确实**标出了字段宽度（426 字节缓冲被切成 54/54/216/51，逐块对应 `u8[54]` 等），
    所以定宽对位要用它；但它们**不消费线长**，所以「观测线长下界 vs 容量」不能计它
    （否则 `0x64` 缓冲上「切分 100 + 循环可见一趟 2」= 102 会假报超容量）。
    """
    if seen is None:
        seen = set()
    carve = _cursor_step_by_register(insns)
    total = carve
    for idx, ins in enumerate(insns):
        if ins.mnem in JCC or ins.mnem == "jmp":
            tgt = ins.ov(0)
            if ins.ot(0) in (O_NEAR, O_FAR) and 0 < tgt <= ins.ea:
                return None, "含回跳（需按循环次数展开）", 0
        if ins.mnem == "add" and ins.is_mem(0) and ins.is_imm(1) and ins.ov(1) in (1, 2, 4, 8):
            total += ins.ov(1)
            continue
        if ins.mnem != "call":
            continue
        t = ins.ov(0)
        if ins.ot(0) != O_NEAR:
            continue
        if t in PRIM_READ:
            w = PRIM_READ[t]
            if w == "str":
                return None, "含变长串", 0
            total += WIDTH_OF_TYPE[w]
            continue
        if t in PRIM_WRITE:
            w = PRIM_WRITE[t]
            if w == "str":
                return None, "含变长串", 0
            total += WIDTH_OF_TYPE[w]
            continue
        if depth >= 3 or t in seen:
            continue
        body, _rec = slice_.callee_body(t)
        if not body:
            return None, "调用未取到函数体 %s（需加大 callee 深度或人工续扫）" % hex(t), 0
        seen.add(t)
        sub, note, sub_carve = consumed_bytes(body, slice_, depth + 1, seen)
        seen.discard(t)
        if sub is None:
            return None, note, 0
        total += sub
        carve += sub_carve
    return total, "整函数扫描（无回跳）", carve


def _prim(kind: str, wire_type: str) -> dict:
    """读写原语 → 事件。`str` 是 NUL 结尾变长串（长度 = 串长 + 1），宽度给 None。"""
    w = WIDTH_OF_TYPE.get(wire_type)
    return {"kind": kind, "width": w, "wire_type": wire_type,
            "variable": w is None,
            "note": "变长串（长度 = 串长 + 1）" if w is None else None}


def classify_callee(va: int, slice_: Slice) -> dict:
    if va in PRIM_READ:
        return _prim("read", PRIM_READ[va])
    if va in PRIM_WRITE:
        return _prim("write", PRIM_WRITE[va])
    for proto, (g, r) in GUARD.items():
        if va == g:
            return {"kind": "guard", "proto": proto}
        if r is not None and va == r:
            return {"kind": "release"}
    if va == COMMIT:
        return {"kind": "commit"}
    if va == CURSOR_INIT:
        return {"kind": "cursor_init"}
    if va == CURSOR_RESET:
        return {"kind": "cursor_reset"}
    body, rec = slice_.callee_body(va)
    if not body:
        return {"kind": "unknown", "note": "函数体未取到"}
    c = classify_body(body)
    used, note, carve = consumed_bytes(body, slice_)
    out = {"kind": c["kind"], "width": c["width"], "consumed": used, "consume_note": note,
           "carve": carve, "name": (rec or {}).get("name"), "insns": len(body)}
    if c["kind"] == "reserve":
        out["note"] = "只推进解码缓冲游标（非字段）"
    return out


# ---------------------------------------------------------------- 六项复核

def find_capacity(slice_: Slice) -> dict | None:
    """容量指纹：`mov R,[H+78h]` → 紧随 `push IMM; call R`。

    四约束：只认 `+78h` 分配器；寄存器任意；立即数两种写法；宿主优先带位移
    （`[esi+0Ch]` 是解码器对象，`[esi]` 是客户端对象 —— 双宿主坑）。
    """
    cands = []
    insns = slice_.insns
    for i, ins in enumerate(insns):
        if ins.mnem != "mov" or not ins.is_reg(0) or not ins.is_mem(1):
            continue
        if "+78h" not in ins.ox(1).lower():
            continue
        reg = ins.ox(0).strip()
        host = ins.ox(1)
        alloc_va = ins.ea
        for j in range(i + 1, min(i + 14, len(insns))):
            ij = insns[j]
            if ij.mnem == "push" and ij.is_imm(0):
                for k in range(j + 1, min(j + 4, len(insns))):
                    ik = insns[k]
                    if ik.mnem != "call":
                        continue
                    if ik.is_reg(0) and ik.ox(0).strip() == reg:
                        cands.append({
                            "value": ij.ov(0), "va": hx(ij.ea), "reg": reg,
                            "host": host, "alloc_va": hx(alloc_va), "call_va": hx(ik.ea),
                        })
                break
            if ij.mnem in ("call", "jmp", "retn", "ret"):
                break
    if not cands:
        return None
    # 双宿主：优先带位移的宿主（解码器对象），无位移宿主只在唯一候选时采用
    disp = [c for c in cands if re.search(r"\+[0-9A-Fa-f]+h?\]", c["host"] or "")]
    pool = disp or cands
    return pool[0]


def find_guard(slice_: Slice) -> dict | None:
    pair = GUARD.get(slice_.proto or "")
    if not pair:
        return None
    gva, rva = pair
    for i, ins in enumerate(slice_.insns):
        if ins.mnem == "call" and ins.ot(0) == O_NEAR and ins.ov(0) == gva:
            module = None
            for j in range(i - 1, max(-1, i - 4), -1):
                if slice_.insns[j].mnem == "push" and slice_.insns[j].is_imm(0):
                    module = slice_.insns[j].ov(0)
                    break
            return {"va": hx(ins.ea), "func": hx(gva), "module_id": module,
                    "release_va": hx(rva) if rva else None}
    return None


def find_closer(slice_: Slice, window_start: int, window_end: int) -> dict | None:
    """闭合点：`cmp <游标>,<末尾>` + `jz/je` **或** `jnz/jne`（第 ② 条）。

    排除 `cmp reg,IMM`（循环上界）与 `cmp reg,reg`（数组循环），
    优先「含内存操作数」的 cmp；取窗口内**最后一个**候选。

    同时记四个址（`protocol_analysis` 的 README 对闭合点有四种记法，diff 侧全认）：
      * `va`      —— cmp 指令址（本工具的规范口径）；
      * `jcc_va`  —— 紧随的条件跳转址；
      * `seq_va`  —— 闭合序列起点（cmp 之前为该 cmp 装载操作数的 `mov/lea/sub/add` 链）；
      * `jcc_dst` —— 跳转**落点**（cmp 成立后跳到的标签址）。有的 README 把「校验通过后
        落到哪里」记成闭合点（`push <module>; call <release>` 的入口），语义上等价于
        「此处校验游标 == 末尾」，故一并认。
    """
    cands = []
    insns = slice_.insns
    for i, ins in enumerate(insns):
        if ins.mnem != "cmp" or ins.ea < window_start or ins.ea > window_end:
            continue
        if ins.is_imm(0) or ins.is_imm(1):
            continue
        if not (ins.is_mem(0) or ins.is_mem(1)):
            continue
        for k in range(i + 1, min(i + 6, len(insns))):
            ik = insns[k]
            if ik.mnem in NS_MNEM:
                continue
            if ik.mnem in JZ or ik.mnem in JNZ:
                cands.append({"va": hx(ins.ea), "kind": "jz" if ik.mnem in JZ else "jnz",
                              "jcc_va": hx(ik.ea),
                              "seq_va": _closure_seq_start(insns, i),
                              "jcc_dst": hx(ik.ov(0)) if ik.ot(0) == O_NEAR else None,
                              "cmp": ins.text})
            break
    if cands:
        return cands[-1]
    # 退路：C→S 的闭合 = 提交调用 / 发送点
    if slice_.direction == "CS":
        for i, ins in enumerate(insns):
            if ins.mnem == "call" and ins.ot(0) == O_NEAR and ins.ov(0) == COMMIT:
                return {"va": hx(ins.ea), "kind": "commit", "jcc_va": None,
                        "seq_va": None, "cmp": None}
        d = find_dispatch(slice_, exclude_va=None)
        if d:
            return {"va": d["va"], "kind": "send", "jcc_va": None, "seq_va": None, "cmp": None}
    return None


def _closure_seq_start(insns: list[Insn], cmp_i: int) -> str | None:
    """闭合序列起点：cmp 之前为其装载操作数的 `mov/lea/sub/add`（最多回退 4 条）。"""
    j = cmp_i - 1
    steps = 0
    start = None
    while j >= 0 and steps < 4:
        ins = insns[j]
        if ins.mnem not in ("mov", "lea", "sub", "add"):
            break
        start = hx(ins.ea)
        steps += 1
        j -= 1
    return start


def _count_argc(insns: list[Insn], call_i: int, lo: int) -> int:
    """去向实参个数：**以「分支/调用」为边界向前清点 push**（批次-8 口径）。"""
    n = 0
    j = call_i - 1
    while j >= 0 and insns[j].ea >= lo:
        ins = insns[j]
        if ins.mnem in JCC or ins.mnem in ("jmp", "retn", "ret", "call", "cmp", "test"):
            break
        if ins.mnem == "push":
            n += 1
        j -= 1
    return n


def find_dispatch(slice_: Slice, exclude_va: str | None) -> dict | None:
    """业务去向：`mov R,[H+NNNh]` + `call R`（或直接 `call [H+NNNh]`）。

    选法（口径来自长期记忆）：
      * 排除 `+78h`（双宿主坑：那是解码缓冲分配器）与 `vt[0x64]`（报错槽）。
      * **槽值上限 `MAX_SLOT`**：虚表槽都在低偏移（0x58/0x70/0x154/0x32C/0x3F4/0x4AC…），
        `[X+2C5Ch]`、`[X+79A8h]` 这类是**对象成员/通知回调**，不是去向槽 —— 不设上限会
        把 `mov eax,[esi+2C5Ch]; ...; call eax` 误判为去向（假阳性主因）。
      * **C→S**：去向恒为 `vt[0x58](buf, 负载长度)` ⇒ 优先取 slot 0x58。
      * **S→C**：业务去向落在块尾（错误路径均以 `jmp` 出块）⇒ 取**最后一个**候选。
    """
    insns = slice_.insns
    cands = []
    for i, ins in enumerate(insns):
        # 形态二：`call dword ptr [H+NNNh]` —— 间接调用直接带槽位
        if ins.mnem == "call" and ins.is_mem(0):
            m = re.search(r"\+([0-9A-Fa-f]+)h", ins.ox(0))
            if m:
                slot = int(m.group(1), 16)
                if 0 < slot <= MAX_SLOT and slot not in (0x78, ERROR_SLOT):
                    cands.append({
                        "slot": "vt[0x%X]" % slot, "slot_value": slot,
                        "va": hx(ins.ea), "mov_va": hx(ins.ea), "host": ins.ox(0),
                        "argc": _count_argc(insns, i, slice_.block[0]),
                        "form": "call_mem",
                    })
            continue
        if ins.mnem != "mov" or not ins.is_reg(0) or not ins.is_mem(1):
            continue
        m = re.search(r"\+([0-9A-Fa-f]+)h", ins.ox(1))
        if not m:
            continue
        slot = int(m.group(1), 16)
        reg = ins.ox(0).strip()
        # `+78h` 是**双宿主槽**，不能一律排除：解码缓冲对象上它是分配器
        # （`mov ecx,[esi+0Ch]; mov eax,[ecx]; mov edx,[eax+78h]; push 4; call edx`），
        # 而客户端对象自身虚表上它就是**业务去向**
        # （`mov edx,[esi]; mov edx,[edx+78h]; ...; call edx` —— `SC-0x8F36` 即此形）。
        # 分配点由 `exclude_va`（容量 claim 的 `alloc_va`）单独排除；此处只降权，
        # 非 0x78 槽存在时不选它（选法见函数尾）。
        if slot == ERROR_SLOT or slot > MAX_SLOT:
            continue
        for k in range(i + 1, min(i + 24, len(insns))):
            ik = insns[k]
            if ik.mnem == "call" and ik.is_reg(0) and ik.ox(0).strip() == reg:
                if exclude_va and hx(ins.ea) == exclude_va:
                    break
                if any(x.mnem in ("jmp", "retn", "ret") for x in insns[i + 1:k]):
                    break
                cands.append({
                    "slot": "vt[0x%X]" % slot, "slot_value": slot,
                    "va": hx(ik.ea), "mov_va": hx(ins.ea), "host": ins.ox(1),
                    "argc": _count_argc(insns, k, slice_.block[0]),
                    "form": "mov_then_call",
                })
                break
            if ik.mnem in ("call", "jmp", "retn", "ret"):
                break
    if not cands:
        return None
    # `+78h` 降权：只要还有别的槽候选，就不拿 0x78 当去向（它是分配器最常见的宿主位）。
    non78 = [c for c in cands if c["slot_value"] != 0x78]
    if non78:
        cands = non78
    if slice_.direction == "CS":
        for c in cands:
            if c["slot_value"] == 0x58:
                return c
    return cands[-1]


def find_error_slot(slice_: Slice) -> dict | None:
    insns = slice_.insns
    for i, ins in enumerate(insns):
        if ins.mnem != "mov" or not ins.is_reg(0) or not ins.is_mem(1):
            continue
        if "+%Xh" % ERROR_SLOT not in ins.ox(1):
            continue
        reg = ins.ox(0).strip()
        for k in range(i + 1, min(i + 12, len(insns))):
            ik = insns[k]
            if ik.mnem == "call" and ik.is_reg(0) and ik.ox(0).strip() == reg:
                return {"slot": "vt[0x%X]" % ERROR_SLOT, "va": hx(ik.ea),
                        "argc": _count_argc(insns, k, slice_.block[0])}
            if ik.mnem in ("call", "jmp", "retn", "ret"):
                break
    return None


def wire_reads_in_body(body: list[Insn]) -> list[dict]:
    """读取器函数体内部的「线读」：`mov rN,[CUR]`。

    游标在读取器里有两种寄存器角色（长期记忆 批次-16）：
      * **游标对象寄存器** `CO` —— 被 `add dword ptr [CO],N` 推进的那个（`[CO]`=当前指针，
        `[CO+4]`=末尾指针），`cmp R,[CO+4]` 就是读取器的边界校验；
      * **游标值寄存器** `CV` —— `mov CV,[CO]` 取出的当前指针，线读都形如 `mov rN,[CV]`。
    只把 `[CV]` 上的读算线读：`[CO]`/`[CO+4]` 是游标自身的读写（记账，不是字段）。

    ⚠ 批次-27 补：`mov rN,[CV+4]` 是**未展开的 8 字节读的第二半**，也要算一条线读。
    内联 u64 的写法是 `mov edx,[eax]; mov [edi],edx; mov eax,[eax+4]; mov [edi+4],eax;
    add dword ptr [esi],8`（`sub_B06D80` 的 `ms.uniqid` @0xB06D93/0xB06D9C）—— 第二半带
    位移 `+4`，原来只认 `[CV]` 整条漏掉，于是 `u64` 只记到 4 字节，**后面所有成员整体前移一位**，
    成员级字节预算全盘错位（0x1E2F 的 43 成员只剩尾部几条对上）。
    全库 915 份切片里 `[CV+4]` 共 84 处，**全部**后随 `add dword ptr [CO],8`（u64 第二半），
    无例外（`sub_B06200` 读原语自身也是这个写法）。
    """
    add_cur, cur_regs = set(), set()
    for ins in body:
        if ins.mnem == "add" and ins.is_mem(0) and ins.is_imm(1):
            m = re.match(r"^(?:dword|word|byte)\s+ptr\s+\[([a-z0-9_]+)\]$", ins.ox(0).strip().lower())
            if m:
                add_cur.add(m.group(1))
    for ins in body:
        if ins.mnem in ("mov", "movzx", "movsx") and ins.is_reg(0) and ins.is_mem(1):
            m = re.match(r"^\[([a-z0-9_]+)\]$", ins.ox(1).strip().lower())
            if m and m.group(1) in add_cur:
                cur_regs.add(ins.ox(0).strip().lower())
    out = []
    for ins in body:
        if ins.mnem == "call" and ins.ot(0) == O_NEAR:
            w = scalar_width(PRIM_READ.get(ins.ov(0)))
            if w:
                # 读取器体内部还会调用定宽读原语（批次 1 的 clan 读取器：`call sub_B06230` 读 u8）
                out.append({"va": hx(ins.ea), "width": w, "via": "primitive_call"})
            continue
        if ins.mnem not in ("mov", "movzx", "movsx") or not ins.is_reg(0) or not ins.is_mem(1):
            continue
        m = re.match(r"^\[([a-z0-9_]+)(?:\+4)?\]$", ins.ox(1).strip().lower())
        if not m or m.group(1) not in cur_regs:
            continue
        w = reg_width(ins.ox(0))
        if w:
            out.append({"va": hx(ins.ea), "width": w})
    return out


def _loop_trip(body: list[Insn], jcc_i: int, tgt: int) -> tuple[int, str]:
    """回跳循环的行程 = `ceil((上限 - 初值) / 步长)`，返回 `(趟数, 计数器)`。

    ⚠ 不能只看回边前 `cmp reg,IMM` 的 IMM（批次-27 的 0x1E2F **ms** 读取器）：
    游标按 `add reg,STEP` 步进时，IMM 是**索引上界**而不是趟数。`sub_B06D80` 尾部读
    `u32[3][4]`（48 字节）的写法是

        mov edx, 2Fh            ; 初值 47
        loc: … mov eax,[eax] … add edx,4 … cmp edx,3Bh; jb   ; 上界 59

    真趟数 = (59 − 47) / 4 = 3（× 内层 4 = 12 条 u32 = 48 字节）；按 IMM=59 硬展开成
    236 字节，读数总和 428 而不是 244，`ms` 于是报「整体宽度对不上」。
    初值取回跳循环入环前的 `mov ctr,IMM` / `xor ctr,ctr`（找不到按 0，步长按 1，
    此时退化为原来的 `trip = IMM`，其它批次的口径不变）。
    """
    end = body[jcc_i].ea
    ctr = lim = None
    for j in range(jcc_i - 1, max(-1, jcc_i - 8), -1):
        ij = body[j]
        if ij.ea < tgt:
            break
        if ij.mnem == "cmp" and ij.is_imm(1) and ij.imm(1):
            lim = ij.imm(1)
            ctr = ij.ox(0).strip().lower() if ij.is_reg(0) else None
            break
    if not ctr or lim is None:
        return 1, ""
    step = 1
    for ik in body:
        if ik.ea < tgt or ik.ea > end:
            continue
        if ik.mnem in ("add", "sub") and ik.is_reg(0) and ik.is_imm(1) \
                and ik.ox(0).strip().lower() == ctr:
            step = ik.ov(1) if ik.mnem == "add" else -ik.ov(1)
            break
        if ik.mnem in ("inc", "dec") and ik.is_reg(0) and ik.ox(0).strip().lower() == ctr:
            step = 1 if ik.mnem == "inc" else -1
            break
    if step <= 0:
        return max(1, lim), ctr
    init = 0
    start = next((k for k, ik in enumerate(body) if ik.ea == tgt), None)
    if start is not None:
        for j in range(start - 1, max(-1, start - 12), -1):
            ij = body[j]
            if ij.mnem in ("call", "ret", "retn", "jmp") or ij.is_mem(0):
                break
            if ij.mnem == "mov" and ij.is_reg(0) and ij.is_imm(1) \
                    and ij.ox(0).strip().lower() == ctr:
                init = ij.imm(1)
                break
            if ij.mnem == "xor" and ij.is_reg(0) and ij.is_reg(1) \
                    and ij.ox(0).strip().lower() == ij.ox(1).strip().lower() == ctr:
                init = 0
                break
    return max(1, -(-(lim - init) // step)), ctr


def expand_loops(body: list[Insn], reads: list[dict], max_trip: int = 256) -> list[dict]:
    """把落在回跳循环体内的线读按行程数展开（`cmp reg,IMM` + `jb` ⇒ IMM 次）。

    读取器内部常见 `cmp ecx,2; jb` 的「2×u32 → 模型记 u64」写法，不展开就会把
    8 字节的成员判成 4 字节缺口（批次 1 的 `missionunit_store_r`）。

    ⚠ 行程数**上限 `max_trip`**：字符串/名表循环的行程是**字段值**（如名字长度 64），
    硬展开会凭空造出几十条线读，把对位彻底打乱（批次 1 的 `btlroom_info_one`）。
    超过上限 ⇒ 该读标 `trip_unknown`，只记一条、不参与定宽对位。

    ⚠ **嵌套循环是相乘不是取大**（同批次-27）：二维数组读
    `for row(4) { for col(3) { read } }` 里内层读被执行 12 次。原来取 `max` 会
    按外层的上界（如 `cmp edi,48h` = 72）算，把 `u32[40]` 记成 72 条
    （`SC-0xDC47` 的 `sub_B43E00`）；clan 名表 `4 × 28` 更会被少记成 28。
    """
    loops = []
    for i, ins in enumerate(body):
        if ins.mnem not in JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (O_NEAR, O_FAR) else None
        if not tgt or tgt >= ins.ea:
            continue
        loops.append((tgt, ins.ea, _loop_trip(body, i, tgt)[0]))
    if not loops:
        return [dict(r, loop_trip=1) for r in reads]
    out = []
    for r in reads:
        ea = as_int(r["va"]) or 0
        trip = 1
        for s, e, t in loops:
            if s <= ea <= e:
                trip *= t
        if trip > max_trip:
            out.append(dict(r, loop_trip=trip, trip_unknown=True))
            continue
        for _ in range(trip):
            out.append(dict(r, loop_trip=trip))
    return out


def collect_nested_reads(slice_: Slice, prim: dict) -> list[dict] | None:
    """复合/不透明读取器调用 → 展开其内部的线读序列（None = 函数体未取到）。"""
    body, _ = slice_.callee_body(as_int(prim.get("target")))
    if not body:
        return None
    return expand_loops(body, wire_reads_in_body(body))


# --------------------------------------------------- 块内回跳循环：数组读 / 非数组读
#
# 复核批次 23 的㉝坑二：`collect_primitives` 只看命令块里的 `call`，**不展开块内回跳**，
# 于是 `xor edi,edi … call sub_B02DD0 … add ebx,4 … cmp edi,5; jb` 这种
# 「5×u32 = 20」只被记成一条 4B 读 —— 模型写 `u32[5]` 反而对不上（㉝坑一的 7 条假阳性）。
# 但**不能**一律展开：去重 / 重试 / 条件分支都会回跳，硬展开会把真值改成假阳性
# （同一实验里差异面 7 → 18，`SC-0x640D`「观测 1077 > 容量 0x179」就是自相矛盾的证候）。
# 所以这里先**分类**：只有「每迭代读一个线字段」的循环才按行程折算宽度。

def _loop_trip_1step(body: list[Insn]) -> tuple[int, str] | tuple[None, None]:
    """回跳循环的行程：体内有 **1 步计数器**（`add r,1` / `inc r`）且回边前 `cmp r,IMM`。

    用「1 步计数器」当闸门，是为了排掉 `cmp esi,0C1h` / `cmp ecx,[末尾]` 这类
    **按数据定长**的循环（名字串、变长段）——它们的「行程」是字段值，不是元素数。
    """
    counter = None
    for ins in body:
        if ins.mnem in ("add", "sub") and ins.is_reg(0) and ins.is_imm(1) and ins.ov(1) == 1:
            counter = ins.ox(0).strip().lower()
        elif ins.mnem == "inc" and ins.nops() >= 1 and ins.is_reg(0):
            counter = ins.ox(0).strip().lower()
    if counter is None:
        return None, None
    for ins in reversed(body):
        if ins.mnem == "cmp" and ins.is_reg(0) and ins.is_imm(1) \
                and ins.ox(0).strip().lower() == counter:
            return max(1, ins.imm(1)), counter
    return None, None


def _loop_is_array_read(body: list[Insn], start: int, end: int) -> tuple[bool, str]:
    """块内回跳循环是否「每迭代读一个线字段」（三条同时成立才认）。

    1. 体内**至少一个读原语调用**（`call <sub_B02DD0/B02DF0/...>`），且体内**没有
       别的调用**——元素是复合读取器的循环（`array<X,N>` 那种）由 `consumed` 记账，
       在这里再折一次就是重复计数；
    2. 体内条件跳转只允许「回边本身」与「前向逃逸」（`test al,al; jz <错误出口>`）——
       **跳过型分支**（去重 / 重试 / 条件字段）一律不算数组读；
    3. 回边比较的是 1 步计数器（见 `_loop_trip_1step`）。
    """
    reads = 0
    for ins in body:
        if ins.mnem != "call" or ins.ot(0) != O_NEAR:
            continue
        t = ins.ov(0)
        if t in PRIM_READ or t in PRIM_WRITE:
            reads += 1
            continue
        return False, "体内有非读原语调用 %s" % hex(t)
    if not reads:
        return False, "体内无线读"
    for ins in body:
        if ins.mnem not in JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (O_NEAR, O_FAR) else None
        if tgt is None:
            continue
        if tgt == start and ins.ea == end:
            continue                      # 回边
        if tgt > end:
            continue                      # 前向逃逸（错误出口）
        return False, "体内有跳过型分支 %s" % hex(ins.ea)
    if _loop_trip_1step(body)[0] is None:
        return False, "回边比较的不是 1 步计数器"
    return True, "数组读"


def block_array_loops(slice_: Slice, lo: int, hi: int) -> list[tuple[int, int, int]]:
    """块内被判为「数组读」的回跳循环 → `[(start_ea, end_ea, trip)]`。"""
    out = []
    for ins in slice_.insns:
        if ins.mnem not in JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (O_NEAR, O_FAR) else None
        if not tgt or tgt >= ins.ea:
            continue
        if tgt < lo or ins.ea > hi:
            continue
        body = [x for x in slice_.insns if tgt <= x.ea <= ins.ea]
        trip, _ctr = _loop_trip_1step(body)
        if trip is None or trip > 256:
            continue
        ok, _why = _loop_is_array_read(body, tgt, ins.ea)
        if ok:
            out.append((tgt, ins.ea, trip))
    return out


def collect_primitives(slice_: Slice, lo: int, hi: int, direction: str) -> list[dict]:
    """窗口内按线序的读写原语序列（含 reserve / composite，各自带类别）。"""
    loops = block_array_loops(slice_, lo, hi)
    out = []
    for ins in slice_.insns:
        if ins.ea < lo or ins.ea > hi or ins.mnem != "call" or ins.ot(0) != O_NEAR:
            continue
        t = ins.ov(0)
        info = classify_callee(t, slice_)
        if info["kind"] in ("composite", "opaque", "unknown", "blob") and not info.get("name"):
            continue
        rec = {"va": hx(ins.ea), "target": hx(t), "name": info.get("name") or "",
               "kind": info["kind"], "width": info.get("width"),
               "wire_type": info.get("wire_type"),
               "consumed": info.get("consumed"), "consume_note": info.get("consume_note"),
               "carve": info.get("carve"),
               "reserve_note": info.get("note")}
        if rec["kind"] in ("composite", "opaque", "blob", "bounded", "unknown"):
            nested = collect_nested_reads(slice_, rec)
            if nested:
                rec["nested"] = nested
                # 内部线读之和 = 该读取器本次实际消费的线长（可替代未知的 consumed）；
                # 行程未知的循环读不计入（否则名字长度那种循环会把线长吹爆）
                known = [n for n in nested if not n.get("trip_unknown")]
                if known:
                    rec["consumed_effective"] = sum(n["width"] for n in known)
        if loops and rec["kind"] in ("read", "write") and rec["width"]:
            trip = 1
            for s, e, t2 in loops:
                if s <= ins.ea <= e:
                    trip = max(trip, t2)
            if trip > 1:
                # 一次「数组读」合并成一条事件：宽度 = 行程 × 单元宽（= `u32[5]` 的 20），
                # 而不是复制 trip 条 4B —— 复制出来的多条在 LCS 里仍然对不上单个定宽字段。
                rec["width"] = rec["width"] * trip
                rec["loop_trip"] = trip
        out.append(rec)
    return out


def collect_inline_stores(slice_: Slice, lo: int, hi: int) -> list[dict]:
    """窗口内的**内联写线**（`mov <buf>,<reg/imm>`，非栈、非对象成员）。

    C→S 的字段多数不是走写原语，而是内联 `mov [cursor],src`（批次-16/17 口径）。
    这里只认「无位移 / 位移为 0」的目标，用来把 `[esp+..]` 局部变量与
    `[esi+79ECh]` 之类对象成员排除掉；`[ebp+0]` 是 opcode，已按 seq 0 过滤。
    """
    out = []
    for ins in slice_.insns:
        if ins.ea < lo or ins.ea > hi or ins.mnem != "mov":
            continue
        if not ins.is_mem(0) or ins.is_reg(0):
            continue
        dest = ins.ox(0)
        if re.search(r"\+[1-9A-Fa-f]", dest) or "esp" in dest or "fs:" in dest:
            continue
        w = None
        lm = re.search(r"\b(byte|word|dword)\s+ptr\b", dest)
        if lm:
            w = {"byte": 1, "word": 2, "dword": 4}[lm.group(1)]
        elif ins.is_reg(1):
            w = reg_width(ins.ox(1))
        if w:
            role = "opcode" if (w == 2 and ins.is_imm(1)
                                and not re.search(r"\+[1-9A-Fa-f]", dest)) else None
            out.append({"va": hx(ins.ea), "kind": "inline_store", "width": w,
                        "name": "", "consumed": None, "type": ins.ox(1), "dest": dest,
                        "role": role})
    return out


def capacity_relation(seq_actual: list[dict], direction: str, cap: int | None) -> dict:
    """容量 vs 观测线长：`observed` 为**下界**（未知消费量不计入）。

    长期记忆 批次-9 的强不变量：`Σ字段 > 容量` ⇒ 一定多算了字段（915 条 0 违例）。
    故用下界判 `over` 是可靠的硬矛盾；`exact` 只在无未知项时给出。

    ⚠ 批次-17：`consumed` 里要**扣掉「区域切分」字节**（`carve`）。切分器
    （`*dest = *holder; *holder += N`，见 `consumed_bytes`）推进的是解码缓冲写指针，
    不消费线长；把它计入下界会和「同一区域的线读」重复计——10 条 lounge/battle
    命令因此假报 `over`（如 `SC-0x35F8` 容量 0x64：切分 100 + 循环可见一趟 2 = 102）。
    """
    observed = 0
    unknown = []
    for p in seq_actual:
        if p["kind"] in ("read", "write", "inline_store"):
            w = p["width"]
        else:
            w = p.get("consumed")
            if w is not None and p.get("carve"):
                # 只把「线读」部分计入下界；纯切分（w == carve）计 0
                w = max(0, w - p["carve"])
        if w is None:
            unknown.append({"va": p["va"], "kind": p["kind"], "name": p.get("name")})
        else:
            observed += w
    if direction == "CS" and not any(p.get("role") == "opcode" for p in seq_actual):
        observed += 2          # C→S 负载前还有 2B opcode（已在 events 里写过则不重复计）
    rel = None
    if cap is not None:
        if observed > cap:
            rel = "over"
        elif observed == cap and not unknown:
            rel = "exact"
        else:
            rel = "within"
    return {"observed_min": observed, "capacity": cap, "relation": rel,
            "unknown_events": unknown, "is_lower_bound": bool(unknown),
            "note": ("观测线长（下界）%d / 容量 %s" % (observed, hex(cap) if cap is not None else "?"))}


def _prim_consumed(p: dict) -> int | None:
    """原语本次消费的线长：优先读取器内部线读之和（`consumed_effective`）。"""
    return p.get("consumed") if p.get("consumed") is not None else p.get("consumed_effective")


def _same_event(e: dict, p: dict) -> bool:
    if p.get("kind") == "nested_run":
        # 并段只用来对「N 字节定长数组」字段（读取器里就是 N 条 u8 读）；
        #   聚合字段必须对到**调用点的 consumed**，否则会被并段抢走（0x244E 的 clan_zeon）。
        return e["shape"] == "fixed_arr" and e.get("width") is not None \
            and e["width"] == p["width"]
    return ((e["shape"] == "str" and p.get("wire_type") == "str")
            or (e["width"] is not None and p.get("width") == e["width"])
            or (e["width"] is not None and p["kind"] in ("composite", "opaque", "bounded")
                and _prim_consumed(p) == e["width"]))


def align_widths(expected: list[dict], actual: list[dict]) -> dict:
    """用 **LCS（最长公共子序列）** 对位「期望定宽字段」↔「汇编读写事件宽度」。

    为什么不用贪心推进：贪心遇到一个额外的 `reserve`/复合事件就整体错位，
    会把「序列其实完全一致」的命令报成差异（批次 1 里 `SC-0x063E` 就是这样）。
    LCS 允许两侧各有插入，只把**真正对不上**的期望字段算作缺口。
    """
    ei = [i for i, e in enumerate(expected) if e["width"] is not None or e["shape"] == "str"]
    # ⚠ `ai` 必须纳入「消费量已知的复合/不透明读取器」（`consumed`/`consumed_effective`）：
    #   否则 `struct{12}` 这类聚合字段永远对不上调用点，被误报成缺口（批次 1 的 rankself）。
    ai = [j for j, p in enumerate(actual)
          if p["width"] is not None or p.get("wire_type") == "str"
          or _prim_consumed(p) is not None]
    n, m = len(ei), len(ai)
    # dp[i][j] = expected[ei[i:]] 与 actual[ai[j:]] 的 LCS 长度
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            e, p = expected[ei[i]], actual[ai[j]]
            same = _same_event(e, p)
            dp[i][j] = max(dp[i + 1][j], dp[i][j + 1],
                           1 + dp[i + 1][j + 1] if same else 0)
    gaps, matched, pairs = [], 0, []
    i = j = 0
    while i < n and j < m:
        e, p = expected[ei[i]], actual[ai[j]]
        same = _same_event(e, p)
        if same and dp[i][j] == 1 + dp[i + 1][j + 1]:
            pairs.append({"field": e["name"], "width": e["width"], "shape": e["shape"],
                          "va": p["va"], "kind": p["kind"]})
            matched += 1
            i += 1
            j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            gaps.append({"field": e["name"], "wire_type": e["wire_type"],
                         "width": e["width"], "shape": e["shape"],
                         "note": "汇编事件序列里找不到与之对位的读写点（缺字段或宽度不符）"})
            i += 1
        else:
            j += 1
    while i < n:
        e = expected[ei[i]]
        gaps.append({"field": e["name"], "wire_type": e["wire_type"], "width": e["width"],
                     "shape": e["shape"], "note": "汇编事件序列里找不到与之对位的读写点"})
        i += 1
    matched_actual = {p["va"] for p in pairs}
    extras = [{"va": p["va"], "kind": p["kind"], "width": p["width"],
               "wire_type": p.get("wire_type")} for j, p in enumerate(actual)
              if j in ai and p["va"] not in matched_actual]
    return {"pairs": pairs, "gaps": gaps, "matched": matched, "checkable": n,
            "actual_events": len(ai), "unmatched_actual": extras}


def merge_nested_runs(reads: list[dict]) -> list[dict]:
    """把**连续同宽**的内部线读并成一条（`bytes[73]` 在读取器里就是 73 条 u8 读）。

    不并会把「一个定长数组字段」永远判成缺口（批次 1 的 `room_name`/`party_recruit`）。
    只并「同宽且 ≥2 条」的连续段；异宽段（`u32,u32,u8` 这类成员序列）留给成员级字节预算。
    """
    out, i = [], 0
    while i < len(reads):
        j = i
        while (j + 1 < len(reads) and reads[j + 1]["width"] == reads[i]["width"]
               and reads[j + 1].get("loop_trip", 1) == reads[i].get("loop_trip", 1)):
            j += 1
        n = j - i + 1
        if n >= 2:
            out.append({"va": reads[i]["va"], "width": reads[i]["width"] * n,
                        "kind": "nested_run", "count": n,
                        "unit_width": reads[i]["width"],
                        "vas": [r["va"] for r in reads[i:j + 1]]})
        else:
            out.append(dict(reads[i], kind="nested", count=1))
        i = j + 1
    return out


def member_groups(expected: list[dict]) -> list[dict]:
    """把 `父.成员` 形式的期望字段按父名聚组（保持出现顺序，返回期望下标）。"""
    groups = []
    for i, e in enumerate(expected):
        name = str(e.get("name") or "")
        if "." not in name:
            continue
        parent = name.split(".", 1)[0]
        if groups and groups[-1]["parent"] == parent:
            groups[-1]["idx"].append(i)
            groups[-1]["members"].append(e)
        else:
            groups.append({"parent": parent, "idx": [i], "members": [e]})
    return groups


def match_members(group: dict, reads: list[dict], prim: dict) -> dict:
    """成员组 ↔ 父读取器体内部线读：**按字节预算**走。

    模型把 `2×u32` 记成 `u64` 是常态（`missionunit_id` 就是），故一个成员的宽度可由
    **连续多条**内部线读凑齐（`merged` 记几条）。凑不齐则算缺口。
    """
    pairs, gaps = [], []
    if not reads:
        return {"pairs": pairs, "gaps": gaps,
                "unmatchable": [{"parent": group["parent"], "call_va": prim.get("va"),
                                 "reason": "读取器体内部无可识别线读（可能只按整块 memcpy）"}]}
    k = 0
    for m in group["members"]:
        w = m["width"]
        if w is None:
            # 串成员：内部读是变长循环，定宽判据不适用；聚合成员宽度已知者照走
            continue
        acc, used = 0, []
        while k < len(reads) and acc < w:
            acc += reads[k]["width"]
            used.append(reads[k])
            k += 1
        if acc == w and used:
            pairs.append({"field": m["name"], "width": w, "shape": m["shape"],
                          "va": used[0]["va"], "kind": "nested",
                          "vas": [u["va"] for u in used], "merged": len(used),
                          "parent": group["parent"], "call_va": prim.get("va")})
        else:
            gaps.append({"field": m["name"], "wire_type": m["wire_type"], "width": w,
                         "shape": m["shape"],
                         "note": "读取器 %s 内部线读凑不齐该成员宽度（已凑 %d / 需 %d）"
                                 % (prim.get("name") or prim.get("target"), acc, w)})
    return {"pairs": pairs, "gaps": gaps, "unmatchable": []}


def gap_explained_by_reader(slice_: Slice, field_rec: dict, prims: list[dict]) -> dict | None:
    """缺口字段的证据 VA 落在窗口内某读取器函数体里 ⇒ 该字段在读取器内部被读。

    这是**结构性**不可在调用点定宽的情形（消费量取决于读取器内部循环），
    应当记为「不可判定」而不是差异（长期记忆 批次-16）。
    """
    for raw in (field_rec.get("evidence_va") or []):
        va = as_int(str(raw).split("(")[0].split("/")[0].strip())
        if va is None:
            continue
        for p in prims:
            body, _ = slice_.callee_body(as_int(p.get("target")))
            if not body:
                continue
            if body[0].ea <= va <= body[-1].ea:
                return {"callee": p.get("name") or p.get("target"), "call_va": p["va"],
                        "evidence_va": hex(va)}
    return None


def log_strings(insns: list[Insn], strings: list[str], lo: int, hi: int) -> list[str]:
    used = []
    for ins in insns:
        if ins.ea < lo or ins.ea > hi:
            continue
        if ins.sidx is not None and 0 <= ins.sidx < len(strings):
            s = strings[ins.sidx]
            if s and s not in used:
                used.append(s)
    # 只留「像日志标记」的串：`xxx=` / `xxx={` / `xxx=[` / 单独 `}` 之类
    marks = [s for s in used if re.match(r"^[A-Za-z_][A-Za-z0-9_]*\s*[={[:]", s)]
    return marks if marks else used


def analyze(slice_: Slice, model: dict) -> dict:
    direction = slice_.direction or model.get("direction")
    window_start, window_end = slice_.block

    cap = find_capacity(slice_)
    guard = find_guard(slice_)
    # 字段窗口：守卫之后 → 释放调用点 / 提交 / 去向 之前
    #   ⚠ 长期记忆坑：`release_va` 是**释放函数的入口 VA**，字段窗口的右端要取块内
    #   该函数的**调用点**，直接用函数入口会把窗口拉到 0xB4xxxx（非本块地址）。
    rel = None
    if guard and guard.get("release_va"):
        rel = slice_.call_site_of(as_int(guard["release_va"]))
    commit_i = slice_.find_call_index(COMMIT)
    commit_va = slice_.insns[commit_i].ea if commit_i is not None else None
    disp = find_dispatch(slice_, exclude_va=(cap or {}).get("alloc_va"))

    if direction == "SC":
        lo = (as_int(guard["va"]) + 1) if guard else window_start
        hi = rel or (as_int(disp["va"]) if disp else None) or window_end
    else:
        # C→S：无守卫；窗口自块首（opcode 写入）起到提交为止
        lo = window_start
        hi = commit_va or (as_int(disp["va"]) if disp else None) or window_end

    closer = find_closer(slice_, lo, hi if hi else window_end)
    prims = collect_primitives(slice_, lo, hi or window_end, direction)
    # 日志/字段名串的取证窗口 = 闭合点（或提交点）之后到块尾 —— 长期记忆 批次-16：
    #   「字段名取证 = 提交后的 trace 打印块」，故不能只看字段窗口。
    log_lo = as_int((closer or {}).get("va") or commit_va) or lo
    strings = log_strings(slice_.insns, slice_.strings, min(log_lo, window_end), window_end)
    error_slot = find_error_slot(slice_)

    # 模型侧期望
    fields = [f for f in model.get("fields", []) if not f.get("is_closure") and f.get("seq") != 0]
    expected = []
    for f in fields:
        w = scalar_width(f.get("wire_type"))
        shape = wire_shape(f.get("wire_type"))
        if shape == "fixed_arr":
            shape = "fixed_arr"
        if w is None and shape == "agg":
            # `struct{12}` / `struct{95/缓冲 144}` 是**定宽聚合**：宽度可判，与调用点 `consumed` 对位
            msz = re.match(r"^struct\s*\{\s*(\d+)", str(f.get("wire_type")).strip().lower())
            if msz:
                w = int(msz.group(1))
        expected.append({"name": f.get("name"), "wire_type": f.get("wire_type"),
                         "width": w, "seq": f.get("seq"), "shape": shape,
                         "evidence_va": f.get("evidence_va")})

    # 对位：期望定宽字段 ↔ 汇编读写事件（LCS，容忍两侧插入）
    seq_actual = [p for p in prims
                  if p["kind"] in ("read", "write", "composite", "bounded", "opaque", "blob")]
    seq_actual += collect_inline_stores(slice_, lo, hi or window_end)
    seq_actual.sort(key=lambda p: as_int(p["va"]) or 0)
    # 成员级下钻：`父.成员` 的宽度由「父读取器体内部的线读」凑（2×u32 记成 u64 是常态）。
    #   父 ↔ 读取器调用点的对应关系取自**顶层 LCS 的对位结果**，比按出现次序硬配稳。
    groups = member_groups(expected)
    member_idx = {i for g in groups for i in g["idx"]}
    top_expected = [e for i, e in enumerate(expected) if i not in member_idx]
    # 对齐序列 = 顶层原语 + 「父调用点之后紧邻的内部线读并段」（定长数组字段就靠并段对上）
    align_actual = []
    for p in seq_actual:
        align_actual.append(p)
        runs = merge_nested_runs([n for n in (p.get("nested") or [])
                                  if not n.get("trip_unknown")])
        for r in runs:
            align_actual.append(dict(r, nested_of=p["va"]))
    align = align_widths(top_expected, align_actual)
    pairs = list(align["pairs"])
    gaps = list(align["gaps"])
    prim_by_va = {p["va"]: p for p in seq_actual}
    nested_res = {"gaps": [], "unmatchable": []}
    pairs_by_field = {p["field"]: p for p in align["pairs"]}
    exp_order = {str(e.get("name")): i for i, e in enumerate(expected)}

    def _parent_prim(group):
        """成员组的父读取器，三种找法（按可靠性递减）：

        ① 父名是字段且已对位 → 直接用该调用点；
        ② 父名只是通配（如 `clan_*`）→ 用它之前**最近一个已对位的聚合**调用点；
        ③ 还没有对位（父聚合线长与读取器实读不符等）→ 取窗口内**第一个**内部线读
           字节数足够容纳本组成员的读取器调用点（避免成员级判定整组落空）。
        """
        pair = pairs_by_field.get(group["parent"])
        if pair:
            return prim_by_va.get(pair["va"]), "parent_field"
        gi = exp_order.get(str(group["members"][0].get("name")), 0)
        want = sum(m["width"] for m in group["members"] if m["width"] is not None)
        best = None
        for p in align["pairs"]:
            if exp_order.get(str(p["field"]), -1) < gi:
                cand = prim_by_va.get(p["va"])
                if cand and cand.get("nested"):
                    best = cand
        if best:
            return best, "nearest_aggregate"
        for p in seq_actual:
            if p["va"] in used_prim_vas or not p.get("nested"):
                continue
            eff = _prim_consumed(p)
            if eff is not None and (not want or eff >= want):
                used_prim_vas.add(p["va"])
                return p, "by_capacity"
        return None, None

    used_prim_vas = set()
    parent_facts = {}
    for g in groups:
        prim, how = _parent_prim(g)
        if prim is None:
            nested_res["unmatchable"].append(
                {"parent": g["parent"],
                 "reason": "找不到该成员组的父读取器调用点（父聚合未对位，且之前无已对位的聚合字段）"})
            continue
        reads = [n for n in (prim.get("nested") or []) if not n.get("trip_unknown")]
        sub = match_members(g, reads, prim)
        for p in sub["pairs"]:
            p["parent_source"] = how
        pairs += sub["pairs"]
        gaps += sub["gaps"]
        nested_res["unmatchable"] += sub["unmatchable"]
        parent_facts[g["parent"]] = {"prim": prim, "how": how,
                                     "members": g["members"], "sub": sub}
    # 「聚合整体宽度对不上、但成员逐个都对上」——读取器往往读得比该字段多（尾部还有别的
    #   结构/未声明字段），此时以**成员级证据**为准，把父字段的缺口改记为已复核。
    for name, fact in parent_facts.items():
        if any(x["field"] == name for x in gaps) is False:
            continue
        members = [m for m in fact["members"] if m["width"] is not None]
        ok = [p for p in fact["sub"]["pairs"]]
        if not members or len(ok) != len(members):
            continue
        pw = next((e["width"] for e in expected if str(e.get("name")) == name), None)
        eff = _prim_consumed(fact["prim"])
        gaps = [x for x in gaps if x["field"] != name]
        pairs.append({"field": name, "width": pw, "shape": "agg",
                      "va": fact["prim"]["va"], "kind": "aggregate_members",
                      "members": [p["field"] for p in ok],
                      "note": "聚合整体 %s vs 读取器实读 %s：成员逐一在读取器内部对上，"
                              "以成员级证据为准（多出的字节属于读取器尾部的其他结构）"
                              % (pw, eff)})
    nested_flat = [dict(n, kind="nested", name="", wire_type=None, consumed=n["width"])
                   for p in seq_actual for n in (p.get("nested") or [])
                   if not n.get("trip_unknown")]
    actual_view = seq_actual + nested_flat
    actual_view.sort(key=lambda p: as_int(p["va"]) or 0)
    # C→S 的写线多在复合写入器内部（`consumed` 未知），此时定宽对位不可判定 →
    # 降级为提示，不计入 mismatch（否则每条 C→S 都是假阳性）。
    interior_unknown = any(
        p["kind"] in ("composite", "bounded", "blob", "opaque") and _prim_consumed(p) is None
        for p in seq_actual)
    unverifiable_scalars = (direction == "CS" and interior_unknown)
    widths_check = {
        "direction": direction,
        "expected": expected,
        "actual": [{"va": p["va"], "kind": p["kind"], "width": p["width"],
                    "wire_type": p.get("wire_type"), "name": p.get("name"),
                    "consumed": p.get("consumed"),
                    "consumed_effective": p.get("consumed_effective"),
                    "nested_of": p.get("nested_of")} for p in actual_view],
        "matched": len(pairs),
        "checkable": align["checkable"] + sum(1 for g in groups
                                              for m in g["members"] if m["width"] is not None),
        "pairs": pairs,
        "gaps": gaps,
        "unmatched_actual": align["unmatched_actual"],
        "nested_unmatchable": nested_res["unmatchable"],
        "window": [hx(lo), hx(hi)],
        "scalar_match_verifiable": not unverifiable_scalars,
        "capacity_relation": capacity_relation(seq_actual, direction,
                                               as_int((cap or {}).get("value")) if cap else None),
    }

    # 零负载：无任何读写原语（不透明读取器不算「有字段读写」）
    zero_load = not any(p["kind"] in ("read", "write", "inline_store") for p in
                        (seq_actual + nested_flat))

    # 模型 vs 汇编 差异
    mismatches = []
    notes = []

    m_cap = as_int(model.get("capacity"))
    if cap:
        if m_cap is None:
            notes.append({"check": "capacity", "note": "模型无容量，汇编取到 %s（建议回填）" % hex(cap["value"])})
        elif m_cap != cap["value"]:
            mismatches.append({"check": "capacity", "model": model.get("capacity"),
                               "model_value": m_cap, "asm": hex(cap["value"]),
                               "va": cap["va"], "alloc_va": cap["alloc_va"]})
    elif m_cap is not None:
        mismatches.append({"check": "capacity", "model": model.get("capacity"),
                           "asm": None, "va": None,
                           "note": "未命中分配器指纹（疑零负载/或分配点不在块内）"})

    m_closer = as_int(model.get("closer_va"))
    if closer:
        # README 的「闭合点」有五种记法（本工具全认，命中即算过）：
        #   ① cmp 址（本工具规范口径）；② 紧随的 jcc 址；③ 闭合序列起点；
        #   ④ 收尾/释放调用点（`call sub_B41110`）与 C→S 的提交点 —— 批次 1 两例即此写法；
        #   ⑤ 跳转落点（jcc 的目标标签，即「校验通过后落到的那条」）。
        conventions = [(closer["va"], "cmp"), (closer.get("jcc_va"), "jcc"),
                       (closer.get("seq_va"), "seq"), (closer.get("jcc_dst"), "jcc_target")]
        if rel:
            conventions.append((hx(rel), "release_call"))
        if commit_va:
            conventions.append((hx(commit_va), "commit"))
        hit = next((k for v, k in conventions if v and as_int(v) == m_closer), None)
        if hit:
            closer["va_convention"] = hit
        if m_closer is None:
            notes.append({"check": "closer", "note": "模型无闭合点，汇编取到 %s(%s)（建议回填）"
                          % (closer["va"], closer["kind"])})
        elif hit is None:
            mismatches.append({"check": "closer", "model": model.get("closer_va"),
                               "asm": closer["va"], "kind": closer["kind"],
                               "note": "模型记的既不是 cmp 址、jcc 址、闭合序列起点、跳转落点，"
                                       "也不是收尾/提交调用点（五种记法都认，仍对不上）"})
    elif m_closer is not None:
        mismatches.append({"check": "closer", "model": model.get("closer_va"), "asm": None,
                           "note": "窗口内未找到闭合点"})

    m_slot = model.get("dispatch_slot")
    if disp:
        if not m_slot:
            notes.append({"check": "dispatch_slot", "note": "模型无去向槽，汇编取到 %s（建议回填）" % disp["slot"]})
        elif norm_slot(m_slot) != norm_slot(disp["slot"]):
            mismatches.append({"check": "dispatch_slot", "model": m_slot, "asm": disp["slot"],
                               "va": disp["va"]})
        # 去向 VA：口径不统一（部分 README 记 `mov R,[vt]` 的址，部分记 `call R` 的址）→ 两址皆认
        m_dva = as_int(model.get("dispatch_va"))
        if m_dva is not None and m_dva not in (as_int(disp["va"]), as_int(disp.get("mov_va"))):
            mismatches.append({"check": "dispatch_va", "model": model.get("dispatch_va"),
                               "asm": disp["va"], "asm_mov": disp.get("mov_va"),
                               "note": "模型记的既不是 call 址也不是 mov 址"})
    elif m_slot:
        mismatches.append({"check": "dispatch_slot", "model": m_slot, "asm": None,
                           "note": "未找到去向虚表调用"})

    # 容量 vs 观测线长（硬不变量：下界超容量 ⇒ 一定多算了字段）
    caprel = widths_check["capacity_relation"]
    if caprel["relation"] == "over":
        mismatches.append({"check": "capacity_relation", "model": model.get("capacity"),
                           "asm": hex(caprel["capacity"]),
                           "note": "观测线长下界 %d > 容量 %s：字段宽度/条数必有高估"
                                   % (caprel["observed_min"], hex(caprel["capacity"]))})

    mblk = model.get("block")
    win_ok = True
    if mblk and len(mblk) == 2:
        mlo, mhi = as_int(mblk[0]), as_int(mblk[1])
        if guard and not (mlo <= as_int(guard["va"]) <= mhi):
            win_ok = False
            mismatches.append({"check": "field_window", "model": mblk, "asm": guard["va"],
                               "note": "守卫不在模型块范围内"})
        if closer and closer["kind"] in ("jz", "jnz") and not (mlo <= as_int(closer["va"]) <= mhi):
            win_ok = False
            mismatches.append({"check": "field_window", "model": mblk, "asm": closer["va"],
                               "note": "闭合点不在模型块范围内"})

    scalar_gaps = [g for g in gaps if g.get("width") or g.get("shape") == "str"]
    gaps_unexplained, gaps_in_reader = [], []
    for g in scalar_gaps:
        rec = next((f for f in model.get("fields", []) if f.get("name") == g["field"]), None)
        ex = gap_explained_by_reader(slice_, rec, prims) if rec else None
        if ex:
            gaps_in_reader.append(dict(g, reader=ex))
        else:
            gaps_unexplained.append(g)
    if not zero_load and gaps_unexplained and not unverifiable_scalars:
        asm_cands = [{"va": p["va"], "name": p.get("name"), "kind": p["kind"],
                      "consumed": _prim_consumed(p)}
                     for p in seq_actual if p["kind"] in ("composite", "opaque", "bounded")]
        mismatches.append({"check": "primitive_widths",
                           "model": [e["width"] for e in expected],
                           "asm": [p["width"] for p in actual_view],
                           "gaps": gaps_unexplained,
                           "asm_candidates": asm_cands,
                           "note": "定宽字段未能在汇编序列中对位：%s%s"
                                   % (", ".join(g["field"] for g in gaps_unexplained),
                                      "；汇编侧复合读取器：" + ", ".join(
                                          "%s@%s(%sB)" % (c["name"] or "?", c["va"], c["consumed"])
                                          for c in asm_cands) if asm_cands else "")})
    elif not zero_load and (gaps_unexplained or gaps_in_reader):
        notes.append({"check": "primitive_widths",
                      "note": "定宽对位不可判定：C→S 写线在复合写入器内部 consumed 未知；"
                              "缺口 %s" % ", ".join(g["field"] for g in gaps_unexplained)})
    if gaps_in_reader:
        notes.append({"check": "primitive_widths",
                      "note": "证据 VA 落在读取器函数体内（读在读取器内部，调用点不可定宽）：%s"
                              % ", ".join("%s←%s" % (g["field"], (g["reader"] or {}).get("callee"))
                                          for g in gaps_in_reader)})

    # 字段名 vs 日志串对位（证据强度，不算 mismatch）
    names = {str(f.get("name")) for f in fields if f.get("name")}
    hits = []
    for s in strings:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)", s)
        if m and m.group(1) in names:
            hits.append(m.group(1))

    checks = {
        "capacity": cap,
        "field_window": {
            "start_va": hx(lo), "end_va": hx(hi),
            "guard": guard, "closer_or_commit_va": (closer or {}).get("va"),
            "within_model_block": win_ok,
            "range_from": slice_.range_from,
        },
        "primitive_widths": widths_check,
        "closer": closer,
        "dispatch_slot": dict(disp or {}, error_slot=error_slot) if disp else None,
        "log_strings": strings,
    }
    if zero_load:
        checks["primitive_widths"]["zero_load"] = True
        # 零负载命令：模型同样没有容量/闭合/去向 ⇒ 「双方都无」视为已核对（缺省一致）
        for k, mkey in (("capacity", "capacity"), ("closer", "closer_va"),
                        ("dispatch_slot", "dispatch_slot")):
            if checks.get(k) is None and not model.get(mkey):
                checks[k] = {"absent": True, "reason": "零负载命令：无字段 ⇒ 无容量/闭合点/去向"}

    result = {
        "id": slice_.id,
        "verified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "extractor": EXTRACTOR,
        "ida_script": IDA_SCRIPT,
        "range_from": slice_.range_from,
        "block": [hx(slice_.block[0]), hx(slice_.block[1])],
        "block_truncated": slice_.block_truncated,
        "checks": checks,
        "mismatches": mismatches,
        "notes": notes,
        "log_name_hits": sorted(set(hits)),
    }
    result["status"] = decide_status(result, apply_=False)
    return result


SIX_CHECKS = ("capacity", "field_window", "primitive_widths", "closer",
              "dispatch_slot", "log_strings")
# 这四类是「值/址记账」差异：`--apply` 用汇编值落库即可闭合（旧值留 previous）
RESOLVABLE_CHECKS = {"capacity", "closer", "dispatch_slot", "dispatch_va"}


def is_resolvable(m: dict) -> bool:
    """该差异能否靠「以汇编为准回填」闭合（不能的是**结构性**差异，须人工）。"""
    return m.get("check") in RESOLVABLE_CHECKS and m.get("asm") is not None


def decide_status(res: dict, apply_: bool) -> str:
    """状态阶梯：六项 check 全非空 + 无（不可消解的）差异 ⇒ ASM-VERIFIED。"""
    checks = res.get("checks") or {}
    if any(checks.get(k) is None for k in SIX_CHECKS):
        return "IMPORTED"
    ms = res.get("mismatches") or []
    if not ms:
        return "ASM-VERIFIED"
    if apply_ and all(is_resolvable(m) for m in ms):
        return "ASM-VERIFIED"
    return "IMPORTED"


def diffs_closed_by_apply(res: dict, apply_: bool) -> bool:
    """有差异、但差异全是「可回填项」且本次已 `--apply` ⇒ 已闭合，不必人工看。"""
    ms = res.get("mismatches") or []
    return bool(ms) and apply_ and all(is_resolvable(m) for m in ms)


# ---------------------------------------------------------------- 回填

def backfill(cmd: dict, res: dict, apply_: bool) -> dict:
    """把复核结果写回命令模型。默认**只补空**；`--apply` 才用汇编值覆盖模型值。

    覆盖时原值写进 `asm_verification.previous`（口径：长期记忆 §2「发现矛盾时保留原结论」）。
    """
    checks = res["checks"]
    cap = checks.get("capacity")
    closer = checks.get("closer")
    disp = checks.get("dispatch_slot")
    blk = res.get("block") or []

    filled: list[str] = []
    previous: dict[str, object] = {}

    def _set(key, val, va_key=None, va=None):
        if val is None:
            return
        old = cmd.get(key)
        if old in (None, "", "?"):
            cmd[key] = val
            filled.append(key)
            if va_key and va and cmd.get(va_key) in (None, ""):
                cmd[va_key] = va
                filled.append(va_key)
        elif apply_ and str(old) != str(val):
            previous[key] = old
            cmd[key] = val
            filled.append(key + "(override)")
            if va_key and va:
                if cmd.get(va_key) not in (None, ""):
                    previous[va_key] = cmd.get(va_key)
                cmd[va_key] = va

    # `checks.*` 有三种形态：正常结论 / `None`（无该线索）/ `{"absent": True}`（零负载命令的
    # 「双方都无」）。后两种没有 value/va/slot 键，回填时必须跳过，不能直接下标。
    if cap and cap.get("value") is not None:
        _set("capacity", "0x%X" % cap["value"], "capacity_va", cap.get("va"))
    if closer and closer.get("va"):
        _set("closer_va", closer["va"])
    if disp and disp.get("slot"):
        _set("dispatch_slot", disp["slot"], "dispatch_va", disp.get("va"))
    if not cmd.get("block") and len(blk) == 2 and blk[0] and blk[1]:
        cmd["block"] = [blk[0], blk[1]]
        filled.append("block")

    cmd["asm_verification"] = {
        "status": decide_status({"checks": checks, "mismatches": res["mismatches"]}, apply_),
        "verified_at": res["verified_at"],
        "batch": res.get("batch"),
        "extractor": EXTRACTOR,
        "checks": checks,
        "mismatches": res["mismatches"],
        "notes": res.get("notes") or [],
        "resolved_by_apply": (sorted({m["check"] for m in res["mismatches"] if is_resolvable(m)})
                              if apply_ else []),
        "evidence_file": "commands/_verify/%s.json" % res["id"],
        "previous": previous or None,
        "filled": sorted(set(filled)),
    }
    # 回填动了 `capacity`/`closer_va`/`dispatch_slot`/`block` —— 这些都在
    # `check_fingerprint` 的覆盖面内。不同步重算，存根声明的「判定输入」就与实际模型不符，
    # 下次导入会拿错误的输入指纹去比（坑㉟ 的另一半）。
    cmd["check_fingerprint"] = _recompute_check_fingerprint(cmd)
    return cmd


def update_index(commands: list[dict]) -> None:
    """就地更新 schema/commands/index.json 的 status 与统计。"""
    idx_path = CMD_DIR / "index.json"
    if not idx_path.is_file():
        return
    index = load_json(idx_path)
    by_id = {c["id"]: c for c in index.get("commands", [])}
    for c in commands:
        e = by_id.get(c["id"])
        if e is None:
            continue
        av = c.get("asm_verification") or {}
        e["status"] = av.get("status", e.get("status", "IMPORTED"))
        e["capacity"] = c.get("capacity")
        e["closer_va"] = c.get("closer_va")
        e["dispatch_slot"] = c.get("dispatch_slot")
        e["asm_mismatches"] = len(av.get("mismatches") or [])
    by_status: dict[str, int] = {}
    for c in index.get("commands", []):
        s = c.get("status", "IMPORTED")
        by_status[s] = by_status.get(s, 0) + 1
    index.setdefault("counts", {})["by_status"] = by_status
    index["counts"]["asm_mismatch_commands"] = sum(
        1 for c in index.get("commands", []) if c.get("asm_mismatches"))
    index["verified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dump_json(idx_path, index)


# ---------------------------------------------------------------- 批次计划

PROTO_WEIGHT = {"auth": 60, "lounge": 30, "battle": 0}


def build_priority() -> dict:
    """优先级：实体线宽形态（PERSIST 载体）> 提议表证据命令 > 协议类权重。"""
    score: dict[str, int] = {}

    def bump(cid: str, n: int, tag: str):
        score[cid] = score.get(cid, 0) + n

    ent_dir = SCHEMA / "entities"
    if ent_dir.is_dir():
        for p in sorted(ent_dir.glob("*.json")):
            ent = load_json(p)
            persist = sum(1 for f in ent.get("fields", []) if f.get("disposition") == "PERSIST")
            for wf in ent.get("wire_forms", []):
                for cid in wf.get("commands", []) or []:
                    bump(cid, 40 + min(persist, 20), "entity")
    tbl_dir = SCHEMA / "_legacy_tables"
    if tbl_dir.is_dir():
        for p in sorted(tbl_dir.glob("*.json")):
            tbl = load_json(p)
            for cid in tbl.get("evidence_commands", []) or []:
                bump(cid, 20, "table")
    return score


def plan(args) -> None:
    cmds = load_all_commands()
    prio = build_priority()
    pool = []
    for c in cmds:
        av = c.get("asm_verification") or {}
        if av.get("status") in ("ASM-VERIFIED", "BEHAVIOR-DONE") and not args.redo:
            continue
        if args.proto and c.get("proto") not in args.proto:
            continue
        if args.direction and c.get("direction") not in args.direction:
            continue
        if args.only and c["id"] not in args.only:
            continue
        sc = prio.get(c["id"], 0) + PROTO_WEIGHT.get(c.get("proto") or "", 0)
        pool.append((sc, as_int(c.get("opcode")) or 0, c["id"]))
    pool.sort(key=lambda x: (-x[0], x[1], x[2]))
    picked = pool[:args.size] if not args.only else pool

    batch = args.batch
    if batch is None:
        batch = 1
        while (META_DIR / ("batch_%d.json" % batch)).is_file():
            batch += 1

    work = {
        "batch": batch,
        "created": date.today().isoformat(),
        "size": len(picked),
        "criteria": {
            "proto": args.proto, "direction": args.direction, "only": args.only,
            "min_score": picked[-1][0] if picked else None,
        },
        "targets": [{"id": cid, "score": sc, "opcode": "0x%04X" % op}
                    for sc, op, cid in picked],
    }
    dump_json(META_DIR / ("batch_%d.json" % batch), work)

    by_id = {c["id"]: c for c in cmds}
    lines = ["# 批次 %d 复核清单" % batch, "",
             "> 由 `tools/verify_commands_ida.py plan` 生成；口径见 `docs/01-命令模型.md`。",
             "> 优先级 = 实体线宽形态（PERSIST 载体，+40~60）> 提议表证据命令（+20）> 协议类权重（auth 60 / lounge 30 / battle 0）。",
             "", "共 **%d** 条。" % len(picked), "",
             "| # | 命令 | 方向 | 协议类 | opcode | 优先级 | 容量 | 字段 | 状态 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for i, (sc, op, cid) in enumerate(picked, 1):
        c = by_id.get(cid, {})
        lines.append("| %d | <code>%s</code> | %s | %s | %s | %d | %s | %d | %s |" % (
            i, cid, c.get("direction", ""), c.get("proto", ""), c.get("opcode", ""), sc,
            c.get("capacity") or "—", (c.get("wire") or {}).get("field_count", 0),
            ((c.get("asm_verification") or {}).get("status") or "")))
    (META_DIR / ("批次-%d-清单.md" % batch)).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("[plan] 批次 %d：%d 条 → %s" % (batch, len(picked),
                                          META_DIR / ("batch_%d.json" % batch)))
    dist: dict[str, int] = {}
    for sc, op, cid in picked:
        p = by_id.get(cid, {}).get("proto", "?")
        dist[p] = dist.get(p, 0) + 1
    print("[plan] 协议类分布：%s" % dist)


def emit(args) -> None:
    work = load_json(META_DIR / ("batch_%d.json" % args.batch))
    cmds = {c["id"]: c for c in load_all_commands()}
    targets = []
    for t in work["targets"]:
        c = cmds.get(t["id"])
        if c is None:
            continue
        targets.append({
            "id": c["id"], "direction": c.get("direction"), "proto": c.get("proto"),
            "opcode": c.get("opcode"), "block": c.get("block"),
            "handler_va": c.get("handler_va"),
        })
    job = {
        "batch": args.batch,
        "out_dir": str(RAW_DIR),
        "insn_cap": args.insn_cap,
        "callee_insn_cap": args.callee_cap,
        "targets": targets,
    }
    dump_json(JOB_PATH, job)
    for t in targets:
        if not t.get("block") and not t.get("handler_va"):
            print("[emit][WARN] %s 既无 block 也无 handler_va，IDA 侧会跳过" % t["id"])
    print("[emit] 作业写出 %d 条 → %s" % (len(targets), JOB_PATH))
    print("[emit] 下一步：在 IDA MCP 里执行 py_exec_file")
    print("       file_path = F:\\9ymsgo\\9you\\db_design\\tools\\ida_verify_batch.py")
    print("       产出：%s\\<命令 id>.json" % RAW_DIR)
    print("       然后：python tools/verify_commands_ida.py ingest --batch %d" % args.batch)


def load_all_commands() -> list[dict]:
    out = []
    for p in sorted(CMD_DIR.glob("*.json")):
        if p.name.startswith("_") or p.name == "index.json":
            continue
        out.append(load_json(p))
    return out


def ingest(args) -> None:
    work = load_json(META_DIR / ("batch_%d.json" % args.batch))
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    missing = []
    for t in work["targets"]:
        cid = t["id"]
        raw = RAW_DIR / (cid + ".json")
        cmd_path = CMD_DIR / (cid + ".json")
        if not raw.is_file() or not cmd_path.is_file():
            missing.append(cid)
            continue
        slice_ = Slice(load_json(raw))
        cmd = load_json(cmd_path)
        res = analyze(slice_, cmd)
        res["batch"] = args.batch
        dump_json(VERIFY_DIR / (cid + ".json"), res)
        cmd = backfill(cmd, res, apply_=args.apply)
        dump_json(cmd_path, cmd)
        results.append((cmd, res))

    if results:
        update_index([c for c, _ in results])

    write_todo_list(results)
    report(results, missing, args)


def report(results, missing, args) -> None:
    n = len(results)
    apply_ = bool(getattr(args, "apply", False))
    ver = [r for _c, r in results if decide_status(r, apply_) == "ASM-VERIFIED"]
    manual = [(c, r) for c, r in results
              if (r.get("mismatches") or []) and not diffs_closed_by_apply(r, apply_)]
    partial = [(c, r) for c, r in results
               if decide_status(r, apply_) != "ASM-VERIFIED" and not (r.get("mismatches") or [])]
    print("[ingest] 批次 %d：分析 %d 条%s" % (args.batch, n, "（--apply）" if apply_ else ""))
    print("  ASM-VERIFIED %d / 须人工或未闭合 %d / 六项未齐 %d / 缺原始切片 %d"
          % (len(ver), len(manual), len(partial), len(missing)))
    if partial:
        print("  六项未齐（多为守卫/去向规则未覆盖，需迭代规则）：%s%s"
              % (", ".join(c["id"] for c, _r in partial[:6]), " …" if len(partial) > 6 else ""))
    if missing:
        print("  缺切片（先在 IDA 里跑 ida_verify_batch.py）：%s%s"
              % (", ".join(missing[:6]), " …" if len(missing) > 6 else ""))
    kinds: dict[str, int] = {}
    for _c, r in manual:
        for m in r["mismatches"]:
            kinds[m["check"]] = kinds.get(m["check"], 0) + 1
    if kinds:
        print("  差异分类：%s" % kinds)
    for c, r in manual[:10]:
        for m in r["mismatches"][:2]:
            print("    - %s %s：model=%r asm=%r" % (c["id"], m["check"], m.get("model"), m.get("asm")))


def write_todo_list(results) -> None:
    """差异汇入 `_meta/待复核清单.md`（按检查项分组，带 VA，可直接跳 IDA）。"""
    rows: list[str] = []
    mism = [(c, r) for c, r in results if r["mismatches"]]
    for c, r in sorted(mism, key=lambda x: x[0]["id"]):
        for m in r["mismatches"]:
            rows.append("| <code>%s</code> | %s | %s | %s | %s | %s |" % (
                c["id"], m.get("check"),
                str(m.get("model"))[:60].replace("|", "\\|"),
                str(m.get("asm"))[:60].replace("|", "\\|"),
                "可回填" if is_resolvable(m) else "**须人工**",
                (m.get("va") or m.get("note") or "")[:70].replace("|", "\\|")))
    lines = [
        "# 待复核清单（IDA 汇编 ↔ 命令模型 差异）",
        "",
        "> 由 `tools/verify_commands_ida.py ingest` 生成，**每批重写**。",
        "> 「可回填」= 值/址记账差异，`ingest --apply` 即闭合（旧值留在 `asm_verification.previous`）；",
        "> 「须人工」= 结构性差异（字段宽度对位 / 字段窗口 / 容量下界超限），必须看汇编改模型。",
        "",
        "生成时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "",
        "| 命令 | 检查项 | 模型值 | 汇编值 | 处置 | VA / 说明 |",
        "|---|---|---|---|---|---|",
    ]
    lines += rows or ["| — | — | — | — | 本批无差异 |"]
    lines += ["", "## 按检查项统计", ""]
    kinds: dict[str, int] = {}
    for _c, r in mism:
        for m in r["mismatches"]:
            kinds[m["check"]] = kinds.get(m["check"], 0) + 1
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        lines.append("- `%s`：%d" % (k, v))
    if not kinds:
        lines.append("- （无）")
    (META_DIR / "待复核清单.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def status(args) -> None:
    cmds = load_all_commands()
    by_status: dict[str, int] = {}
    mism_by_check: dict[str, int] = {}
    n_mismatch_cmds = 0
    for c in cmds:
        av = c.get("asm_verification") or {}
        s = av.get("status", "IMPORTED")
        by_status[s] = by_status.get(s, 0) + 1
        ms = av.get("mismatches") or []
        if ms:
            n_mismatch_cmds += 1
            for m in ms:
                mism_by_check[m.get("check", "?")] = mism_by_check.get(m.get("check", "?"), 0) + 1
    print("[status] 命令模型 %d 条" % len(cmds))
    for k, v in sorted(by_status.items(), key=lambda x: -x[1]):
        print("  %-14s %d" % (k, v))
    print("[status] 有差异的命令 %d" % n_mismatch_cmds)
    for k, v in sorted(mism_by_check.items(), key=lambda x: -x[1]):
        print("  %-20s %d" % (k, v))
    if by_status.get("IMPORTED"):
        print("[status] 下一步：plan → emit → （IDA）→ ingest")


# ---------------------------------------------------------------- 自检

def selftest(args) -> None:
    """对 `_raw/` 里已有的切片跑分析，只打印、不写文件（规则迭代用）。"""
    files = sorted(RAW_DIR.glob("*.json"))
    if not files:
        print("[selftest] %s 下没有切片，先跑 emit + IDA" % RAW_DIR)
        return
    n_ok = 0
    for p in files:
        slice_ = Slice(load_json(p))
        cmd_path = CMD_DIR / (slice_.id + ".json")
        model = load_json(cmd_path) if cmd_path.is_file() else {}
        res = analyze(slice_, model)
        ch = res["checks"]
        # `checks.*` 有三种形态：正常结论 / `None`（无该线索）/ `{"absent": True}`（零负载命令的
        # 「双方都无」）。后两种没有 value/va/slot 键，打印时不能直接下标或 `.get("value")` 取整。
        cap = ch["capacity"] if isinstance(ch["capacity"], dict) else {}
        cl = ch["closer"] if isinstance(ch["closer"], dict) else {}
        dp = ch["dispatch_slot"] if isinstance(ch["dispatch_slot"], dict) else {}
        win = ch["field_window"] or {}
        cap_repr = "absent（零负载）" if cap.get("absent") else (
            hex(cap["value"]) if cap.get("value") is not None else None)
        print("=" * 100)
        print("%s  [%s]  status=%s" % (slice_.id, slice_.direction, res["status"]))
        print("  capacity : %s @ %s  (host %s, alloc %s)  model=%s" % (
            cap_repr, cap.get("va"), cap.get("host"),
            cap.get("alloc_va"), model.get("capacity")))
        print("  guard    : %s module=%s   window=%s..%s" % (
            (win.get("guard") or {}).get("va"), (win.get("guard") or {}).get("module_id"),
            win.get("start_va"), win.get("end_va")))
        print("  closer   : %s (%s)  model=%s" % (
            cl.get("va") or ("absent" if cl.get("absent") else None),
            cl.get("kind"), model.get("closer_va")))
        print("  dispatch : %s @ %s argc=%s  err=%s  model=%s" % (
            dp.get("slot") or ("absent" if dp.get("absent") else None),
            dp.get("va"), dp.get("argc"),
            (dp.get("error_slot") or {}).get("slot"), model.get("dispatch_slot")))
        pw = ch["primitive_widths"]
        print("  widths   : expected=%s" % [w.get("width") for w in pw["expected"]])
        print("             actual  =%s" % ["%s%s" % (p["kind"][0], p["width"] if p["width"] else
                                                     (p.get("consumed") or "?")) for p in pw["actual"]])
        print("  strings  : %s" % ch["log_strings"][:12])
        for m in res["mismatches"]:
            print("  MISMATCH %s: model=%r asm=%r %s" % (m["check"], m.get("model"), m.get("asm"),
                                                         m.get("note") or ""))
        for m in res.get("notes", []):
            print("  note     %s: %s" % (m["check"], m["note"]))
        if res["status"] == "ASM-VERIFIED":
            n_ok += 1
    print("=" * 100)
    print("[selftest] %d/%d 命中 ASM-VERIFIED（其余为有差异或规则未覆盖，见上）" % (n_ok, len(files)))


# ---------------------------------------------------------------- CLI

def main() -> None:
    ap = argparse.ArgumentParser(description="IDA 汇编复核器（命令模型六项检查）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan", help="挑批次清单（优先级：实体/表/协议类）")
    p.add_argument("--batch", type=int, default=None)
    p.add_argument("--size", type=int, default=50)
    p.add_argument("--proto", nargs="*", default=None)
    p.add_argument("--direction", nargs="*", default=None, choices=["SC", "CS"])
    p.add_argument("--only", nargs="*", default=None, help="指定命令 id（忽略 size）")
    p.add_argument("--redo", action="store_true", help="已 ASM-VERIFIED 的也纳入")
    p.set_defaults(func=plan)

    p = sub.add_parser("emit", help="写 IDA 作业文件 _meta/_verify_job.json")
    p.add_argument("--batch", type=int, required=True)
    p.add_argument("--insn-cap", type=int, default=1500)
    p.add_argument("--callee-cap", type=int, default=400)
    p.set_defaults(func=emit)

    p = sub.add_parser("ingest", help="读原始切片 → 六项检查 → 回填模型")
    p.add_argument("--batch", type=int, required=True)
    p.add_argument("--apply", action="store_true",
                   help="用汇编值覆盖模型值（默认只补空，差异仅记录）")
    p.set_defaults(func=ingest)

    p = sub.add_parser("status", help="状态分布")
    p.set_defaults(func=status)

    p = sub.add_parser("selftest", help="对已有切片跑规则并打印（不写文件）")
    p.set_defaults(func=selftest)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

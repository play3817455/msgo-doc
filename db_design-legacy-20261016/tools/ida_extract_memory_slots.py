r"""Run inside IDA via MCP py_exec_file.

Extract buffer slot offsets (a1+N) from decompiled reader/writer functions.
Output: schema/_meta/ida_memory_slots_batch{N}.json

★ 这个文件是 `audit_memory_chain.py` 的**唯一证据来源**。它漏抽一种写法，审计就会把
**正确**的 `memory_offset` 报成错（2026-09-24：40 条假阳性全部源于此，没有一条是偏移填错）。
所以每补一种写法都要在 `_selftest_ida_slots.py` 里放一段**真伪代码**夹具，并在
`_selftest_memory_audit.py` 里保证审计**还会说「不」**。

覆盖的写法（都由夹具钉住）：

| # | 伪代码形态 | 例子 |
|---|---|---|
| ③ | 裸 `a1` ＝ 偏移 0 | `*(_DWORD *)a1` / `*a1` |
| ④ | 无转型 `a1 + N` | `sub_B02DD0(a1 + 32, …)`（偏移 = N × a1 的声明步长） |
| ⑤ | 定长文本槽循环，**三种次序** + **可选转型**，收尾允许逗号 | `*(_BYTE *)(i + a1 + 12)` / `sub_B061C0(a1 + v5 + 80, a2)` / `((_BYTE *)a1 + v10 + 204)` |
| ⑥ | 下标 `a1[…]`，走通用下标求值 `index_range` | `*(_DWORD *)&a1[2 * v2 + 2 + 2 * i]`（`_WORD *a1`） |
| ⑥b | 元素数组循环 `a1 + K * (V + W)`，**下标起点可以非 0** | `v29 = 47; … a1 + 4 * (v29 + v30)` |
| ⑦ | 已知 helper 调用（顺带记槽宽） | `sub_B06290(a1 + 52, a2)` |

三处**换算/映射判据**也是踩过坑才定下来的：

* `(_T *)a1 + N` ⇒ 偏移 = `N × sizeof(_T)`（转型**先**发生）。旧实现一律 ×4，
  于是 `*((_WORD *)a1 + 1)` 明明是字节 2 被算成 4（`total_result_wave.rank` 就是被这条顶掉的）。
* `*(_T *)(a1 + N)` ⇒ 加法发生在 a1 自己的类型上，先按 a1 的声明类型换 N 个元素，再看转型。
* 带转型的文本槽（`(_BYTE *)a1 + v + 204`）里 204 是**字节**偏移，再乘 a1 的步长会算成 816。
* `total_result_wave` 曾**映射到别的函数**（`sub_B45580`，真 reader 是 `sub_B45650`）。

另有两条实现约束：

* **只扫函数体**：签名行里的 `(_DWORD *a1, int a2)` 含子串 `*a1`，会把偏移 0 变出一条假证据。
* `index_range` 取**凸包**：各项步长不同时和集可能有洞（`{0,64,128,192} + {2,…,64}`），
  按「范围内、步长 = 各项 gcd」摊开，用于判定「该偏移属于此数组」够用，且不会放到数组外。
"""

from __future__ import annotations

import json
import math
import re
import sys

import idc

try:
    from ida_hexrays import decompile
except ImportError:
    decompile = None

BATCH = sys.argv[1] if len(sys.argv) > 1 else "all"
OUT = rf"F:\9ymsgo\9you\db_design\schema\_meta\ida_memory_slots_batch{BATCH}.json"

HELPER_SLOT = {
    "sub_B068B0": 24,
    "sub_B06290": 18,
    "sub_B06230": 1,
    "sub_B061C0": 1,
    "sub_B02DD0": 4,
    "sub_B02DF0": 2,
    "sub_B02D80": 4,
    "sub_B02DA0": 2,
    "sub_B434F0": 22,
    "sub_B08920": 18,
}

BATCH_FN = {
    "1": {
        "item": "sub_B434F0",
        "ms_set": "sub_B41B10",
        "equip_set": "sub_B41C60",
        "pilot": "sub_B06360",
        "missionunit_set": "sub_B41BF0",
        "roominfo": "sub_B44880",
        "cinfo": "sub_B45940",
        "pilot_detail": "sub_B42640",
        "pilots_list": "sub_B42BB0",
        "pcard": "sub_B42BB0",
    },
    "2": {
        "lpcard": "sub_B43100",
        "ms": "sub_B06D80",
        "snapshot": "sub_B075A0",
        "funnelss": "sub_B081C0",
        "unlockw": "sub_B439D0",
        "adop_list": "sub_B43D90",
        "recruits": "sub_B45400",
        "leaders": "sub_B454D0",
        "bracket": "sub_B47060",
        "AI": "sub_B07230",
    },
    "3": {
        "item_list": "sub_B458A0",
        "party_member_stat": "sub_B432C0",
        "order": "sub_B46420",
        "rankself": "sub_B464A0",
        "ranking": "sub_B46560",
        "special_a_next": "sub_B46CD0",
        "sort_info": "sub_B461E0",
    },
    "4": {
        "ext_subrule": "sub_B456F0",
        "xwar_ext_rule": "sub_B08160",
        "wbonus": "sub_B453B0",
        "buffitem": "sub_B07E70",
        "config": "sub_B077B0",
        "progress": "sub_B07880",
        "bgm_desc": "sub_B07E00",
    },
    "5": {
        "phase_info": "sub_B46D20",
        "bracket_info": "sub_B46D80",
        "buildup_info": "sub_B44050",
        "challenge_info": "sub_B07540",
        "check_quest": "sub_B06C00",
        "wave_res": "sub_B08020",
        "appear_info": "sub_B07EC0",
        "avatar": "sub_B068B0",
    },
    "6": {
        "beginner_challenge_info": "sub_B42440",
        "clan_eff": "sub_B45F30",
        "dailycup_conf": "sub_B46E80",
        "dc_point": "sub_B47120",
        "exam_state": "sub_B42330",
    },
    "7": {
        "intro_info": "sub_B46140",
        "hack_check": "sub_B065D0",
        "lvjudge_hist": "sub_B44750",
        "unlocked_navi": "sub_B434B0",
        "pointdmg": "sub_B45760",
        "total_result_wave": "sub_B45650",
        "recruit": "sub_B45400",
    },
    "8": {
        "replay_info": "sub_B47340",
        "season_rb_conf": "sub_B471E0",
        "precord": "sub_B440B0",
    },
}


_SIZE_OF = {
    "_BYTE": 1, "char": 1, "__int8": 1, "unsigned __int8": 1,
    "_WORD": 2, "short": 2, "__int16": 2, "unsigned __int16": 2,
    "_DWORD": 4, "int": 4, "__int32": 4, "unsigned int": 4, "float": 4,
    "_QWORD": 8, "__int64": 8, "double": 8, "unsigned __int64": 8,
}


def _num(s: str) -> int:
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def _cast_size(name: str) -> int:
    return _SIZE_OF.get(name.strip(), 1)


def a1_elem_size(text: str) -> int:
    """a1 的声明类型步长 —— `a1 + N` 的加法发生在 a1 自己的类型上。"""
    head = text.lstrip("\n\r\t ").split("\n", 1)[0]
    m = re.search(r"([A-Za-z_][\w \t]*?)\s*\*+\s*a1\s*[,)]", head)
    if not m:
        return 1  # `int a1` / `_BYTE *a1` / 认不出 ⇒ 按字节
    return _cast_size(m.group(1))


def loop_bounds(text: str) -> dict[str, int]:
    """循环变量 → 上界字面量（定长文本槽 / 数组循环的槽宽和元素数就是这么来的）。"""
    out: dict[str, int] = {}
    for m in re.finditer(
        r"for\s*\(\s*(\w+)\s*=\s*0\s*;\s*(?:\(unsigned int\))?\s*\1\s*<\s*(0x[0-9a-fA-F]+|\d+)", text
    ):
        out.setdefault(m.group(1), _num(m.group(2)))
    for m in re.finditer(r"\+\+\s*(\w+)\s*>=\s*(0x[0-9a-fA-F]+|\d+)", text):
        out.setdefault(m.group(1), _num(m.group(2)))
    # ★ 2026-09-24 补：「if-continue」风格的外层循环 —— 实测 `pointdmg\sub_B45760`
    # 是 `while(2){ for(i<3){…} v2 += 3; if (v2 < 6) continue; }`，
    # 上界只出现在 `if (V < N)` 里，旧实现看不见 ⇒ 这类数组槽整段丢失。
    for m in re.finditer(r"\bif\s*\(\s*(\w+)\s*<\s*(0x[0-9a-fA-F]+|\d+)\s*\)", text):
        out.setdefault(m.group(1), _num(m.group(2)))
    for m in re.finditer(r"\bwhile\s*\(\s*(\w+)\s*<\s*(0x[0-9a-fA-F]+|\d+)\s*\)", text):
        out.setdefault(m.group(1), _num(m.group(2)))
    return out


def var_starts(text: str) -> dict[str, int]:
    """循环变量初值（`v29 = 47;`）——数组**不一定从下标 0 起**。"""
    out: dict[str, int] = {}
    for m in re.finditer(r"^[ \t]*(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*;$", text, re.M):
        out.setdefault(m.group(1), _num(m.group(2)))
    for m in re.finditer(r"for\s*\(\s*(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*;", text):
        out.setdefault(m.group(1), _num(m.group(2)))
    return out


def var_steps(text: str) -> dict[str, int]:
    """循环变量步长（`v29 += 4;`；自增记 1）。"""
    out: dict[str, int] = {}
    for m in re.finditer(r"\b(\w+)\s*\+=\s*(0x[0-9a-fA-F]+|\d+)\s*;", text):
        out.setdefault(m.group(1), _num(m.group(2)))
    for m in re.finditer(r"\+\+\s*(\w+)", text):
        out.setdefault(m.group(1), 1)
    return out


def loop_values(
    var: str, bounds: dict[str, int], starts: dict[str, int], steps: dict[str, int]
) -> list[int] | None:
    """变量在循环里实际取到的下标集合（推不出上界就返回 None，宁缺毋滥）。"""
    top = bounds.get(var)
    if top is None:
        return None
    step = steps.get(var, 1) or 1
    v, vals = starts.get(var, 0), []
    while v < top and len(vals) < 256:
        vals.append(v)
        v += step
    return vals or None


def index_range(
    expr: str, bounds: dict[str, int], starts: dict[str, int], steps: dict[str, int]
) -> tuple[int, int, int] | None:
    """下标表达式的 (最小下标, 最大下标, 步长) —— 任一项定不下来就返回 None。

    只处理「若干项相加」：`k * var` / `var` / `常量`。**结果取凸包**：
    若各项步长不同，和集理论上可能有洞（`{0,64,128,192} + {2,4,…,64}`），
    这里按「范围内、步长 = 各项步长之 gcd」摊开，即凸包 ⊇ 真实和集。
    用于判定「这个偏移属于该数组」是够的，且不会把数组外的偏移算进来。
    """
    lo = hi = 0
    stride = 0
    for part in expr.split("+"):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\s*\*\s*([A-Za-z_]\w*)", part)
        if m:
            k, var = int(m.group(1)), m.group(2)
            vals = loop_values(var, bounds, starts, steps)
            if vals is None:
                return None
            lo += k * min(vals)
            hi += k * max(vals)
            g = k * (steps.get(var, 1) or 1)
            stride = g if stride == 0 else math.gcd(stride, g)
            continue
        if re.fullmatch(r"[A-Za-z_]\w*", part):
            vals = loop_values(part, bounds, starts, steps)
            if vals is None:
                return None
            lo += min(vals)
            hi += max(vals)
            g = steps.get(part, 1) or 1
            stride = g if stride == 0 else math.gcd(stride, g)
            continue
        if re.fullmatch(r"0x[0-9a-fA-F]+|\d+", part):
            c = _num(part)
            lo += c
            hi += c
            continue
        return None
    return lo, hi, max(1, stride)




def parse_decompile_slots(text: str) -> list[dict]:
    """Find a1+N buffer writes/calls in reader decompile."""
    segs: list[dict] = []
    seen: set[tuple[int, str]] = set()
    a1s = a1_elem_size(text)
    bounds = loop_bounds(text)
    starts = var_starts(text)
    steps = var_steps(text)
    # ★ 只扫**函数体**：签名行里的 `(_DWORD *a1, int a2)` 含子串 `*a1`，
    # 会让「裸 a1 ＝ 偏移 0」凭空多出一条假证据。
    brace = text.find("{")
    body = text[brace:] if brace >= 0 else text

    def add(off: int, kind: str, extra: dict | None = None) -> None:
        key = (off, kind)
        if key in seen:
            return
        seen.add(key)
        row = {"offset": off, "kind": kind}
        if extra:
            row.update(extra)
        segs.append(row)

    def add_loop(lit: str, var: str, scale: int = 1) -> None:
        add(_num(lit) * scale, "slot_loop", {"index": var, "width": bounds.get(var)})

    def add_range(lo: int, hi: int, stride: int, vars_: list[str]) -> None:
        """连续字节/数组循环覆盖 [lo, hi) 里所有 stride 的倍数（起点下标可以非 0）。"""
        span = (hi - lo) // stride if stride else 0
        if span <= 0 or span > 256:
            return
        kind = "text_slot" if stride == 1 else "array_loop"
        add(lo, kind, {"stride": stride, "end": hi, "vars": vars_})

    # ① `*(_T *)(a1 + N)`：加法先按 a1 的声明类型走 N 个元素，再转型
    for m in re.finditer(
        r"\(\s*([_A-Za-z][\w \t]*?)\s*\*+\s*\)\s*\(\s*a1\s*\+\s*(0x[0-9a-fA-F]+|\d+)\s*\)", body
    ):
        add(_num(m.group(2)) * a1s, "cast_ptr", {"cast": m.group(1).strip()})

    # ② `(_T *)a1 + N`：转型先发生 ⇒ 偏移 = N × sizeof(_T)
    for m in re.finditer(
        r"\(\s*([_A-Za-z][\w \t]*?)\s*\*+\s*\)\s*a1\s*\+\s*(0x[0-9a-fA-F]+|\d+)", body
    ):
        add(_num(m.group(2)) * _cast_size(m.group(1)), "cast_ptr_arith", {"cast": m.group(1).strip()})

    # ③ 裸 a1 ＝ 偏移 0（`*(_DWORD *)a1` / `*a1` / `sub_XXX(a1, …)`）
    for m in re.finditer(r"\(\s*[_A-Za-z]\w*(?:\s+\w+)?\s*\*+\s*\)\s*a1\b(?!\s*\+)", body):
        add(0, "base")
    for m in re.finditer(r"\*\s*a1\b(?!\s*[+\[])", body):
        add(0, "base_deref")

    # ④ `a1 + N`（无转型；被转型接管的那些交给 ②，否则同为 `+N` 会按两套步长各算一次）
    for m in re.finditer(r"\ba1\s*\+\s*(0x[0-9a-fA-F]+|\d+)", body):
        prefix = body[max(0, m.start() - 40) : m.start()]
        if re.search(r"\(\s*[_A-Za-z][\w \t]*?\s*\*+\s*\)\s*$", prefix):
            continue
        add(_num(m.group(1)) * a1s, "ref")

    # ⑤ 定长文本槽循环：变量名、书写次序、有没有转型都不固定（三种次序 + 带转型都实测见过）
    # ★ 收尾不能要求 `)`：伪代码里这类槽多作为 helper 实参出现（`sub_B061C0(a1 + v5 + 80, a2)`，
    # 数字后面是逗号）。旧写法只认「数字后紧跟右括号」，于是 `pilot.clan_name@80` /
    # `cupteam_name@120` 这两条**已被写方 oracle 实证**的槽反而被判成「无证据」。
    # ★ 带转型时（`((_BYTE *)a1 + v10 + 204)`）步长按**转型后**的类型算：
    # 此时 204 是字节偏移而不是 `_DWORD` 下标，再乘 a1 的步长会算成 816。
    for m in re.finditer(
        r"\(\s*(?:\(\s*([_A-Za-z][\w \t]*?)\s*\*+\s*\)\s*)?a1\s*\+\s*([A-Za-z_]\w*)\s*\+\s*(0x[0-9a-fA-F]+|\d+)\s*(?=[\),])",
        body,
    ):
        add_loop(m.group(3), m.group(2), _cast_size(m.group(1)) if m.group(1) else a1s)
    for m in re.finditer(
        r"\(\s*(?:\(\s*([_A-Za-z][\w \t]*?)\s*\*+\s*\)\s*)?a1\s*\+\s*(0x[0-9a-fA-F]+|\d+)\s*\+\s*([A-Za-z_]\w*)\s*(?=[\),])",
        body,
    ):
        add_loop(m.group(2), m.group(3), _cast_size(m.group(1)) if m.group(1) else a1s)
    for m in re.finditer(
        r"\(\s*([A-Za-z_]\w*)\s*\+\s*a1\s*\+\s*(0x[0-9a-fA-F]+|\d+)\s*(?=[\),])", body
    ):
        add_loop(m.group(2), m.group(1), a1s)

    # ⑥ 下标写法：一律走通用下标求值（步长按 a1 的声明类型，不再一律 ×4）
    # ★ 2026-09-24 补：实测 `xwar_ext_rule\sub_B08160` 是
    # `*(_DWORD *)&a1[2 * v2 + 2 + 2 * i]`（a1 是 `_WORD *`）——
    # 旧实现只认 `a1[NUM]` 和 `a1[V + NUM]`，这种「带系数的和式下标」整条漏掉。
    for m in re.finditer(r"\ba1\s*\[\s*([^\[\]]+?)\s*\]", body):
        rng = index_range(m.group(1), bounds, starts, steps)
        if rng is None:
            continue
        lo, hi, st = rng
        if lo == hi:
            add(lo * a1s, "index")
        else:
            add_range(lo * a1s, (hi + 1) * a1s, st * a1s, [m.group(1).strip()])

    # ⑥b 元素数组循环 `a1 + K * (V + W)`：**起点不必是 0**
    # 实测 `ms\sub_B06D80`：`v29 = 47; … *(_DWORD *)(a1 + 4 * (v29 + v30))`，
    # 即 adop_items_eq@188（= 4×47），v29 按 +4 递增到 <0x3B ⇒ 下标 47..58。
    for m in re.finditer(
        r"\ba1\s*\+\s*(0x[0-9a-fA-F]+|\d+)\s*\*\s*\(?\s*([A-Za-z_]\w*(?:\s*\+\s*[A-Za-z_]\w*)*)\s*\)?",
        body,
    ):
        stride = _num(m.group(1))
        if stride <= 1:
            continue
        names = re.findall(r"[A-Za-z_]\w*", m.group(2))
        ranges = [loop_values(n, bounds, starts, steps) for n in names]
        if not ranges or any(r is None for r in ranges):
            continue
        lo = sum(min(r) for r in ranges)
        hi = sum(max(r) for r in ranges) + 1
        add_range(lo * stride, hi * stride, stride, names)

    # ⑦ 已知 helper 调用（带槽宽，顺带记下「谁写的这段槽」）
    # 偏移同 ④ 一样按 a1 的声明步长换算（`_DWORD *a1` 的 `a1 + 32` 是字节 128，不是 32）
    for fn, size in HELPER_SLOT.items():
        for m in re.finditer(
            re.escape(fn) + r"\s*\(\s*(?:\(\s*[_A-Za-z]\w*\s*\*+\s*\)\s*)?\(\s*a1\s*\+\s*(\d+)",
            body,
        ):
            add(int(m.group(1)) * a1s, "call", {"fn": fn, "size": size})

    segs.sort(key=lambda s: s["offset"])
    return segs


def expand_slots(segs: list[dict]) -> list[int]:
    """把数组循环段摊成显式偏移（审计只认「客户端确实碰过这个字节」）。"""
    out: set[int] = set()
    for s in segs:
        out.add(s["offset"])
        stride, end = s.get("stride"), s.get("end")
        if stride and end:
            out.update(range(s["offset"], end, stride))
    return sorted(out)

    segs.sort(key=lambda s: s["offset"])
    return segs


def parse_function(func_name: str) -> dict:
    ea = idc.get_name_ea_simple(func_name)
    if ea == idc.BADADDR:
        return {"function": func_name, "error": "no func"}
    if decompile is None:
        return {"function": func_name, "error": "no hexrays"}
    cfunc = decompile(ea)
    if not cfunc:
        return {"function": func_name, "error": "decompile failed"}
    text = str(cfunc)
    segs = parse_decompile_slots(text)
    slots = expand_slots(segs)
    max_end = 0
    for s in segs:
        end = s.get("end") or (s["offset"] + (s.get("size") or s.get("width") or s.get("bound") or 1))
        max_end = max(max_end, end)
    return {
        "function": func_name,
        "reader": func_name,  # 兼容 audit_memory_chain 的字段名（它原先一直读到 None）
        "slots": slots,
        "segments": segs,
        "a1_elem_size": a1_elem_size(text),
        "max_touch": max_end,
    }


def run_batch(batch_id: str) -> None:
    out_path = rf"F:\9ymsgo\9you\db_design\schema\_meta\ida_memory_slots_batch{batch_id}.json"
    fn_map = BATCH_FN.get(batch_id, {})
    out = {ent: parse_function(fn) for ent, fn in fn_map.items()}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote", out_path, "batch", batch_id)
    for ent, fn in fn_map.items():
        d = out[ent]
        slots = d.get("slots", [])
        print(f"{ent:20} fn={fn:14} slots={len(slots):2} max={d.get('max_touch', '?')}")


def _in_ida() -> bool:
    """只有真在 IDA 里（py_exec_file）才跑批量抽取；被 import（自测/静态检查）时不跑。"""
    return hasattr(idc, "get_idb_path") and hasattr(idc, "get_name_ea_simple")


if _in_ida():
    if BATCH in ("all", "*"):
        for bid in sorted(BATCH_FN, key=int):
            run_batch(bid)
    elif BATCH in BATCH_FN:
        run_batch(BATCH)
    else:
        # py_exec_file 下 sys.argv 是 IDA 自己的参数 ⇒ 默认全量重跑（幂等：覆盖 8 个 batch 文件）
        for bid in sorted(BATCH_FN, key=int):
            run_batch(bid)

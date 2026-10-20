# -*- coding: utf-8 -*-
"""在 IDA 里跑：静态抽取每个 cfg reader 的「完整读列集」（含包装函数的透传）。

背景：Unicorn 仿真在 reader 早期调用运行时 map/vector 查询时会死循环被 count 截断
（EMU-CUT），此时仿真读集只是**下界**。本脚本用 hexrays 的常量传播 + 包装函数透传分析
给出完整读集，用于交叉验证 schema 的 declared/non_gap。

规则：
  1) 通用助手（列号 = 最后一个参数）：
       sub_BBB370(tbl,n) int / sub_BBB470(tbl,n) float / sub_BBB3F0(tbl,n) i64
       sub_BBB4F0(dst,tbl,n) str / sub_BBB920(dst,tbl,n) str / sub_456D90(...) str
  2) 包装函数：若 F 体内把「自己的最后一个参数」原样传给上面任一助手的列号位置，
     则 F 也算一个「列号在最后参数」的读取器（如 sub_5976F0(dst,tbl,col) -> sub_BBB920(dst,tbl,col)）。
  3) reader 调用点的**最后一个实参**若是立即数（或先赋常量再传的局部）⇒ 记为该列。

输出 datatables/_out_static_cols.json
"""
import json
import os
import re

import ida_hexrays

HERE = r"f:\9ymsgo\9you\datatables"

# 通用助手 -> 列号参数位置（0 基，均取"最后一个参数"）
GENERIC = {
    "sub_BBB370": 1,
    "sub_BBB470": 1,
    "sub_BBB3F0": 1,
    "sub_BBB4F0": 2,
    "sub_BBB920": 2,
    "sub_456D90": 2,
}
CAST = re.compile(r"\( *(?:unsigned +int|int|signed +int|unsigned +__int64|__int64|unsigned +__int8|char) *\)")
ASSIGN = re.compile(r"\b(v\d+) = (0x[0-9A-Fa-f]+|\d+);")
PARAM = re.compile(r"^(?:\w[\w:<>* ]*?\s+)?([\w\[\]]+)$")


def split_args(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out]


def find_calls(text, fname):
    """返回 [(call_start_pos, 参数串)]，按出现顺序；括号配平扫描。"""
    res, pos = [], 0
    key = fname + "("
    while True:
        i = text.find(key, pos)
        if i < 0:
            return res
        j, depth = i + len(key), 1
        while j < len(text) and depth:
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
            j += 1
        res.append((i, text[i + len(key): j - 1]))
        pos = j


def const_of(expr, assigns_pos, pos):
    """解析实参常量；局部变量按「调用点之前最近一次赋值」解析（v124 等会被复用）。"""
    e = CAST.sub("", expr).strip().rstrip("uUlL")
    if re.match(r"^(0x[0-9A-Fa-f]+|\d+)$", e):
        return int(e, 0)
    if re.match(r"^v\d+$", e):
        best = None
        for (ap, var, val) in assigns_pos:
            if var == e and ap < pos:
                best = val
        if best is not None:
            return int(best, 0)
    return None


def params_of(text):
    """从函数签名里取参数名列表（含 this）。"""
    head = text.split(")", 1)[0]
    if "(" not in head:
        return []
    inner = head.split("(", 1)[1]
    if not inner.strip():
        return []
    names = []
    for p in split_args(inner):
        m = re.search(r"([A-Za-z_]\w*)\s*(?:\[\d+\])?$", p)
        if m:
            names.append(m.group(1))
    return names


def decompile(ea):
    try:
        return str(ida_hexrays.decompile(ea))
    except Exception:
        return None


def ea_of(name):
    m = re.match(r"^sub_([0-9A-Fa-f]+)$", name)
    return int(m.group(1), 16) if m else None


def main():
    readers = json.load(open(os.path.join(HERE, "_out_reader_list.json"), encoding="utf-8"))
    funcs = json.load(open(os.path.join(HERE, "_out_ida_funcs.json"), encoding="utf-8"))["funcs"]

    # 候选包装函数集 = 所有 reader 的直接被调函数
    cand = set()
    for name, meta in funcs.items():
        cand |= set(meta.get("calls") or {})
    cand -= set(GENERIC)
    cand = {c for c in cand if re.match(r"^sub_[0-9A-Fa-f]+$", c)}
    print(f"候选包装函数 {len(cand)}")

    text_of = {}
    params_of_f = {}
    for c in sorted(cand | set(readers) | set(GENERIC)):
        ea = ea_of(c)
        if ea is None:
            print("skip(非法函数名):", c)
            continue
        t = decompile(ea)
        if t:
            text_of[c] = t
            params_of_f[c] = params_of(t)

    # 固定点：判定哪些函数"最后一个参数 = 列号"
    lastparam_wrap = set()
    for _ in range(4):
        added = set()
        for c in text_of:
            if c in lastparam_wrap:
                continue
            pl = params_of_f.get(c) or []
            if not pl:
                continue
            last = pl[-1]
            hit = False
            for fn, ai in GENERIC.items():
                for _pos, raw in find_calls(text_of[c], fn):
                    args = split_args(raw)
                    if ai < len(args) and args[ai].strip() == last:
                        hit = True
            if not hit:
                for w in lastparam_wrap:
                    for _pos, raw in find_calls(text_of[c], w):
                        args = split_args(raw)
                        if len(args) >= 2 and args[-1].strip() == last:
                            hit = True
            if hit:
                added.add(c)
        if not added:
            break
        lastparam_wrap |= added
    print(f"判定为「最后参数=列号」的函数 {len(lastparam_wrap)}：{sorted(lastparam_wrap)}")

    result = {}
    for name in sorted(readers):
        if not name.startswith("sub_"):
            continue
        t = text_of.get(name)
        if not t:
            result[name] = {"tables": readers[name]["tables"], "error": "decompile failed"}
            continue
        assigns = [(m.start(), m.group(1), m.group(2)) for m in ASSIGN.finditer(t)]
        cols, unres, ncall = set(), [], 0
        colfuncs = set(GENERIC) | lastparam_wrap
        for fn in colfuncs:
            ai = GENERIC.get(fn, -1)  # 包装函数一律取最后一个实参
            for pos, raw in find_calls(t, fn):
                args = split_args(raw)
                ncall += 1
                if not args:
                    continue
                idx = ai if ai >= 0 else len(args) - 1
                if idx >= len(args):
                    unres.append(f"{fn}:{raw[:32]}")
                    continue
                c = const_of(args[idx], assigns, pos)
                if c is None:
                    unres.append(f"{fn}:{args[idx][:20]}")
                else:
                    cols.add(c)
        result[name] = {
            "tables": readers[name]["tables"],
            "cols": sorted(cols),
            "unresolved": unres,
            "n_calls": ncall,
        }

    outp = os.path.join(HERE, "_out_static_cols.json")
    json.dump(result, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", outp, len(result))
    for name in sorted(result):
        r = result[name]
        if "cols" in r:
            print(f"{name:14s} {','.join(r['tables'])[:22]:22s} cols={len(r['cols']):3d} "
                  f"calls={r['n_calls']:3d} unres={len(r['unresolved'])}")
        else:
            print(f"{name:14s} ERROR {r.get('error')}")


main()

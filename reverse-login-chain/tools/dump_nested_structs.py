# -*- coding: utf-8 -*-
"""
批量提取客户端"嵌套结构打印器"（每字段一个 "xxx=" 字符串 + push 顺序 = 线序）。
原理：协议 dump 代码里每个字段形如
        movsx ecx, byte ptr [base+15h]      ; 读字段
        push  offset aDeckIndex             ; 字段名
        call  sub_41D990                    ; 字符串拼接
     → xref 到 "*=" 字符串的函数 = 结构打印器；xref 地址排序 = 字段顺序。
产出：
    formats/battle_nested_fields.json
    formats/battle-嵌套结构字段表.md
"""
import re, json
import idautils, ida_funcs, ida_name, idc

OUT_JSON = r"F:\9ymsgo\9you\reverse-login-chain\formats\battle_nested_fields.json"
OUT_MD = r"F:\9ymsgo\9you\reverse-login-chain\formats\battle-嵌套结构字段表.md"

NAME_RE = re.compile(r"^[a-z0-9_]{2,40}=$")
# 帮助函数（拼接/数值打印）
HELPERS = {0x41D990, 0xB03580, 0xB032A0, 0xB032A0, 0xB083A0, 0xB031A0}

size_cache = {}
def fsize(f):
    return idc.get_func_attr(f, idc.FUNCATTR_END) - f


def scan_read_back(ea, limit=28):
    """从 push 处往前找最近的"读字段"指令，返回 (offset, kind)。"""
    p = ea
    for _ in range(limit):
        p = idc.prev_head(p)
        if p == idc.BADADDR:
            return None
        d = idc.generate_disasm_line(p, 0) or ""
        m = idc.print_insn_mnem(p)
        if m not in ("mov", "movsx", "movzx"):
            continue
        if "[" not in d:
            continue
        # 形如  movsx ecx, word ptr [ebp+24h]   /  mov eax, [esi+8]
        mm = re.search(r"\[\s*[a-z0-9]+\s*(?:\+\s*([0-9A-Fa-f]+h?))?\s*\]", d)
        if not mm:
            continue
        off = mm.group(1)
        off = int(off[:-1], 16) if (off and off.endswith("h")) else (int(off, 16) if off and re.search(r"[a-f]", off) else (int(off) if off else 0))
        kind = "u8" if "byte" in d else ("u16" if "word" in d else "u32")
        if m == "movsx":
            kind = "s" + kind[1:]
        elif m == "movzx":
            kind = "u" + kind[1:]
        return (off, kind)
    return None


def in_loop(ea, span=40):
    """push 点是否位于一个回边循环内。"""
    cur = ea
    for _ in range(span):
        cur = idc.next_head(cur)
        if cur == idc.BADADDR:
            return False
        m = idc.print_insn_mnem(cur)
        if m.startswith("j"):
            tgt = idc.get_operand_value(cur, 0)
            if 0 < tgt <= ea:
                return True
    return False


def collect():
    name_ea = {}
    for s in idautils.Strings():
        t = str(s)
        if NAME_RE.match(t):
            name_ea[s.ea] = t

    from collections import defaultdict
    fn_fields = defaultdict(list)   # func_start -> [(xref_ea, name)]
    for ea, t in name_ea.items():
        for x in idautils.XrefsTo(ea):
            f = ida_funcs.get_func(x.frm)
            if not f:
                continue
            fn_fields[f.start_ea].append((x.frm, t))

    result = []
    for fva, lst in sorted(fn_fields.items()):
        if len(lst) < 2:
            continue
        lst.sort()
        fields = []
        for xea, nm in lst:
            r = scan_read_back(xea)
            fields.append({
                "name": nm,
                "off": (r[0] if r else None),
                "kind": (r[1] if r else "?"),
                "loop": in_loop(xea),
                "xref": hex(xea),
            })
        # 谁调用该打印器
        callers = []
        for c in idautils.XrefsTo(fva):
            fn = ida_funcs.get_func(c.frm)
            callers.append(ida_name.get_name(fn.start_ea) if fn else hex(c.frm))
        result.append({
            "func": hex(fva),
            "size": fsize(fva),
            "n_fields": len(fields),
            "callers": sorted(set(callers))[:6],
            "fields": fields,
        })
    return result


def main():
    res = collect()
    with open(OUT_JSON, "w", encoding="utf-8") as fp:
        json.dump(res, fp, ensure_ascii=False, indent=1)

    lines = ["# 战服（battle）嵌套结构字段表 —— 由打印器自动提取",
             "",
             "> 工具：`reverse-login-chain/tools/dump_nested_structs.py`（IDA，2026-09-15）",
             "> 原理：客户端 dump 代码里每字段 = 读字段 + `push \"xxx=\"` + 拼接 ⇒ xref 排序 = **线序**。",
             "> 机读版：`battle_nested_fields.json`。`off` 为**内存槽偏移**（线序可能更紧凑，见各结构备注）。",
             ""]
    for r in sorted(res, key=lambda x: -x["n_fields"]):
        lines.append("## `%s`（%d 字节，%d 字段）← 调用者: %s" % (
            r["func"], r["size"], r["n_fields"], ", ".join(r["callers"])))
        lines.append("")
        lines.append("| # | 槽偏移 | 宽度 | 字段名 | 数组 |")
        lines.append("|---|---|---|---|---|")
        for i, fl in enumerate(r["fields"], 1):
            off = ("0x%X" % fl["off"]) if fl["off"] is not None else "?"
            lines.append("| %d | %s | %s | `%s` | %s |" % (
                i, off, fl["kind"], fl["name"][:-1], "是" if fl["loop"] else ""))
        lines.append("")
    with open(OUT_MD, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))
    print("printers=%d  ->  %s" % (len(res), OUT_MD))
    for r in sorted(res, key=lambda x: -x["n_fields"])[:20]:
        print("%-10s n=%-3d size=%-6d %s" % (r["func"], r["n_fields"], r["size"],
                                             ",".join(f["name"][:-1] for f in r["fields"][:8])))


main()

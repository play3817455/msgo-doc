# -*- coding: utf-8 -*-
"""批量提取大厅 S->C 应答报文的"线体规格"（IDA 静态，按 case 区间切分）。

思路：
  1. 定位包含所有响应 case 的**分发函数**（= entry 所在函数）
  2. 整个函数扫一遍，找出全部 **case 起点**：`push <gate>; mov ecx,esi; call sub_B41120`
  3. 每个 entry 归属到"起点 <= entry 的最后一个 case"，其范围 = [起点, 下一个起点)
  4. 在范围内聚合：alloc / readers / magic / fields

读取器字节消费（`probe_lobby_readers.py` 实测）：
  B41470=4  B413B0=2  B41A10=8  B02DD0=4  B02DF0=2  B06230=1
  B06200=8  B434B0=8  B05E30=1  B43B00=95  B43BE0=12
  数组型：B41850=4×n  B416C0=24×n  B415A0=96×n  B06060=12×n
  变长串：B02BA0（NUL 结尾有界串）

输出：server/docs/lobby_wire_spec.json
运行：IDA MCP 的 py_exec_file
"""
import json
import os
import idc
import ida_ua
import ida_funcs

ROOT = r"F:\9ymsgo\9you"
SLOT_MAP = os.path.join(ROOT, "reverse-login-chain", "formats", "_lounge_apply_slot_map.json")
OUT = os.path.join(ROOT, "server", "docs", "lobby_wire_spec.json")

FIXED = {
    0xB41470: ("u32", 4), 0xB413B0: ("u16", 2), 0xB41A10: ("u64", 8),
    0xB02DD0: ("u32b", 4), 0xB02DF0: ("u16b", 2), 0xB06230: ("u8b", 1),
    0xB06200: ("bytes8", 8), 0xB434B0: ("u32x2", 8), 0xB05E30: ("u8", 1),
    0xB41850: ("u32arr", -4), 0xB416C0: ("blk24arr", -24),
    0xB415A0: ("blk96arr", -96), 0xB06060: ("blk12arr", -12),
    0xB43B00: ("blk95", 95), 0xB43BE0: ("blk12", 12), 0xB02BA0: ("cstr", 0),
}
GATE_FN = 0xB41120
SZ = {}
for _a, (_n, _s) in FIXED.items():
    SZ.setdefault(_n, _s)


def line(ea):
    return idc.generate_disasm_line(ea, 0) or ""


def scan_func(f):
    """线性扫一个函数，产出 cases / events。"""
    s, en = f.start_ea, f.end_ea
    cases = []
    events = []
    ptr78 = set()
    last_push = None
    prev = []            # 最近 2 条 (addr, mnem)
    cur = s
    guard = 0
    while cur < en and guard < 6000000:
        guard += 1
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            cur += 1
            continue
        t = line(cur)
        mnem = idc.print_insn_mnem(cur)

        if mnem == "mov" and "+78h" in t:
            try:
                ptr78.add(idc.print_operand(cur, 0))
            except Exception:
                pass
        elif mnem == "push":
            last_push = idc.get_operand_value(cur, 0)
            events.append((cur, "push", last_push))
        elif mnem == "call":
            op0 = idc.print_operand(cur, 0)
            tgt = idc.get_operand_value(cur, 0)
            if tgt == GATE_FN and len(prev) >= 2 and prev[-1][1] == "mov" and prev[-2][1] == "push":
                g = idc.get_operand_value(prev[-2][0], 0)
                if 0 <= g < 0x10000:
                    cases.append((prev[-2][0], g, cur))
            elif op0 in ptr78 and isinstance(last_push, int) and 0 < last_push < 0x800000:
                events.append((cur, "alloc", last_push))
            elif tgt in FIXED:
                events.append((cur, "read", FIXED[tgt][0]))
        elif mnem == "mov" and "var_4]" in t:
            try:
                v = idc.get_operand_value(cur, 1)
                if 0 < v < 0x100000:
                    events.append((cur, "magic", v))
            except Exception:
                pass

        prev.append((cur, mnem))
        if len(prev) > 3:
            prev.pop(0)
        cur += ln
    cases.sort()
    events.sort()
    return cases, events


def main():
    with open(SLOT_MAP, encoding="utf-8") as fh:
        slot = json.load(fh)
    ents = slot.get("entries", {})
    items = [e for e in (ents.values() if isinstance(ents, dict) else ents)
             if isinstance(e, dict) and e.get("entry")]

    f = ida_funcs.get_func(int(items[0]["entry"], 16))
    print("分发函数 0x%X..0x%X (%.0f KB)  条目 %d" % (
        f.start_ea, f.end_ea, (f.end_ea - f.start_ea) / 1024.0, len(items)))
    cases, events = scan_func(f)
    print("case 数 %d  事件数 %d" % (len(cases), len(events)))
    if not cases:
        print("!! 未找到 case 起点，检查 sub_B41120 调用形态")
        return

    out = {}
    for e in items:
        ea = int(e["entry"], 16)
        name = e.get("name") or ("0x%04X" % e["id"])
        idx = -1
        for i, c in enumerate(cases):
            if c[0] <= ea:
                idx = i
            else:
                break
        if idx < 0:
            idx = 0
        pa, gate, _ca = cases[idx]
        end = cases[idx + 1][0] if idx + 1 < len(cases) else f.end_ea

        alloc = None
        magic = None
        readers = []
        fields = []
        for (a, kind, val) in events:
            if a < pa or a >= end:
                continue
            if kind == "alloc":
                if alloc is None:
                    alloc = val
            elif kind == "read":
                readers.append("%s@%X" % (val, a))
            elif kind == "magic":
                if magic is None:
                    magic = val
        # 字段名
        cur = pa
        while cur < end:
            insn = ida_ua.insn_t()
            ln = ida_ua.decode_insn(insn, cur)
            if ln == 0:
                break
            if idc.print_insn_mnem(cur) == "push":
                tg = idc.get_operand_value(cur, 0)
                if tg:
                    s = idc.get_strlit_contents(tg, -1, 0)
                    if isinstance(s, bytes):
                        try:
                            s = s.decode("utf-8")
                        except Exception:
                            s = s.decode("latin-1", "replace")
                    if s and s.strip().endswith("=") and 2 < len(s) < 40:
                        fields.append(s.strip())
            cur += ln

        fixed_sum = 0
        has_var = False
        for r in readers:
            k = r.split("@")[0]
            sz = SZ.get(k)
            if sz is None:
                continue
            if sz > 0:
                fixed_sum += sz
            else:
                has_var = True
        out[name] = {
            "id": e.get("id"),
            "id_hex": "0x%04X" % e["id"] if e.get("id") is not None else "",
            "entry": e.get("entry"),
            "gate": gate, "alloc": alloc, "magic": magic,
            "fixed_sum": fixed_sum, "has_var_reader": has_var,
            "fields": fields, "readers": readers,
        }

    st = {
        "total": len(out),
        "with_alloc": sum(1 for v in out.values() if v["alloc"]),
        "alloc_eq_sum": sum(1 for v in out.values()
                            if v["alloc"] and not v["has_var_reader"] and v["alloc"] == v["fixed_sum"]),
        "with_fields": sum(1 for v in out.values() if v["fields"]),
        "cases": len(cases),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"stats": st, "entries": out}, fh, ensure_ascii=False, indent=1)
    print("== stats ==", json.dumps(st, ensure_ascii=False))
    print("-> %s" % OUT)

    print("\n===== 全表 =====")
    for nm, v in sorted(out.items(), key=lambda kv: kv[1].get("id") or 0):
        print("%-46s %-7s gate=%-4s alloc=%-7s sum=%-6s %s f=%-2s %s" % (
            nm, v["id_hex"], v["gate"], v["alloc"], v["fixed_sum"],
            "VAR" if v["has_var_reader"] else "   ",
            len(v["fields"]), ",".join(v["fields"][:16])))


main()

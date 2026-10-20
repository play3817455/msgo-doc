# -*- coding: utf-8 -*-
"""只打印 case 里的「**读取器调用**」与「**字段名/打印串**」两类行。

为什么：`dump_case.py` 打全文（一个 case 上千行），批量看 16 条直接爆输出 ✗
而**线体布局只由这两类行决定** ⇒ 过滤后每 case 只剩 20~40 行 ✓

读 `reverse-login-chain/tools/_case_addrs.txt`（每行 `0xADDR # 说明`）。
运行：IDA MCP 的 py_exec_file
"""
import os
import re
import idc
import ida_ua

ROOT = r"F:\9ymsgo\9you"
ADDRS = os.path.join(ROOT, "reverse-login-chain", "tools", "_case_addrs.txt")

# 读取器助手（消费线体字节的）：用地址前缀判断
READER_RE = re.compile(r"call\s+(sub_B02|sub_B05|sub_B06|sub_B414|sub_B413|sub_B41A|sub_B418|"
                       r"sub_B43|sub_B44|sub_B434|sub_B416|sub_B411|sub_B075|sub_B0A)")
# 字段名/打印串（`push offset aXxx`）—— 顺序 = 读取顺序 ✓
STR_RE = re.compile(r"push\s+offset\s+(\w+)")
STOP = ("loc_B890EE", "loc_B890FE")


def main():
    with open(ADDRS, encoding="utf-8") as fh:
        items = [l.split("#")[0].strip() for l in fh]
    items = [x for x in items if x]

    for spec in items:
        start = int(spec, 16)
        end = start + 0x1600
        print("\n===== case 0x%X =====" % start)
        read = 0
        named = 0
        cur = start
        while cur != idc.BADADDR and cur < end:
            t = idc.generate_disasm_line(cur, 0) or ""
            mnem = idc.print_insn_mnem(cur)
            if mnem in ("retn", "ret"):
                break
            if "loc_B890" in t:
                break
            if READER_RE.search(t) and "sub_B41120" not in t:
                print("  %06X  %s" % (cur, t.strip()))
                read += 1
            else:
                m = STR_RE.search(t)
                if m and m.group(1)[:1] == "a" and m.group(1)[1:2].isupper():
                    op = idc.get_operand_value(cur, 0)
                    s = idc.get_strlit_contents(op) if op else None
                    show = s.decode("utf-8", "replace") if s else m.group(1)
                    print("  %06X  ### %s" % (cur, show[:44]))
                    named += 1
            if read > 60:
                print("  ...(读取行截断)")
                break
            nxt = idc.next_head(cur, end)
            if nxt <= cur:
                break
            cur = nxt


if __name__ == "__main__":
    main()

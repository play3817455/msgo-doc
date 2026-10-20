# -*- coding: utf-8 -*-
"""精确区间反汇编 —— 用来"看某几条指令到底干了什么"（call/push/cmp 之外的**内联内存操作**）。

用法：`_case_addrs.txt` 每行写 `START-END  # 注释`（十六进制，可多行）。
     ↓ 需要 IDA 环境（本脚本由 `py_exec_file` 在 IDA 里跑）
"""
import io
import sys

import idc

# ★IDA 里 `sys.stdout` 已经是 StringIO（没有 `.buffer`）⇒ 不能再包一层 ✗（本轮踩过）
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except AttributeError:
    pass

SPEC = r"F:\9ymsgo\9you\reverse-login-chain\tools\_case_addrs.txt"


def main():
    items = []
    for line in open(SPEC, encoding="utf-8"):
        line = line.split("#")[0].strip()
        if not line or "-" not in line:
            continue
        a, b = line.split("-")
        items.append((int(a, 16), int(b, 16)))
    for start, end in items:
        print("\n===== %X .. %X =====" % (start, end))
        cur = start
        n = 0
        while cur != idc.BADADDR and cur < end and n < 400:
            n += 1
            t = idc.generate_disasm_line(cur, 0) or ""
            print("  %06X  %s" % (cur, t.strip()))
            nxt = idc.next_head(cur, end)
            if nxt <= cur:
                break
            cur = nxt


main()

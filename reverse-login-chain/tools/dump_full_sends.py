# -*- coding: utf-8 -*-
"""把若干 send_* 函数**完整**反编译打印（函数很短时用，避免正则漏掉日志串字段名）。

读 `reverse-login-chain/tools/_send_full.txt`（每行 `0xADDR # 说明`）。
运行：IDA MCP 的 py_exec_file
"""
import os
import ida_hexrays
import idc

ROOT = r"F:\9ymsgo\9you"
ADDRS = os.path.join(ROOT, "reverse-login-chain", "tools", "_send_full.txt")

with open(ADDRS, encoding="utf-8") as fh:
    items = [l.split("#")[0].strip() for l in fh]
items = [x for x in items if x]

for spec in items:
    ea = int(spec, 16)
    print("\n===== 0x%X %s =====" % (ea, idc.get_func_name(ea)))
    try:
        cf = ida_hexrays.decompile(ea)
    except Exception as e:
        print("  !! %s" % e)
        continue
    if cf is None:
        print("  !! 无结果")
        continue
    lines = [l.rstrip() for l in str(cf).splitlines()]
    # 只跳到"第一个字段写入"之后（前面全是守卫/缓冲申请，噪声大）
    start = 0
    for i, l in enumerate(lines):
        if "sub_B02B40" in l or "sub_41D990" in l or "sub_B03580(a" in l:
            start = max(0, i - 6)
            break
    for l in lines[start:start + 45]:
        print("   " + l[:150])

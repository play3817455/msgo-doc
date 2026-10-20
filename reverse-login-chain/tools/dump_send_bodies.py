# -*- coding: utf-8 -*-
"""批量反编译 send_* 函数，只打印"组包相关行"（报文 ID + 字段写入 + 串写入）。

为什么只打这几类行：伪代码几千行，但**线体布局只由这几行决定**：
  · `*(_WORD *)v = <imm>;`        ⇒ 报文 ID（imm 与 0xNNNN 对照）
  · `*(_DWORD *)(v + N) = aK;`    ⇒ 第 K 个 u32 字段
  · `sub_B02B40(...)`             ⇒ NUL 串字段（cap 见第三个实参）
  · `sub_B02D80/sub_B07590(...)`  ⇒ 定长字段/尾巴
  · `v28[0] = ...`               ⇒ 游标推进（体长上界的来源）

读 `reverse-login-chain/tools/_send_addrs.txt`（每行：`0xADDR # 说明`）。

运行：IDA MCP 的 py_exec_file
"""
import os
import re
import ida_hexrays
import idc

ROOT = r"F:\9ymsgo\9you"
ADDRS = os.path.join(ROOT, "reverse-login-chain", "tools", "_send_addrs.txt")

PAT = re.compile(
    r"\*\(_WORD \*\)\s*\w+\s*=|"          # 报文 ID
    r"\*\(_DWORD \*\)\(\s*\w+ \+ \d+\)\s*=|"
    r"\*\(_DWORD \*\)\s*\w+\s*=\s*a\d|"
    r"sub_B02B40|sub_B02D80|sub_B07590|sub_B07540|sub_B02BA0|sub_B02DD0|"
    r"\bv28\[0\]|v28\[1\]|"
    r"sub_B03580\(\s*a\d|aId|aProto"
)

with open(ADDRS, encoding="utf-8") as fh:
    items = [l.split("#")[0].strip() for l in fh]
items = [x for x in items if x]

for spec in items:
    ea = int(spec, 16)
    name = idc.get_func_name(ea)
    print("\n===== 0x%X %s =====" % (ea, name))
    try:
        cf = ida_hexrays.decompile(ea)
    except Exception as e:
        print("  !! 反编译失败: %s" % e)
        continue
    if cf is None:
        print("  !! 无结果")
        continue
    lines = str(cf).splitlines()
    hit = 0
    for l in lines:
        s = l.strip()
        if PAT.search(s):
            print("   " + s[:170])
            hit += 1
        if hit > 40:
            print("   ...(截断)")
            break
    if hit == 0:
        # 兜底：打前 25 行，便于人看结构
        print("   （无匹配行，打印前 25 行）")
        for l in lines[:25]:
            print("   " + l.strip()[:170])

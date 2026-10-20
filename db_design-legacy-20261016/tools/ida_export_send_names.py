#!/usr/bin/env python3
"""导出「客户端 → 服务端发方全集」→ `schema/_meta/ida_send_names.txt`（在 IDA 里跑）。

为什么需要它：`no_writer` 那一桶（35 个根）和 `tournament` 的裁决都压在**一句否定**上——
「这个实体没有客户端写方」。否定断言必须可复核：先把发方**全集**取出来，再证明
「已建模的 CS 命令集 == 发方全集」（双向差集皆空）。只要这条恒成立，
「发方全集里没有它」就等于「它没有写方」。详见 docs/05 §9.7。

取法：协议层每条 send 都有断言串 `)-> _proto_<域>::send_<名>( `，扫全段字节按正则抓名字去重即可，
不依赖符号表。**大小写都要抓**（`msma_AI_*` 里是大写，只抓小写会漏 5 条）。

用法（两种都行）：
  * IDA 里 `File > Script file...` 选本文件；
  * 或经 IDA MCP：`py_exec_file` / `py_eval`（把 `main()` 体贴过去）。

注意（单调性）：重导会随客户端版本变化，**先 diff 再覆盖**；删名字必须在
`homing/_overrides.json.reviewed.batch_15_*` 或新批次里写明理由。
覆盖后必须跑 `python db_design/tools/_survey_homing.py`（守卫 14 会重比两侧）。
"""

from __future__ import annotations

import os
import re

PAT = re.compile(rb"send_([A-Za-z0-9_]+)\(")

HEADER = """# 客户端 → 服务端发方全集（IDA 导出，用于「0 个 CS 写方」这类否定断言的取证）
#
# 来源：客户端二进制 IDB（IDA Pro）。
# 方法：扫全段字节，匹配断言串 `send_<名>(`（大小写都要抓——`msma_AI_*` 里有大写），
#       取 `<名>` 去重（同名跨域合并，如 proto_version_check / authenticate 各注册 3 个域）。
# 导出脚本：db_design/tools/ida_export_send_names.py
# 对照：schema/commands 的 CS-*.json 解析出的唯一名必须与本文件**一一对应**
#       （回归见 tools/_survey_homing.py 守卫 14）。
# 用途：证明某类实体「0 个 CS 写方」时的发方全集底账；
#       详见 homing/_overrides.json 的 reviewed.batch_15_tournament_writer_hunt 与 docs/05 §9.7。
# 单调性：重导前先比对，删名字必须说明理由（不许静默减少）。
"""

# 仓库内位置（脚本在 IDA 里跑，用绝对路径；按需改成本机路径）。
OUT = os.environ.get("IDA_SEND_NAMES_OUT", r"F:\9ymsgo\9you\db_design\schema\_meta\ida_send_names.txt")


def collect() -> dict[str, int]:
    """名字 → 首次出现的地址（断言串位置，可当出处引用）。"""
    import ida_bytes
    import ida_segment
    import idautils

    names: dict[str, int] = {}
    for seg in idautils.Segments():
        s = ida_segment.getseg(seg)
        if not s:
            continue
        data = ida_bytes.get_bytes(s.start_ea, s.end_ea - s.start_ea) or b""
        for m in PAT.finditer(data):
            names.setdefault(m.group(1).decode(), s.start_ea + m.start())
    return names


def main() -> None:
    names = collect()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("\n".join(sorted(names)))
        f.write("\n")
    print(f"发方唯一名 {len(names)} 个 → {OUT}")
    print("大写名：", sorted(n for n in names if any(c.isupper() for c in n)))
    print("下一步：python db_design/tools/_survey_homing.py（守卫 14 会重比两侧）")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""按名字 / id 查「线体规格」与「上行发送函数」（★常用工具，保留 ✓）。

用法：
    python reverse-login-chain/tools/spec.py <报文名> [报文名...]
    python reverse-login-chain/tools/spec.py 0xB985            # 也可以直接给 id

输出（每个应答各一段）：
    entry / gate / alloc / fixed_sum / magic / has_var_reader
    fields  —— case 里的**打印串**（= 字段名，顺序与读取序一一对应 ✓）
    readers —— 逐次读取的助手与地址（`u32@B52541` = 原始读 / `u32b@` = 受检查读 ✓）
以及每条上行的 `func_addr`（喂给 `dump_send_bodies.py` 取体 ✓）。

★配合使用：`fields` 给你字段名，`readers` 给你项序 ——
  两者对齐后即可按 P110 铁律（**体长 = Σ受检查读取器**）写出编码器 ✓
"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"F:\9ymsgo\9you"
d = json.load(open(ROOT + r"\server\docs\lobby_wire_spec.json", encoding="utf-8"))["entries"]
s = json.load(open(ROOT + r"\reverse-login-chain\formats\_lounge_send_idmap.json",
                   encoding="utf-8"))

args = sys.argv[1:]
by_id = {}
for n, v in d.items():
    by_id[v["id"]] = (n, v)

for a in args:
    if a.startswith("--id"):
        continue
    if a.lower().startswith("0x"):
        nv = by_id.get(int(a, 16))
        if not nv:
            print("!! 无此 id %s" % a)
            continue
        name, v = nv
    else:
        v = d.get(a)
        if not v:
            print("!! 无此报文 %s" % a)
            continue
        name = a
    print("\n=== %-44s %s ===" % (name, v["id_hex"]))
    print("  entry=%s gate=%s alloc=%s fixed_sum=%s magic=%s var=%s"
          % (v["entry"], v["gate"], v["alloc"], v["fixed_sum"], v["magic"],
             v["has_var_reader"]))
    print("  fields =", v["fields"])
    print("  readers=", v["readers"])

for a in args:
    if a.startswith("--id"):
        continue
    u = s.get(a)
    if u:
        print("\n[send] %-44s %s func=%s" % (a, u["id_hex"], u["func_addr"]))
    else:
        print("\n[send] %-44s NONE" % a)

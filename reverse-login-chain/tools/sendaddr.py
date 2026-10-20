# -*- coding: utf-8 -*-
"""把一批**上行报文名**解析成"发送函数地址"表，写进 `_send_addrs.txt`。

用法：
    python reverse-login-chain/tools/sendaddr.py clan_create clan_kick_member ...
然后跑 IDA 的 `dump_send_bodies.py` 即可取体 ✓

★保留为常用工具（配合 `spec.py` → `dump_send_bodies.py` 三件套 ✓）。
"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = r"F:\9ymsgo\9you"
m = json.load(open(ROOT + r"\reverse-login-chain\formats\_lounge_send_idmap.json",
                   encoding="utf-8"))

lines = []
miss = []
for n in sys.argv[1:]:
    v = m.get(n)
    if not v or not v.get("func_addr"):
        miss.append(n)
        continue
    lines.append("%s  # %s %s" % (v["func_addr"].upper(), v["id_hex"], n))

open(ROOT + r"\reverse-login-chain\tools\_send_addrs.txt", "w", encoding="utf-8").write(
    "\n".join(lines) + "\n")
print("写了 %d 条；缺 %d 条：%s" % (len(lines), len(miss), ",".join(miss)))

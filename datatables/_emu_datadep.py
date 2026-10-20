# -*- coding: utf-8 -*-
"""对比「字符串列给真标记」vs「字符串列给空串」两次仿真的读列集合
-> 判断 reader 的取列数是否依赖数据（!= 空列为止）-> datatables/_out_emu_datadep.txt

读集变小 = 依赖数据（假环境会高估列数，真值取决于官方 CSV 里非空列有多少）
读集不变 = 结构性固定（列数是硬编码的，缺列就是真缺）
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(HERE, "_out_emu_readers_filled.json"), encoding="utf-8"))
b = json.load(open(os.path.join(HERE, "_out_emu_readers_empty.json"), encoding="utf-8"))

dep, same = [], []
for k in sorted(a):
    sa = {n for n in a[k]["observed"] if n is not None}
    sb = {n for n in b[k]["observed"] if n is not None}
    if not sa:
        continue
    if sa != sb:
        dep.append((k, a[k]["tables"], len(sa), len(sb), sorted(sa - sb)[:20], sorted(sb - sa)[:10]))
    else:
        same.append((k, a[k]["tables"], len(sa)))

out = []
out.append(f"读集随数据变化（字符串列空串后变小/变化）: {len(dep)} 个 reader")
for k, t, la, lb, lost, gain in dep:
    out.append(f"  {k:12s} {','.join(t)[:30]:30s} 标记串={la:3d} 空串={lb:3d} 少读={lost[:12]}{'...' if len(lost) > 12 else ''} 多读={gain}")
out.append("")
out.append(f"读集不随数据变化（结构性固定）: {len(same)} 个 reader")
out.append("  " + "  ".join(f"{k}({','.join(t)[:16]}:{n})" for k, t, n in same))
text = "\n".join(out)
print(text)
open(os.path.join(HERE, "_out_emu_datadep.txt"), "w", encoding="utf-8").write(text + "\n")

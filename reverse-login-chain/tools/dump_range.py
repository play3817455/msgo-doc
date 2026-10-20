# -*- coding: utf-8 -*-
"""打印 [start,end) 的反汇编，并把 `push offset aXxx` / `mov edx, offset aXxx`
解析成**字符串字面量**（找打印器字段名用 ✓）。

读 `reverse-login-chain/tools/_range.txt`（每行 `0xSTART 0xEND  # 说明`）。
用完即删。
"""
import os
import re

import idc

ROOT = r"F:\9ymsgo\9you"
RANGE = os.path.join(ROOT, "reverse-login-chain", "tools", "_range.txt")

STRPAT = re.compile(r"offset\s+(a\w+|asc_\w+|unk_\w+)")


def main():
    with open(RANGE, encoding="utf-8") as fh:
        lines = [l.split("#")[0].strip() for l in fh]
    for spec in lines:
        if not spec:
            continue
        a, b = spec.split()
        start, end = int(a, 16), int(b, 16)
        print("\n===== %06X .. %06X =====" % (start, end))
        cur = start
        n = 0
        while cur < end and cur != idc.BADADDR and n < 400:
            n += 1
            t = idc.generate_disasm_line(cur, 0) or ""
            show = t.strip()
            m = STRPAT.search(t)
            if m:
                ea = idc.get_name_ea_simple(m.group(1))
                s = idc.get_strlit_contents(ea) if ea != idc.BADADDR else None
                if s:
                    show += '        ### "%s"' % s.decode("utf-8", "replace")[:60]
            print("  %06X  %s" % (cur, show))
            nxt = idc.next_head(cur, end)
            if nxt <= cur:
                break
            cur = nxt


if __name__ == "__main__":
    main()

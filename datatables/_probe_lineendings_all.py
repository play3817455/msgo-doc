# -*- coding: utf-8 -*-
"""全量扫描 server/datafiles 下种子 CSV 的行尾符（找 LF-only / 混排 / BOM）。只读。"""
import os

ROOT = r"f:\9ymsgo\9you"
BASE = os.path.join(ROOT, "server", "datafiles")

bad, ok = [], 0
for dirpath, _dirs, files in os.walk(BASE):
    for fn in files:
        if not fn.lower().endswith(".csv"):
            continue
        p = os.path.join(dirpath, fn)
        try:
            b = open(p, "rb").read()
        except OSError:
            continue
        crlf = b.count(b"\r\n")
        lf = b.count(b"\n") - crlf
        bom = b.startswith(b"\xef\xbb\xbf")
        rel = os.path.relpath(p, ROOT)
        if lf or bom or (crlf == 0 and len(b) > 0):
            bad.append((rel, crlf, lf, bom))
        else:
            ok += 1

print("合规 CSV: %d ; 异常 %d" % (ok, len(bad)))
for rel, crlf, lf, bom in bad:
    print("  %-70s CRLF=%-6d 裸LF=%-5d BOM=%s" % (rel, crlf, lf, bom))

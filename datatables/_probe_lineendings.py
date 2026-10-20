# -*- coding: utf-8 -*-
"""检查 5 张 n1 表种子的行尾符/BOM/编码（填写规则要求 UTF-8 无 BOM + CRLF）。只读。"""
import io
import os

ROOT = r"f:\9ymsgo\9you"
FILES = [
    "server/datafiles/lounge/msma/msma_settings.csv",
    "server/datafiles/lounge/msma/msma_model.csv",
    "server/datafiles/lounge/msma/msma_rental.csv",
    "server/datafiles/lounge/msma/msma_module.csv",
    "server/datafiles/lounge/msma/msma_breakup.csv",
    "server/datafiles/lounge/item/weapon_settings.csv",
    "server/datafiles/lounge/item/weapon_battle_detail.csv",
]
for rel in FILES:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print("%-58s 缺文件" % rel)
        continue
    b = open(p, "rb").read()
    crlf = b.count(b"\r\n")
    lf_only = b.count(b"\n") - crlf
    bom = b.startswith(b"\xef\xbb\xbf")
    print("%-58s CRLF=%-6d 裸LF=%-6d BOM=%s 末字节=%r"
          % (os.path.basename(rel), crlf, lf_only, bom, b[-2:]))

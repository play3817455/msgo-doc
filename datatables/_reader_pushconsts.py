# -*- coding: utf-8 -*-
"""静态取常量：reader 里每个 CSV 助手调用点前压栈的**立即数**（列号）
用法: python _reader_pushconsts.py 0x58C440 [0x570750 ...]
-> datatables/_out_pushconsts.txt
"""
import io
import os
import sys

import capstone
import pefile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
pe = pefile.PE(os.path.join(ROOT, "unpacked", "GundamOnline_CHINA_v15.exe"), fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
md.detail = True
HELPER = {0xBBB370: "int", 0xBBB470: "float", 0xBBB4F0: "str-cdecl", 0x456D90: "str-this"}


def dis(va, n=0x600):
    return list(md.disasm(pe.get_data(va - base, n), va))


out = []
for arg in sys.argv[1:]:
    va = int(arg, 16)
    ins = dis(va)
    out.append(f"==== sub_{va:X} ====")
    for i, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str.startswith("0x"):
            tgt = int(x.op_str, 16)
            if tgt in HELPER:
                ctx = ins[max(0, i - 6):i]
                pushes = [f"{c.mnemonic} {c.op_str}" for c in ctx
                          if c.mnemonic in ("push", "mov", "lea") and ("push" in c.mnemonic)]
                out.append(f"  {x.address:#010x} call {tgt:#x} ({HELPER[tgt]})")
                for c in ctx:
                    out.append(f"        ^ {c.address:#010x} {c.mnemonic} {c.op_str}")
    out.append("")
text = "\n".join(out)
print(text)
open(os.path.join(HERE, "_out_pushconsts.txt"), "w", encoding="utf-8").write(text + "\n")

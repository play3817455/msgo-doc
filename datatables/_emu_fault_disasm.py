# -*- coding: utf-8 -*-
"""看仿真崩在哪条指令 -> datatables/_out_emu_faults.txt"""
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
out = []


def rd(va, n=64):
    return pe.get_data(va - base, n)


for eip in [int(x, 16) for x in sys.argv[1:]]:
    out.append(f"==== eip={eip:#x} ====")
    start = eip - 0x20
    for ins in md.disasm(rd(start, 0x40), start):
        mark = " <<<<<" if ins.address == eip else ""
        out.append(f"  {ins.address:#010x}  {ins.bytes.hex():<20s} {ins.mnemonic} {ins.op_str}{mark}")
text = "\n".join(out)
print(text)
open(os.path.join(HERE, "_out_emu_faults.txt"), "w", encoding="utf-8").write(text + "\n")

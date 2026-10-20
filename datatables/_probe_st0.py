# -*- coding: utf-8 -*-
"""测 Unicorn 写 ST0 的正确姿势：整数位模式 vs double 位模式"""
import io, struct, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from unicorn import *
from unicorn.x86_const import *

uc = Uc(UC_ARCH_X86, UC_MODE_32)
BASE = 0x100000
uc.mem_map(BASE, 0x10000)
CODE = BASE + 0x1000
MEM = BASE + 0x2000
uc.mem_write(MEM, b"\x00" * 0x100)

# fstp dword ptr [MEM] ; ret
code = b"\xd9\x1d" + struct.pack("<I", MEM) + b"\xc3"
uc.mem_write(CODE, code)
uc.reg_write(UC_X86_REG_ESP, BASE + 0x8000)
uc.mem_write(BASE + 0x8000, struct.pack("<I", BASE + 0x9000))

target = 1048583.0
for label, raw in (
    ("double-bits", struct.unpack("<Q", struct.pack("<d", target))[0]),
    ("int-value", int(target)),
):
    uc.mem_write(MEM, b"\x00" * 8)
    try:
        uc.reg_write(UC_X86_REG_ST0, raw)
    except Exception as e:
        print(label, "write failed:", e)
        continue
    back = uc.reg_read(UC_X86_REG_ST0)
    uc.reg_write(UC_X86_REG_ESP, BASE + 0x8000)
    try:
        uc.emu_start(CODE, CODE + len(code))
    except Exception as e:
        try:
            eip = uc.reg_read(UC_X86_REG_EIP)
            print("   bytes@eip:", uc.mem_read(eip, 8).hex())
        except Exception as e2:
            print("   (eip unreadable)", e2)
        print(label, "emu failed:", e)
        continue
    got = struct.unpack("<f", uc.mem_read(MEM, 4))[0]
    print(f"{label}: wrote={raw:#x} readback={back:#x} fstp->{got}")

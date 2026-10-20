# -*- coding: utf-8 -*-
"""用 Unicorn 真跑 78 个 cfg reader，拿到「CSV 字段号 -> 内存偏移」的**真值**
-> datatables/_out_emu_readers.json / _out_emu_readers.txt

原理：reader 读 CSV 全靠两个助手（已逐条反汇编确认）
  sub_BBB370(tbl, n) -> int   (内部：sub_456D90 取第 n 个字段串 -> sub_CC6876 atoi)
  sub_BBB470(tbl, n) -> float (内部：sub_456D90 取第 n 个字段串 -> sub_CC74E9 atof)
  sub_BBB4F0(dst, tbl, n) -> 第 n 个字段原串（写入 MSVC 28 字节小字符串对象）
  sub_456D90(this, dst, n) -> 同上（thiscall）
所以把 n 变成「唯一标记」返回，再记录 reader 写内存的 (偏移, 标记)，
即可反推每个写点对应的字段号 —— 无需任何静态常量传播（能绕开循环展开/指针差技巧）。

依赖：unicorn / capstone / pefile（均已安装）
"""
import io
import json
import os
import struct
import sys

import pefile
from unicorn import *
from unicorn.x86_const import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PE_PATH = os.path.join(ROOT, "unpacked", "GundamOnline_CHINA_v15.exe")
FUNCS_JSON = os.path.join(HERE, "_out_ida_funcs.json")
HOOK_JSON = os.path.join(HERE, "_out_hook_names.json")
READER_JSON = os.path.join(HERE, "_out_reader_list.json")
_SUF = os.environ.get("EMU_OUT_SUFFIX", "")
OUT_JSON = os.path.join(HERE, f"_out_emu_readers{_SUF}.json")
OUT_TXT = os.path.join(HERE, f"_out_emu_readers{_SUF}.txt")

STACK_BASE = 0x30000000
STACK_SIZE = 0x100000
ESP0 = STACK_BASE + 0x80000
SCRATCH_BASE = 0x60000000
SCRATCH_SIZE = 0x1000000
FS_BASE = 0x70000000

OUT_REGION = SCRATCH_BASE + 0x0010000  # 每次 reader 用的干净输出区
OUT_REGION_SIZE = 0x10000
OUT_OFF = 0x2000  # out 指针落点（之前留 8KB 给负偏移写）
RET_MAGIC = SCRATCH_BASE + 0x0E00000
VTBL_OBJ = SCRATCH_BASE + 0x0D00000
DUMMY_TBL = SCRATCH_BASE + 0x0D01000
FAKE_VCALL = SCRATCH_BASE + 0x0F00000  # 未映射 -> 由 fetch-unmapped 假返回

IN_BASE = 0x0A000000   # int 助手返回的标记基址
CV_BASE = 0x0C000000   # 枚举转换器返回的标记基址
FL_BASE = 0x00100000   # float 助手返回的标记基址（<2^24 保证精确）

INT_HELPERS = {0xBBB370}
INT64_HELPERS = {0xBBB3F0}      # cdecl: [esp+4]=tbl [esp+8]=n，返回 edx:eax（caller 存成 _QWORD）
FLOAT_HELPERS = {0xBBB470}
STR_HELPERS_C = {0xBBB4F0}     # cdecl: [esp+4]=dst [esp+8]=tbl [esp+0xC]=n
STR_HELPERS_THIS = {0x456D90}  # thiscall: ecx=this [esp+4]=dst [esp+8]=n
BENIGN = {0xCC5E75, 0xCC529D, 0xCC6876, 0xCC74E9, 0x4029E0, 0x402AD0, 0xBBB250}

log = []


def emit(s=""):
    print(s)
    log.append(s)


def align(x, a=0x1000):
    return (x + a - 1) & ~(a - 1)


class Emu:
    def __init__(self, func_meta, converters):
        self.func_meta = func_meta
        self.converters = converters
        self.hooked = {}
        self.reset()

    def reset(self):
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.emu = pefile.PE(PE_PATH, fast_load=True)
        self.base = self.emu.OPTIONAL_HEADER.ImageBase
        size = self.emu.OPTIONAL_HEADER.SizeOfImage
        for s in self.emu.sections:
            size = max(size, s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData))
        self.img_size = align(size)
        uc = self.uc
        uc.mem_map(self.base, self.img_size, UC_PROT_ALL)
        uc.mem_write(self.base, self.emu.__data__[: self.emu.OPTIONAL_HEADER.SizeOfHeaders])
        for s in sorted(self.emu.sections, key=lambda s: s.VirtualAddress):
            d = s.get_data()
            if d:
                uc.mem_write(self.base + s.VirtualAddress, d)
        uc.mem_map(STACK_BASE, STACK_SIZE, UC_PROT_ALL)
        uc.mem_map(SCRATCH_BASE, SCRATCH_SIZE, UC_PROT_ALL)
        uc.mem_map(FS_BASE, 0x10000, UC_PROT_ALL)
        uc.mem_write(FS_BASE, b"\x00" * 0x10000)
        # Unicorn 2.x 不支持写 FS_BASE（x86）——读取 fs:0 会走 unmapped 钩子按需映射
        try:
            uc.reg_write(UC_X86_REG_FS_BASE, FS_BASE)
        except Exception:
            pass
        self.calls = []
        self.conv_calls = []
        self.writes = []
        self.seq = 0
        self.err = None
        self.bad_addr = None
        self.last_str_cid = None
        self.in_hook = 0
        self.out_ptr = OUT_REGION + OUT_OFF
        self.install_hooks()

    # ---------- helpers ----------
    def rd32(self, a):
        return struct.unpack("<I", self.uc.mem_read(a, 4))[0]

    def wr32(self, a, v):
        self.uc.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))

    def write_str28(self, dst, text):
        if os.environ.get("EMU_EMPTYSTR"):
            text = ""  # 实验：字符串列一律给空串，看 reader 的取列数会不会变（判断是否「读到空列为止」）
        b = text.encode("ascii", "replace")
        blob = b"\x00" * 4 + (b + b"\x00").ljust(16, b"\x00")
        blob += struct.pack("<I", len(b)) + struct.pack("<I", 7)
        self.in_hook += 1
        try:
            self.uc.mem_write(dst, blob)
        finally:
            self.in_hook -= 1

    def read_str28(self, dst):
        try:
            n = self.rd32(dst + 0x14)
            cap = self.rd32(dst + 0x18)
            p = dst + 4 if cap < 8 else self.rd32(dst + 4)
            if n > 64:
                return ""
            return self.uc.mem_read(p, n).decode("ascii", "replace")
        except Exception:
            return ""

    def next_code(self):
        self.seq += 1
        return self.seq

    def do_return(self, addr, pop_extra, eax=None, edx=None, st0=None):
        uc = self.uc
        esp = uc.reg_read(UC_X86_REG_ESP)
        ret = self.rd32(esp)
        uc.reg_write(UC_X86_REG_ESP, esp + 4 + pop_extra)
        uc.reg_write(UC_X86_REG_EIP, ret)
        if eax is not None:
            uc.reg_write(UC_X86_REG_EAX, eax & 0xFFFFFFFF)
        if edx is not None:
            uc.reg_write(UC_X86_REG_EDX, edx & 0xFFFFFFFF)
        if st0 is not None:
            try:
                uc.reg_write(UC_X86_REG_ST0, st0)
            except Exception:
                pass

    # ---------- hooks ----------
    def install_hooks(self):
        uc = self.uc
        meta = self.func_meta
        cv = set(self.converters)
        self.trace = []
        self.esp_hist = []
        if os.environ.get("EMU_TRACE"):
            def tcb(uc_, address, size, ud):
                if address >= self.base and address < self.base + self.img_size:
                    self.trace.append(address)
                    if len(self.trace) > 60:
                        del self.trace[:20]
                    if os.environ.get("EMU_TRACE_ESP"):
                        self.esp_hist.append((address, uc_.reg_read(UC_X86_REG_ESP)))
                        if len(self.esp_hist) > 4000:
                            del self.esp_hist[:2000]

            uc.hook_add(UC_HOOK_CODE, tcb)
        for addr in INT_HELPERS:
            self.hook_int(addr)
        for addr in INT64_HELPERS:
            self.hook_int64(addr)
        for addr in FLOAT_HELPERS:
            self.hook_float(addr)
        for addr in STR_HELPERS_C:
            self.hook_str_c(addr, meta)
        for addr in STR_HELPERS_THIS:
            self.hook_str_this(addr, meta)
        for name in cv:
            if not name.startswith("sub_"):
                continue
            a = int(name[4:], 16)
            if a in INT_HELPERS or a in INT64_HELPERS or a in FLOAT_HELPERS or a in STR_HELPERS_C or a in STR_HELPERS_THIS:
                continue
            self.hook_conv(a, meta)
        for a in BENIGN:
            if a in cv:
                continue
            self.hook_benign(a, meta)
        uc.hook_add(
            UC_HOOK_MEM_WRITE, self.on_write, None, SCRATCH_BASE, SCRATCH_BASE + SCRATCH_SIZE
        )
        uc.hook_add(UC_HOOK_MEM_FETCH_UNMAPPED, self.on_fetch_unmapped)
        uc.hook_add(UC_HOOK_MEM_WRITE_UNMAPPED, self.on_write_unmapped)
        uc.hook_add(UC_HOOK_MEM_READ_UNMAPPED, self.on_read_unmapped)

    def _pop_extra(self, meta, addr):
        return meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

    def hook_int(self, addr):
        meta = self.func_meta
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            esp = uc.reg_read(UC_X86_REG_ESP)
            n = self.rd32(esp + 8)
            cid = self.next_code()
            self.calls.append({"cid": cid, "kind": "int", "n": n, "ea": a, "seq": cid})
            self.do_return(a, pop, eax=IN_BASE + cid)

        uc = self.uc
        uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_int64(self, addr):
        meta = self.func_meta
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            esp = uc.reg_read(UC_X86_REG_ESP)
            n = self.rd32(esp + 8)
            cid = self.next_code()
            self.calls.append({"cid": cid, "kind": "int64", "n": n, "ea": a, "seq": cid})
            self.do_return(a, pop, eax=IN_BASE + cid, edx=0)

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_float(self, addr):
        pop = self.func_meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            esp = uc.reg_read(UC_X86_REG_ESP)
            n = self.rd32(esp + 8)
            cid = self.next_code()
            self.calls.append({"cid": cid, "kind": "float", "n": n, "ea": a})
            self.do_return(a, pop, st0=float(FL_BASE + cid))

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_str_c(self, addr, meta):
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            esp = uc.reg_read(UC_X86_REG_ESP)
            dst, tbl, n = self.rd32(esp + 4), self.rd32(esp + 8), self.rd32(esp + 0xC)
            cid = self.next_code()
            self.calls.append({"cid": cid, "kind": "str", "n": n, "ea": a})
            self.last_str_cid = cid
            if 0 < dst < 0x100000000:
                self.write_str28(dst, str(cid))
            self.do_return(a, pop, eax=dst)

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_str_this(self, addr, meta):
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            esp = uc.reg_read(UC_X86_REG_ESP)
            dst, n = self.rd32(esp + 4), self.rd32(esp + 8)
            cid = self.next_code()
            self.calls.append({"cid": cid, "kind": "str", "n": n, "ea": a})
            self.last_str_cid = cid
            if 0 < dst < 0x100000000:
                self.write_str28(dst, str(cid))
            self.do_return(a, pop, eax=dst)

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_conv(self, addr, meta):
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            ecx = uc.reg_read(UC_X86_REG_ECX)
            esp = uc.reg_read(UC_X86_REG_ESP)
            s = self.read_str28(ecx)
            if not s:
                s = self.read_str28(self.rd32(esp + 4))
            cid = self.next_code()
            self.conv_calls.append({"cid": cid, "str": s, "src": self.last_str_cid, "ea": a})
            self.do_return(a, pop, eax=CV_BASE + cid)

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def hook_benign(self, addr, meta):
        pop = meta.get(f"sub_{addr:X}", {}).get("retn_pop") or 0

        def cb(uc, a, size, ud):
            self.do_return(a, pop, eax=0)

        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def on_write(self, uc, access, address, size, value, ud):
        if self.in_hook:
            return True
        self.seq += 1
        self.writes.append({
            "seq": self.seq,
            "abs": address,
            "off": address - self.out_ptr,
            "size": size,
            "value": value,
        })
        return True

    def on_fetch_unmapped(self, uc, access, address, size, value, ud):
        # 库外代码（IAT / 假 vtable）-> 直接当「返回 0」处理
        esp = uc.reg_read(UC_X86_REG_ESP)
        ret = self.rd32(esp)
        uc.reg_write(UC_X86_REG_ESP, esp + 4)
        uc.reg_write(UC_X86_REG_EIP, ret)
        uc.reg_write(UC_X86_REG_EAX, 0)
        return True

    def _lazy_map(self, uc, address):
        page = address & ~0xFFF
        try:
            uc.mem_map(page, 0x1000, UC_PROT_ALL)
        except Exception:
            # 已映射 / 非法地址：能读就当已映射，读不了才失败
            try:
                uc.mem_read(page, 1)
            except Exception:
                self.bad_addr = address
                return False
        return True

    def on_write_unmapped(self, uc, access, address, size, value, ud):
        return self._lazy_map(uc, address)

    def on_read_unmapped(self, uc, access, address, size, value, ud):
        return self._lazy_map(uc, address)

    # ---------- run ----------
    def fill_dummy(self, mode):
        """mode 0: 全 0（默认）；mode 1: 每个 dword 指向 scratch 里的合法小对象
        mode 2: 每个 dword 指向一个自指「RB 树 nil 节点」——让 map/tree 查询立即命中"未找到"，
                避免假对象把 tree 遍历带进死循环（EMU-CUT(limit) 的根因）。"""
        uc = self.uc
        if mode == 0:
            uc.mem_write(DUMMY_TBL, b"\x00" * 0x2000)
            return
        if mode == 2:
            nil = SCRATCH_BASE + 0x900000
            node = bytearray(struct.pack("<I", nil) * 0x80)  # 512B，所有 dword 自指
            node[13] = 1      # MSVC _Isnil
            node[117] = 1     # 本作 RB 树判空字节（sub_4317D0: *((_BYTE*)v4+117)）
            uc.mem_write(nil, bytes(node))
            uc.mem_write(DUMMY_TBL, struct.pack("<I", nil) * 0x800)
            return
        blob = bytearray()
        for i in range(0x800):
            ptr = SCRATCH_BASE + 0x900000 + (i % 0x100) * 0x40
            blob += struct.pack("<I", ptr)
        uc.mem_write(DUMMY_TBL, bytes(blob))

    def run(self, name, addr, args, out_ptr, timeout=3_000_000, count=4_000_000):
        """args = 按 cdecl 顺序的实参列表（最后一个通常在栈顶前一位）。"""
        self.reader_start = addr
        self.out_ptr = out_ptr
        uc = self.uc
        uc.mem_write(OUT_REGION, b"\x00" * OUT_REGION_SIZE)
        esp = ESP0
        for v in reversed(args):
            esp -= 4
            self.wr32(esp, v)
        esp -= 4
        self.wr32(esp, RET_MAGIC)
        uc.reg_write(UC_X86_REG_ESP, esp)
        uc.reg_write(UC_X86_REG_EBP, 0)
        uc.reg_write(UC_X86_REG_EBX, 0)
        # 有些 reader 是 thiscall（this 在 ECX），给个假对象免得写到 0 附近
        uc.reg_write(UC_X86_REG_ECX, DUMMY_TBL)
        try:
            uc.emu_start(addr, RET_MAGIC, timeout=timeout, count=count)
            self.err = None
            # 停在 RET_MAGIC 有两种可能：函数正常 ret 走了；或中途栈错位/假返回导致"提前回来"。
            # 用返回时的 ESP 对齐来判别（正常 ret + retn pop 后 ESP 必然回到 ESP0）。
            self.exit_esp = uc.reg_read(UC_X86_REG_ESP)
            self.exit_eip = uc.reg_read(UC_X86_REG_EIP)
            pop = self._pop_extra(self.func_meta, addr)
            expect = ESP0 - 4 * len(args) + pop
            if self.exit_eip != RET_MAGIC:
                self.err = f"EMU-CUT(limit) eip={self.exit_eip:#x}"
            elif self.exit_esp != expect:
                self.err = f"TRUNCATED esp={self.exit_esp:#x} expect={expect:#x}"
            if os.environ.get("EMU_TRACE"):
                n_in = sum(1 for a in self.trace if addr <= a <= (addr + 0x4000))
                print(f"[STOP {name}] eip={self.exit_eip:#x} esp={self.exit_esp:#x} expect={expect:#x} "
                      f"in_reader={n_in} err={self.err}")
                print("  last:", " ".join(f"{a:#x}" for a in self.trace[-40:]))
                if os.environ.get("EMU_TRACE_ESP"):
                    for ea, sp in self.esp_hist[-24:]:
                        print(f"    {ea:#010x} esp={sp:#x}")
        except UcError as e:
            try:
                eip = uc.reg_read(UC_X86_REG_EIP)
            except Exception:
                eip = 0
            ba = f" bad={self.bad_addr:#x}" if self.bad_addr else ""
            self.err = f"{e} eip={eip:#x}{ba}"
            print(f"[TRACE {name}] eip={eip:#x}{ba}")
            print("  last:", " ".join(f"{a:#x}" for a in self.trace[-40:]))
            try:
                print("  bytes@eip:", uc.mem_read(eip, 16).hex())
                print("  regs:", {r: hex(uc.reg_read(r)) for r in (UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_EBP)})
            except Exception:
                pass


def build_call_map(calls, conv_calls, writes):
    """标记值 -> 字段号；写点 -> 字段号（标记优先，其次按执行顺序配对）"""
    cid2n = {c["cid"]: c["n"] for c in calls}
    cid2kind = {c["cid"]: c["kind"] for c in calls}
    conv2sid = {}
    for cc in conv_calls:
        s = cc["str"]
        if s.startswith("M") and s[1:].isdigit():
            conv2sid[cc["cid"]] = int(s[1:])
        elif cc.get("src"):
            conv2sid[cc["cid"]] = cc["src"]
    store = []
    for w in writes:
        val = w["value"]
        n = kind = via = None
        if IN_BASE <= val < IN_BASE + 200000:
            c = val - IN_BASE
            if c in cid2n:
                n, kind, via = cid2n[c], cid2kind[c], "marker"
        if n is None and CV_BASE <= val < CV_BASE + 200000:
            sid = conv2sid.get(val - CV_BASE)
            if sid is not None:
                n, kind, via = cid2n.get(sid), "enum", "conv-marker"
        if n is None:
            f = struct.unpack("<f", struct.pack("<I", val & 0xFFFFFFFF))[0]
            if FL_BASE <= f < FL_BASE + 200000 and abs(f - round(f)) < 1e-6:
                c = int(round(f)) - FL_BASE
                if c in cid2n:
                    n, kind, via = cid2n[c], "float", "marker"
        store.append({"seq": w["seq"], "off": w["off"], "size": w["size"], "value": val, "n": n, "kind": kind, "via": via})

    # 兜底：按执行顺序，把还没解出的调用配到它之后最近的未认领写点
    claimed = {s["seq"] for s in store if s["n"] is not None}
    free = sorted([s for s in store if s["n"] is None], key=lambda s: s["seq"])
    for c in sorted(calls, key=lambda c: c["cid"]):
        if any(s["n"] == c["n"] and s["via"] is not None for s in store):
            pass
        cand = [s for s in free if s["seq"] > c["cid"] and s["seq"] not in claimed]
        if not cand:
            continue
        t = cand[0]
        t["n"], t["kind"], t["via"] = c["n"], c["kind"], "pair"
        claimed.add(t["seq"])
    return store


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    funcs = json.load(open(FUNCS_JSON, encoding="utf-8"))["funcs"]
    hooks = json.load(open(HOOK_JSON, encoding="utf-8"))
    readers = json.load(open(READER_JSON, encoding="utf-8"))

    E = Emu(funcs, [n for n in hooks["names"] if n in hooks["converters"]])

    out_ptr = OUT_REGION + OUT_OFF
    results = {}
    targets = [(n, readers[n]) for n in sorted(readers) if n.startswith("sub_")]
    if only:
        targets = [t for t in targets if t[0] == only]

    emit(f"{'reader':14s} {'表':24s} {'助手读':>6s} {'写点':>5s} {'已解出':>6s} {'ABI':>5s} {'错误':>14s}")
    emit("-" * 100)

    def abi_layouts():
        """reader 的 (tbl, ?, dst) 实参排布各作不同——逐个试，取「解出的写点最多」的那个。"""
        return [
            ("dst3", (DUMMY_TBL, 0, out_ptr)),
            ("dst4", (DUMMY_TBL, 0, 0, out_ptr)),
            ("dst1", (out_ptr, DUMMY_TBL, 0)),
            ("dst2", (DUMMY_TBL, out_ptr, 0)),
        ]

    for name, info in targets:
        addr = int(name[4:], 16)
        best = None
        for lname, args in abi_layouts():
            mode_runs = []
            chosen = None
            for mode in (0, 1, 2):
                E.reset()
                E.fill_dummy(mode)
                E.run(name, addr, args, out_ptr)
                w = [x for x in E.writes]
                store = build_call_map(E.calls, E.conv_calls, w)
                resolved = [s for s in store if s["n"] is not None]
                observed = sorted({c["n"] for c in E.calls} | {s["n"] for s in resolved if s["n"] is not None})
                mode_runs.append({
                    "mode": mode, "err": E.err, "calls": E.calls, "conv_calls": E.conv_calls,
                    "writes": w, "store": store, "resolved": resolved, "observed": observed,
                })
                if not E.err:
                    chosen = mode_runs[-1]
                    break
            if chosen is None:
                # 三种假对象都跑不通：取「读到的列最多」的那次作为下界
                chosen = max(mode_runs, key=lambda r: len(r["observed"]))
            cand = dict(chosen, abi=lname, layouts=mode_runs)
            # 打分：无错 > 高置信写点(numbered) 多 > 观察到列多
            hi = [s for s in chosen["store"] if s.get("via") in ("marker", "conv-marker")]
            score = (1 if chosen["err"] is None else 0, len(hi), len(chosen["resolved"]), len(chosen["observed"]))
            good = chosen["err"] is None and hi
            if best is None or score > best[0]:
                best = (score, cand)
            # 已经稳了（解出量达到申报列的 6 成以上）就不必再试别的 ABI
            if good and len(hi) >= max(4, 0.6 * len(info["declared"])):
                break
        score, chosen = best
        mode_runs = chosen["layouts"]
        dbg = chosen["mode"]
        w = chosen["writes"]
        store = chosen["store"]
        resolved = chosen["resolved"]
        observed = chosen["observed"]
        results[name] = {
            "tables": info["tables"],
            "declared": info["declared"],
            "non_gap": info["non_gap"],
            "err": chosen["err"],
            "retry": dbg,
            "abi": chosen["abi"],
            "modes": [{"mode": r["mode"], "err": r["err"], "observed": r["observed"]} for r in mode_runs],
            "calls": chosen["calls"],
            "n_seq": [c["n"] for c in chosen["calls"]],
            "observed": observed,
            "stores": store,
            "resolved": [{"off": s["off"], "n": s["n"], "kind": s["kind"], "via": s.get("via")} for s in resolved],
        }
        emit(
            f"{name:14s} {','.join(info['tables'])[:24]:24s} {len(chosen['calls']):6d} {len(w):5d} "
            f"{len(resolved):6d} {chosen['abi']:>5s}{str(chosen['err'])[:14]:>14s}"
        )

    json.dump(results, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print(f"\nwrote {OUT_JSON}  ({len(results)} readers)")


main()

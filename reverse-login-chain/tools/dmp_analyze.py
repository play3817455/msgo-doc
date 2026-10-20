# -*- coding: utf-8 -*-
"""
dmp_analyze.py —— 客户端崩溃取证：**解析 WER minidump**（异常码 / 异常地址 / 模块归属 / EBP 链 / 特征串）。

配套文档：`.codebuddy/memory/topics/20-客户端崩溃取证SOP.md`（★先读它 ✓）

为什么需要它：
    客户端崩了以后，`%LOCALAPPDATA%\\CrashDumps\\GundamOnline_CHINA.exe.<pid>.dmp` 会留下
    **完整的异常记录**（异常码 + 异常地址 + 全部寄存器 + 部分内存 ✓）。
    WER 事件日志只给一句 `module unknown / offset 0` ✗ **没有信息量** ✓，真东西在 dmp 里 ✓。

用法：
    python dmp_analyze.py <file.dmp> [more.dmp ...]      # 基本（异常 + 模块 + EBP 链）
    python dmp_analyze.py --str <file.dmp> [关键字...]    # 扫内存块里的可读字符串
    python dmp_analyze.py --all <dir 或 glob>            # 批量比多个转储（找"是不是同一个崩"）

判读要点（详细见 SOP）：
    ★`0xC0000005` + 崩溃地址形如 `<随机基址>+0x8D71`（低 16 位恒为 `8D71`）
      ⇒ **手工映射的反外挂用户态模块**（HookLibraryx86 / XGG）✓ —— 长期现象，**与游戏数据无关** ✗
    ★`0xC0000005` + 固定 `0x004037CC` ⇒ 反外挂**蓄意 NULL 写自毁** ✓
    ★`0xC0000409` ⇒ CPS 90s 看门狗 fail-fast ✓
    ★`0x00000000` + `offset 0` + `module unknown` ⇒ 客户端**自己走致命退出**路径 ✓（非访问违例 ✗）
    ★`0xC0000005` + **具体小地址**（如 `0x94`）⇒ 多半是**我们下发的数据结构不合法** ✓（该查服务端 ✓）

已实证案例：2026-09-17 22:28 那次 —— 8 份 dmp 全是
    `mov eax,[ecx+0x90]` + `ecx=4` ⇒ 读 `0x94`，地址全部 `??..8D71` ⇒ **反外挂模块** ✓
"""
import glob
import io
import os
import re
import struct
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

STREAM = {3: "ThreadList", 4: "ModuleList", 5: "MemoryList", 6: "Exception",
          7: "SystemInfo", 9: "Memory64List", 15: "MiscInfo", 16: "MemoryInfoList"}

CODES = {
    0xC0000005: "ACCESS_VIOLATION(非法内存访问)",
    0xC0000094: "INTEGER_DIVIDE_BY_ZERO(除零)",
    0xC00000FD: "STACK_OVERFLOW(栈溢出)",
    0xC000001D: "ILLEGAL_INSTRUCTION(非法指令)",
    0xC0000096: "PRIVILEGED_INSTRUCTION",
    0xC0000409: "STACK_BUFFER_OVERRUN / **fail-fast(反外挂看门狗常见 ✓)**",
    0x80000003: "BREAKPOINT",
    0xE06D7363: "C++ EXCEPTION(throw)",
}


def load(path):
    """读出 dmp 的目录 + 内存映射（内存块 → 文件偏移）。"""
    b = open(path, "rb").read()
    if b[:4] not in (b"MDMP", b"PMDM"):
        raise ValueError("不是 minidump（签名 %r）" % b[:4])
    _sig, _ver, nstr, dir_rva = struct.unpack_from("<IIII", b, 0)
    dirs = [struct.unpack_from("<III", b, dir_rva + i * 12) for i in range(nstr)]

    def stream(t):
        for st, size, rva in dirs:
            if st == t:
                return rva, size
        return None, None

    ranges = []
    r9, _ = stream(9)                     # Memory64List
    if r9:
        n, base = struct.unpack_from("<QQ", b, r9)
        off = base
        for i in range(n):
            s, sz = struct.unpack_from("<QQ", b, r9 + 16 + i * 16)
            ranges.append((s, sz, off))
            off += sz
    r5, _ = stream(5)                     # MemoryList（每条 16B ✓ ★别写成 12B ✗）
    if r5:
        n = struct.unpack_from("<I", b, r5)[0]
        for i in range(n):
            s, sz, r = struct.unpack_from("<QII", b, r5 + 4 + i * 16)
            ranges.append((s, sz, r))
    r3, _ = stream(3)                     # 线程栈（每条 48B，栈描述符在 +24 ✓）
    if r3:
        n = struct.unpack_from("<I", b, r3)[0]
        for i in range(n):
            s, sz, r = struct.unpack_from("<QII", b, r3 + 4 + i * 48 + 24)
            if sz:
                ranges.append((s, sz, r))
    return b, dirs, stream, ranges


def reader(b, ranges):
    def rd(addr, ln):
        for s, sz, r in ranges:
            if s <= addr < s + sz:
                d = r + (addr - s)
                return b[d:min(d + ln, d + (s + sz - addr))]
        return b""
    return rd


def modules(b, stream):
    rva, _ = stream(4)
    out = []
    if not rva:
        return out
    n = struct.unpack_from("<I", b, rva)[0]
    for i in range(n):                    # MINIDUMP_MODULE = 108B，名字 RVA 在 +20 ✓
        base = rva + 4 + i * 108
        b64, sz, _c, _t, name_rva = struct.unpack_from("<QIIII", b, base)
        ln = struct.unpack_from("<I", b, name_rva)[0]
        nm = b[name_rva + 4:name_rva + 4 + ln].decode("utf-16", "replace").split("\\")[-1]
        out.append((b64, sz, nm))
    return sorted(out)


def regs_of(b, stream, ranges):
    rva, _ = stream(6)
    if not rva:
        return {}, {}
    tid, = struct.unpack_from("<I", b, rva)
    code, flags = struct.unpack_from("<II", b, rva + 8)
    _rec, addr = struct.unpack_from("<QQ", b, rva + 16)
    nparam = struct.unpack_from("<I", b, rva + 32)[0]
    params = struct.unpack_from("<15Q", b, rva + 40)
    ctx_size, ctx_rva = struct.unpack_from("<II", b, rva + 160)
    regs = {}
    if ctx_rva:
        for name, off in [("edi", 156), ("esi", 160), ("ebx", 164), ("edx", 168), ("ecx", 172),
                          ("eax", 176), ("ebp", 180), ("eip", 184), ("esp", 196)]:
            regs[name] = struct.unpack_from("<I", b, ctx_rva + off)[0]
    info = {"tid": tid, "code": code, "flags": flags, "addr": addr,
            "nparam": nparam, "params": params}
    return info, regs


def basic(path):
    b, dirs, stream, ranges = load(path)
    print("=== %s ===" % os.path.basename(path))
    print("  流: " + ", ".join("%s(%dB)" % (STREAM.get(st, "?%d" % st), size) for st, size, _ in dirs))
    mods = modules(b, stream)
    info, regs = regs_of(b, stream, ranges)
    rd = reader(b, ranges)
    code, addr = info["code"], info["addr"]
    print("  code = 0x%08X  (%s)" % (code, CODES.get(code, "?")))
    showed = " ".join("%#x" % p for p in info["params"][:max(0, min(2, info["nparam"]))])
    print("  addr = 0x%08X   参数=[%s]%s" % (
        addr, showed, "   ★被访问地址=0x%X" % info["params"][1] if info["nparam"] >= 2 else ""))
    hit = next(((m[0], m[1], m[2]) for m in mods if m[0] <= addr < m[0] + m[1]), None)
    if hit:
        print("  ★模块归属：**%s** + 0x%X（base=0x%X）" % (hit[2], addr - hit[0], hit[0]))
    else:
        print("  ★模块归属：**不属于任何模块**（动态分配 / 已卸载 ✗）")
        near = sorted(mods, key=lambda m: abs(m[0] - addr))[:3]
        print("     最近模块：" + ", ".join("%s@0x%X" % (m[2], m[0]) for m in near))
    print("  寄存器: " + " ".join("%s=%08X" % (k, v) for k, v in regs.items()))
    cb = rd(addr, 16)
    print("  ★崩溃处字节: %s" % (" ".join("%02X" % c for c in cb) if cb else "(该页不在转储里 ✗)"))
    # EBP 链（VM/无帧代码会失效 ⇒ 只有两层 ntdll 属正常 ✓）
    ebp, seen = regs.get("ebp", 0), set()
    print("  ---- EBP 链（VM 代码不维护 EBP ⇒ 短属正常 ✓）----")
    for _ in range(24):
        if ebp < 0x1000 or ebp in seen:
            break
        seen.add(ebp)
        pair = rd(ebp, 8)
        if len(pair) < 8:
            break
        nxt, ret = struct.unpack("<II", pair)
        tag = ""
        for base, sz, nm in mods:
            if base <= ret < base + sz:
                tag = "  ← %s+0x%X" % (nm, ret - base)
                break
        print("     ret=%08X%s" % (ret, tag))
        ebp = nxt
    print()


def strings(path, keys):
    b, _dirs, _stream, ranges = load(path)
    pat = re.compile(rb"[ -~]{6,}")
    print("=== 字符串扫描 %s（块 %d）===" % (os.path.basename(path), len(ranges)))
    for s, sz, r in sorted(ranges):
        for m in pat.finditer(b[r:r + sz]):
            t = m.group(0).decode("latin-1")
            low = t.lower()
            if not keys or any(k in low for k in keys):
                print("  @%08X  %s" % (s + m.start(), t[:120]))


def stacks(path, top=600):
    """★扫**每个线程的栈**，把里面"指向某个模块（尤其是游戏 exe）"的 DWORD 全列出来。

    用途：崩溃的 `eip` 落在"数据/堆区"（= 返回地址或函数指针被写坏 ✓）时，
        `EBP` 链必然断 ✗（被写坏的那段根本不维护帧 ✓）
        ⇒ **唯一能反推"当时是谁在跑"的办法 = 把栈上残留的代码指针捞出来** ✓✓
    判读：游戏 exe = `0x401000`~`0xD66000`（`.text` ✓ base 0x400000 ✓）
        ⇒ 出现 `GundamOnline_CHINA.exe+0x……` 的那几条 = 出事时**正在跑的游戏函数** ✓
    """
    b, _dirs, stream, ranges = load(path)
    mods = modules(b, stream)
    rd = reader(b, ranges)
    rva, _ = stream(3)
    if not rva:
        print("!! 无 ThreadList")
        return

    def owner(v):
        for base, sz, nm in mods:
            if base <= v < base + sz:
                return "%s+0x%X" % (nm, v - base)
        return None

    n = struct.unpack_from("<I", b, rva)[0]
    print("=== 扫栈 %s（线程 %d）===" % (os.path.basename(path), n))
    for i in range(n):
        base = rva + 4 + i * 48
        tid, = struct.unpack_from("<I", b, base)
        s, sz, r = struct.unpack_from("<QII", b, base + 24)          # Stack 描述符 ✓
        csz, crva = struct.unpack_from("<II", b, base + 40)          # ThreadContext ✓
        esp = eip = 0
        if crva:
            eip = struct.unpack_from("<I", b, crva + 184)[0]
            esp = struct.unpack_from("<I", b, crva + 196)[0]
        stack = b[r:r + sz] if sz else b""
        if not stack:
            print("  线程 %-6d 栈不在转储里 ✗（eip=%08X）" % (tid, eip))
            continue
        hits = []
        for off in range(0, len(stack) - 3, 4):
            v = struct.unpack_from("<I", stack, off)[0]
            o = owner(v)
            if o:
                hits.append((s + off, v, o))
        cur = owner(eip) or "**无模块(动态/被写坏)**"
        print("  线程 %-6d eip=%08X (%s)  栈=%08X+%X  命中代码指针 %d"
              % (tid, eip, cur, s, sz, len(hits)))
        for addr, v, o in hits[:top]:
            print("        [%08X] %08X  %s" % (addr, v, o))


def main(argv):
    if not argv:
        print(__doc__)
        return
    if argv[0] in ("--str", "--stack"):
        if len(argv) < 2:
            print(__doc__)
            return
        if argv[0] == "--str":
            strings(argv[1], [k.lower() for k in argv[2:]])
        else:
            stacks(argv[1])
        return
    rest = argv[1:] if argv[0] == "--all" else argv
    files = []
    for p in rest:
        files.extend(sorted(glob.glob(p)) if any(c in p for c in "*?") else [p])
    for f in files:
        try:
            basic(f)
        except Exception as e:
            print("!! %s: %s\n" % (f, e))


if __name__ == "__main__":
    main(sys.argv[1:])

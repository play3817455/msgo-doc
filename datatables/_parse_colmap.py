# -*- coding: utf-8 -*-
"""把 _out_ida_reader_asm.txt 解析成「取列调用点 → 列号 → 紧随落点偏移」表。

口径：
  * 调用点 = call 到 CSV 助手族（BBB370/BBB3F0/BBB470/BBB4F0/BBB920/456D90/5976F0/5978A0/597D00/597AF0/596xxx）
  * 列号 = 调用点前最近一条「带立即数的 push / mov reg,imm」（0..255）
  * 落点 = 调用点到下一次调用之间出现的 `mov [reg+disp],..` / `lea reg,[reg+disp]` / `fstp [reg+disp]` 的 disp
"""
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PATH = r"datatables\_out_ida_reader_asm.txt"
OUT = r"datatables\_out_colmap_ws.txt"

HELPERS = {
    "sub_BBB370", "sub_BBB3F0", "sub_BBB470", "sub_BBB4F0", "sub_BBB920", "sub_456D90",
    "sub_5976F0", "sub_5978A0", "sub_597D00", "sub_597AF0", "sub_56F550",
    "sub_5968A0", "sub_596990", "sub_596A80", "sub_596B70", "sub_596510", "sub_5965F0",
    "sub_5964A0", "sub_596C60", "sub_596D50", "sub_596E40", "sub_596100", "sub_483020",
    "sub_40CE20", "sub_469990", "sub_BBB130", "sub_BBB250", "sub_408530",
}
LINE = re.compile(r"^\s+(0x[0-9a-f]+)\s+(\S+)\s*(.*?)(?:\s*;\s*->\s*(\S+))?$")
MEM = re.compile(r"\[([a-z0-9]+)(?:\s*([+-])\s*(0x[0-9a-f]+|\d+))?\]")


def disp_of(op):
    m = MEM.search(op)
    if not m:
        return None
    base, sign, val = m.groups()
    if val is None:
        return (base, 0)
    v = int(val, 16) if val.startswith("0x") else int(val)
    if sign == "-":
        v = -v
    return (base, v)


def parse(path):
    blocks, cur = [], None
    for raw in open(path, encoding="utf-8"):
        s = raw.rstrip("\n")
        if s.startswith("### "):
            cur = {"head": s, "ins": []}
            blocks.append(cur)
            continue
        if cur is None:
            continue
        m = LINE.match(s)
        if not m:
            continue
        ea, mnem, ops, callee = m.groups()
        cur["ins"].append({"ea": int(ea, 16), "mnem": mnem, "ops": ops, "callee": callee})
    return blocks


log = []
for blk in parse(PATH):
    log.append("=" * 100)
    log.append(blk["head"])
    ins = blk["ins"]
    for i, x in enumerate(ins):
        if x["mnem"] != "call" or (x["callee"] or "") not in HELPERS:
            continue
        # 列号：往前找最近一条立即数（跳过 mov reg,reg 等）
        col = None
        for j in range(i - 1, max(-1, i - 12), -1):
            p = ins[j]
            if p["mnem"] == "call":
                break
            if p["mnem"] == "push":
                v = p["ops"].strip()
                if re.fullmatch(r"0x[0-9a-f]+|\d+", v):
                    col = int(v, 16) if v.startswith("0x") else int(v)
                    break
            if p["mnem"] == "mov":
                a, _, b = p["ops"].partition(", ")
                b = b.strip()
                if re.fullmatch(r"0x[0-9a-f]+|\d+", b) and "[" not in a:
                    col = int(b, 16) if b.startswith("0x") else int(b)
                    break
        # 落点：往后找第一条内存写/lea
        stores = []
        for j in range(i + 1, min(len(ins), i + 14)):
            n = ins[j]
            if n["mnem"] == "call":
                break
            d = disp_of(n["ops"])
            if d and n["mnem"] in ("mov", "lea", "fstp", "movzx", "movsx"):
                stores.append(f"{n['mnem']} {n['ops']} @{n['ea']:#x}")
                if len(stores) >= 3:
                    break
        log.append(f"  call {x['ea']:#010x} -> {x['callee']:12s} col={col}")
        for s in stores:
            log.append(f"        store: {s}")

text = "\n".join(log) + "\n"
print(text)
open(OUT, "w", encoding="utf-8").write(text)

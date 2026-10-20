# -*- coding: utf-8 -*-
"""从 _out_ida_readers_pseudo.txt 抽取 WEAPON_SETTING 静态读列集合，并与 schema 对账。

判据：这些助手函数的**最后一个实参**就是 CSV 列号（已逐条对照反汇编确认）：
  sub_BBB370(row,col) / sub_BBB3F0 / sub_BBB470 / sub_BBB4F0(buf,row,col)
  sub_456D90(row,col) / sub_BBB920(buf,row,col) / sub_5976F0(buf,row,col)(= 包 sub_BBB920)
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PSEUDO = r"datatables\_out_ida_readers_pseudo.txt"
SCHEMA = r"db_design\schema\cfg\tables\WEAPON_SETTING.json"

HELPERS = ("BBB370", "BBB3F0", "BBB470", "BBB4F0", "BBB920", "456D90", "5976F0")
CALL = re.compile(r"sub_(?:" + "|".join(HELPERS) + r")\(")


def section(text, header):
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("### ") and header in ln:
            start = i
            break
    if start is None:
        raise SystemExit(f"no section {header}")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("### "):
            end = j
            break
    return "\n".join(lines[start:end])


def last_arg(src, open_paren_idx):
    depth = 0
    args = []
    cur = []
    for k in range(open_paren_idx, len(src)):
        ch = src[k]
        if ch == "(":
            depth += 1
            if depth == 1:
                continue
        elif ch == ")":
            depth -= 1
            if depth == 0:
                args.append("".join(cur).strip())
                break
        if depth >= 1:
            cur.append(ch)
        if depth == 1 and ch == ",":
            args.append("".join(cur[:-1]).strip())
            cur = []
    return args[-1] if args else ""


def parse_col(arg):
    a = arg.replace(" ", "")
    m = re.fullmatch(r"(0x[0-9a-fA-F]+|\d+)[uU]?(?:\.0)?", a)
    if not m:
        return None
    v = m.group(1)
    return int(v, 16) if v.lower().startswith("0x") else int(v)


text = open(PSEUDO, encoding="utf-8").read()
sec = section(text, "WEAPON_SETTING  sub_597F50")

found = {}
for m in CALL.finditer(sec):
    helper = sec[m.start():m.end() - 1].split("sub_")[1]
    arg = last_arg(sec, m.end() - 1)
    col = parse_col(arg)
    if col is None:
        print(f"  !! 未解析 col: {helper} ... {arg!r}")
        continue
    found.setdefault(col, []).append(helper)

schema = json.loads(open(SCHEMA, encoding="utf-8").read())
sch_conf = {c["csv_index"] for c in schema["columns"] if c.get("status") == "confirmed"}
sch_gap = {c["csv_index"] for c in schema["columns"] if c.get("status") == "gap"}
sch_all = {c["csv_index"] for c in schema["columns"]}

static = set(found)
print("=" * 90)
print(f"WEAPON_SETTING: 静态抽到 {len(static)} 个读列：{sorted(static)}")
print(f"schema confirmed={len(sch_conf)} gap={len(sch_gap)} total={len(sch_all)} max_csv={max(sch_all)}")
print("=" * 90)

print("\n[1] schema 标 gap，但 reader 真读（应订正）：")
for c in sorted(sch_gap & static):
    print(f"  col{c:<4} via {found[c]}")
print(f"  合计 {len(sch_gap & static)}")

print("\n[2] schema 标 gap，静态也未见读（保持 gap）：")
print("  " + ", ".join(f"col{c}" for c in sorted(sch_gap - static)))

print("\n[3] schema 标 confirmed，但静态未见读（需人工复核）：")
print("  " + ", ".join(f"col{c}" for c in sorted(sch_conf - static)))

print("\n[4] 静态读到、schema 完全没有的列（行宽可能不足）：")
missing = sorted(static - sch_all)
print("  " + (", ".join(f"col{c}" for c in missing) if missing else "（无）"))
if missing:
    print(f"  → max 读列 {max(static)} vs schema max {max(sch_all)}")

print("\n[5] 每列 col → 内存/名字（schema）与 reader 出处：")
for c in sorted(static):
    col = next((x for x in schema["columns"] if x["csv_index"] == c), None)
    nm = (col or {}).get("db_column") or "?"
    st = (col or {}).get("status") or "MISSING"
    print(f"  col{c:<4} status={st:<9} {nm:<28} via {','.join(found[c])}")

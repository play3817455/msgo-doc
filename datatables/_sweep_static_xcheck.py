# -*- coding: utf-8 -*-
"""三路对账：schema declared/non_gap  vs  Unicorn 仿真 observed  vs  IDA 静态 cols
-> datatables/_out_static_xcheck.json / .txt / datatables/18-静态复核.md

关键点：仿真若被 count/timeout 截断（EMU-CUT）或崩（UC_ERR_*），其 observed 只是**下界**，
不能用它判"schema 高估"；那些表必须以静态 cols 为准。
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
L = []
A = L.append


def load(n):
    return json.load(open(os.path.join(HERE, n), encoding="utf-8"))


emu = load("_out_emu_readers.json")
sta = load("_out_static_cols.json")
wl = load("_out_reader_list.json")

rows = []
for r, e in sorted(emu.items()):
    s = sta.get(r, {})
    tabs = e["tables"]
    cur = wl.get(r) or {}
    non_gap = sorted(set(cur.get("non_gap") or e["non_gap"]))
    declared = cur.get("declared") or e["declared"]
    obs = sorted(set(e["observed"]))
    stat = sorted(set(s.get("cols", [])))
    emu_bad = bool(e["err"])
    dyn_ok = (not emu_bad) and not s.get("unresolved")
    # 以「可信来源」为准：仿真干净用仿真；否则用静态（若静态有未解析则标注）
    if not emu_bad:
        truth, src = obs, "仿真"
    elif stat:
        truth, src = stat, "静态"
    else:
        truth, src = obs, "仿真(坏)"
    miss = sorted(set(non_gap) - set(truth))   # schema 声明读、真值没读到 => 疑似高估
    extra = sorted(set(truth) - set(non_gap))  # 真值读到、schema 没声明 => schema 漏列
    rows.append({
        "reader": r, "tables": tabs, "err": e["err"], "mode": e["retry"],
        "declared": declared, "non_gap": non_gap,
        "observed": obs, "static": stat, "static_unresolved": len(s.get("unresolved", [])),
        "truth": truth, "src": src,
        "missing_vs_schema": miss, "extra_vs_schema": extra,
        "match": not miss and not extra,
    })

res = {
    "n_readers": len(rows),
    "match": [x for x in rows if x["match"]],
    "diff": [x for x in rows if not x["match"]],
    "emu_bad": [x for x in rows if x["err"]],
}
json.dump(res, open(os.path.join(HERE, "_out_static_xcheck.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

n_bad = len(res["emu_bad"])
n_cut = len([x for x in res["emu_bad"] if "EMU-CUT" in (x["err"] or "")])
n_crash = n_bad - n_cut
A("# 18 读表真值静态复核（IDA hexrays 常量抽取 vs schema vs 仿真）")
A("")
A("> 复现：`py_exec_file datatables/_ida_static_cols.py`（在 IDA 内跑）→ `python datatables/_sweep_static_xcheck.py`")
A("")
A("## 0. 为什么需要静态复核")
A("")
A("`_emu_readers.py` 原来只把 `UcError` 当失败，但 Unicorn 在 **count/timeout 用尽**时是")
A("**静默返回**的：reader 早期调用运行时 map/vector 查询（假对象→死循环）的用例会被截断，")
A("却记为 `err=None`，于是 `observed` 只是**下界**，据此判「schema 高估」会得出相反结论。")
A("")
A("现已加两条判别：`EMU-CUT(limit)`（EIP 未到 RET_MAGIC）与 `TRUNCATED`（栈未复原）；")
A("对这类 reader 改用 IDA hexrays 静态抽列（含包装函数 `(dst,tbl,col)` 透传）作为真值。")
A("")
A("## 1. 总览")
A("")
A(f"- 仿真有问题的 reader：**{n_bad}**（其中 EMU-CUT 截断 **{n_cut}**、崩在缺映射/断言 **{n_crash}**）")
A(f"- 三路对账「schema == 真值」：**{len(res['match'])}** / {len(rows)}")
A(f"- 有差异：**{len(res['diff'])}**")
A("")
A("## 2. 仿真不可信（EMU-CUT / 崩溃）的 reader 及其静态真值")
A("")
A("| reader | 表 | 仿真状态 | 仿真 observed | 静态 cols | schema non_gap | 静态 vs schema |")
A("|---|---|---|---|---|---|---|")
for x in res["emu_bad"]:
    tag = "差异" if not x["match"] else "一致 ✓"
    A(f"| `{x['reader']}` | {','.join(x['tables'])} | {(x['err'] or '')[:22]} | "
      f"{len(x['observed'])} 列 | **{len(x['static'])} 列** | {len(x['non_gap'])} 列 | {tag} |")
A("")
for x in res["emu_bad"]:
    A(f"### `{x['reader']}` ({','.join(x['tables'])})")
    A("")
    A(f"- 仿真 observed（下界）：`{x['observed']}`")
    A(f"- 静态 cols（真值）：`{x['static']}`（未解析参数 {x['static_unresolved']} 处）")
    A(f"- schema non_gap：`{x['non_gap']}`")
    if x["missing_vs_schema"]:
        A(f"- **schema 声明但真值未读到**：`{x['missing_vs_schema']}`")
    if x["extra_vs_schema"]:
        A(f"- **真值读到但 schema 未声明**：`{x['extra_vs_schema']}`")
    if x["match"]:
        A("- ⇒ 三方一致：schema 无需改动 ✓")
    A("")
A("## 3. 仿真可信、但仿真≠schema 的 reader（逐条核查）")
A("")
A("| reader | 表 | schema 有仿真无 | 仿真有 schema 无 | 静态 cols | 结论 |")
A("|---|---|---|---|---|---|")
for x in res["diff"]:
    if x["err"]:
        continue
    A(f"| `{x['reader']}` | {','.join(x['tables'])} | {x['missing_vs_schema']} | {x['extra_vs_schema']} | "
      f"{len(x['static'])} 列 | {'三方一致' if x['static'] and x['match'] else '需核查'} |")
A("")

txt = "\n".join(L)
open(os.path.join(HERE, "_out_static_xcheck.txt"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
print(f"\n--- diff 明细 ---")
for x in res["diff"]:
    print(f"{x['reader']:14s} {','.join(x['tables'])[:20]:20s} err={str(x['err'])[:20]:20s} "
          f"src={x['src']} miss={x['missing_vs_schema'][:8]} extra={x['extra_vs_schema'][:8]}")

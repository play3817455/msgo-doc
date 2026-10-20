# -*- coding: utf-8 -*-
"""把 Ids reader 仿真真值 (_out_emu_readers.json) 与 cfg table schema 逐表对账
-> datatables/_out_sweep_verdict.json / _out_sweep_verdict.txt

判据（每个 reader = 一张或多张表）：
  A 读集   : reader 实际读到的 CSV 列号集合  vs  schema 里 is_gap != true 的 csv_index 集合
  B 内存序 : 只在「高置信写点」(via=marker/conv-marker，值就是助手返回值) 上比较
             schema 的 memory_offset 与仿真的 offset 作为**多重集**是否一致：
               - 一致 -> 再比 csv_index<->offset 的配对 -> 配对不同 = 真错位(#50 类)
               - 差一个常量 -> 再比移位后的配对
               - 否则 -> offset 约定不同，不做判定（只提示）
"""
import io
import json
import os
import sys
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")


def load_tables():
    out = {}
    for fn in sorted(os.listdir(TABLES_DIR)):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(TABLES_DIR, fn), encoding="utf-8"))
        out[d.get("table") or fn[:-5]] = d
    return out


# ★ 静态反汇编读集覆盖（2026-10-05）。
#
# 为什么需要：`sub_A47BC0` 是**回调分派**式行解析——它自己只读 col0（属性名），
# 然后经容器 vtable 查词表选出子表，由**子表的 AddRow 读 col1（键）**、
# **子表的 vtable[0] 读值列**（列号随属性名而定，如 WEAPON 的 STABILITY=col2..col6、
# SHIELD=col2..col8；MSMA 的 BOOST_SPEED=col2..col15、JUMP=col2..col13、RESPAWN=col2..col12）。
# 仿真器没有那两个 vtable 对象（call [vtable[0]] ⇒ eip=0x2），**必然** `UC_ERR_EXCEPTION`，
# 于是这两张表的读集永远只有 [0]。所以这里用**静态反汇编**给出确证读集：
# 逐个子表 reader 扫 `push imm` + `call sub_BBB370/470/4F0`，取最大列号。
STATIC_READSET = {
    # SHIELD sub_595D60 读 csv2..csv8 → 0..8
    "WEAPON_BATTLE_DETAIL": sorted(range(0, 9)),
    # BOOST_SPEED sub_57B9F0 读 csv2..csv15 → 0..15
    "MSMA_BATTLE_DETAIL": sorted(range(0, 16)),
}


def schema_readset(t):
    """schema 认为 reader 会读的列号（status != gap）

    返回 (non, gap, exempt)：
      non   = 参与仿真读集比对的列号 -> memory_offset
      gap   = 声明为 gap 的列号
      exempt= **判据豁免**列（schema 里带 `emu_exempt` 说明）：这些列要么是表级键
              （值提取器式 reader 不读 col0，由容器 AddRow 读），要么是**条件列**
              （列号随行数据浮动，例如 ITEM_PART 的 MS_BOOST_GAUGE_RECOV 余量槽位）。
              仿真读集天然看不到它们，故不计入比对，但仍在报告里列明原因。
    """
    cols = t.get("columns") or []
    if isinstance(cols, dict):
        cols = list(cols.values())
    non, gap, exempt = {}, set(), {}
    for ci, c in enumerate(cols):
        idx = c.get("csv_index", ci)
        st = (c.get("status") or "").lower()
        if c.get("is_gap") or st == "gap":
            gap.add(idx)
        elif c.get("emu_exempt"):
            exempt[idx] = str(c.get("emu_exempt"))
        else:
            non[idx] = c.get("memory_offset")
    return non, gap, exempt


def sim_offsets(v):
    """高置信 (csv 列号 -> 内存偏移)：只取 via=marker/conv-marker 的写点"""
    cand = defaultdict(list)
    for s in v["stores"]:
        if s["n"] is None:
            continue
        if s.get("via") not in ("marker", "conv-marker"):
            continue
        cand[s["n"]].append(s["off"])
    out = {}
    for n, offs in cand.items():
        out[n] = Counter(offs).most_common(1)[0][0]
    return out


def best_shift(a, b):
    """找 c 使 sorted(a) == sorted(x+c for x in b) —— a 是 schema, b 是仿真"""
    if len(a) != len(b):
        return None
    sa, sb = sorted(a), sorted(b)
    c = sa[0] - sb[0]
    if all(x + c == y for x, y in zip(sb, sa)):
        return c
    return None


def judge(name, v, tables):
    tnames = v["tables"]
    obs = {n for n in v["observed"] if n is not None}
    res = {"reader": name, "tables": tnames}
    per = []
    for tn in tnames:
        t = tables.get(tn)
        if t is None:
            per.append({"table": tn, "verdict": "NO-SCHEMA"})
            continue
        non, gap, exempt = schema_readset(t)
        if tn in STATIC_READSET:
            obs_t = set(STATIC_READSET[tn])
            miss = sorted(set(non) - obs_t)
            extra = sorted(obs_t - set(non))
            verdict = "STATIC-OK" if not (miss or extra) else "STATIC-DIFF"
            note = (
                f"静态反汇编读集 csv 0..{max(obs_t)}（子表 vtable[0] 各读各的值槽；"
                f"仿真走回调 vtable 必然失败）"
                + (f" schema有静态无={miss} 静态有schema无={extra}" if (miss or extra) else "")
            )
            per.append({"table": tn, "verdict": verdict, "note": note,
                        "gap": sorted(gap), "reads": sorted(obs_t)})
            continue
        ex_note = ""
        if exempt:
            ex_note = "｜豁免=" + ",".join(f"{i}({r[:24]})" for i, r in sorted(exempt.items()))
        sim_off = sim_offsets(v)
        if v["err"]:
            verdict, note = "EMU-PARTIAL", v["err"][:60]
        else:
            miss = sorted(set(non) - obs)
            extra = sorted(obs - set(non))
            if miss or extra:
                verdict = "READSET-DIFF"
                note = f"schema有仿真无={miss} 仿真有schema无={extra}"
            elif len(sim_off) >= 3 and len(sim_off) == len(non) and all(
                non[i] is not None for i in non
            ):
                # 读集完全一致，再比内存序
                s_off = [non[i] for i in sorted(non)]
                r_off = [sim_off[i] for i in sorted(sim_off)]
                if Counter(s_off) == Counter(r_off):
                    same = all(non[i] == sim_off[i] for i in non)
                    verdict = "OK" if same else "MISALIGN"
                    note = f"offset 多重集一致 配对{'一致' if same else '不同'}"
                else:
                    c = best_shift(s_off, r_off)
                    if c is not None:
                        same = all(non[i] == sim_off[i] + c for i in non)
                        verdict = "OK" if same else "MISALIGN"
                        note = f"offset 差常量 {c:+d} 配对{'一致' if same else '不同'}"
                    else:
                        verdict, note = "OFFSET-UNSURE", (
                            f"schema={sorted(non.values())} 仿真={sorted(sim_off.values())}"
                        )
            else:
                verdict, note = "READSET-OK", f"仅读集可比(高置信写点 {len(sim_off)}/{len(non)})"
            note += ex_note
        per.append({"table": tn, "verdict": verdict, "note": note, "gap": sorted(gap),
                    "exempt": {str(k): v2 for k, v2 in sorted(exempt.items())}})
    res["per"] = per
    res["err"] = v["err"]
    res["reads"] = sorted(obs)
    return res


def main():
    tables = load_tables()
    d = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
    verdicts = [judge(k, v, tables) for k, v in sorted(d.items())]

    # 按表汇总（多表共用 reader 的拆开）
    bytable = {}
    for r in verdicts:
        for p in r["per"]:
            bytable.setdefault(
                p["table"], (p["verdict"], p["note"], r["reader"], p.get("reads") or r["reads"]))

    allt = sorted(tables)
    covered = [t for t in allt if t in bytable]
    cnt = Counter(v[0] for v in bytable.values())

    lines = []
    lines.append(f"表总数 {len(allt)}｜仿真覆盖 {len(covered)}｜未覆盖 {sorted(set(allt)-set(covered))}")
    lines.append("判定分布: " + "  ".join(f"{k}={c}" for k, c in cnt.most_common()))
    lines.append("")
    for v in ("MISALIGN", "READSET-DIFF", "OFFSET-UNSURE", "EMU-PARTIAL", "STATIC-DIFF"):
        rows = [(t, meta) for t, meta in sorted(bytable.items()) if meta[0] == v]
        if not rows:
            continue
        lines.append(f"==== {v} ({len(rows)}) ====")
        for t, (vd, note, reader, reads) in rows:
            lines.append(f"  {t:28s} {reader:12s} {note[:120]}")
        lines.append("")
    rows = [(t, meta) for t, meta in sorted(bytable.items())
            if meta[0] in ("OK", "READSET-OK", "STATIC-OK")]
    lines.append(f"==== 一致 ({len(rows)}) ====")
    lines.append("  " + "  ".join(t for t, _ in rows))
    stat = sorted(t for t, m in bytable.items() if m[0] == "STATIC-OK")
    lines.append("")
    lines.append(f"★ 其中读集由**静态反汇编**背书（仿真结构性失败）{len(stat)} 张: " + ", ".join(stat))
    text = "\n".join(lines)
    print(text)
    json.dump({"by_table": {k: v for k, v in bytable.items()}, "readers": verdicts},
              open(os.path.join(HERE, "_out_sweep_verdict.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    open(os.path.join(HERE, "_out_sweep_verdict.txt"), "w", encoding="utf-8").write(text + "\n")


main()

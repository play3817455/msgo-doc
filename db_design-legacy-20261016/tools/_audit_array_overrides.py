# -*- coding: utf-8 -*-
"""检查 `_overrides/*.json` 里对数组字段打的元素线长，是否与元素复合体一致。

动机：`SC-0x305D.members` 的 override 写 `34·N`，理由「读取器 sub_B454D0 整函数扫描
4+25+1+2+1+1=34」——但该读取器体内 **嵌套调用了 avatar 读取器 sub_B068B0（18B）**，
真正的线消耗是 52。同一批（26 行未建模数组）都是用「整函数扫描」定的元素线长，
凡元素读取器**体内还嵌套别的读取器**的，都会同样被低估。

判据：override 声明的元素线长 k（`k·N` / `k·变量` / 纯 `k`）
      ↔ 元素复合体 `composites/<array<X,...> 里的 X>.json` 的 `length`。
只看能按名字取到复合体的行。
"""
import io
import json
import os
import re
import sys

CMD = os.path.join("schema", "commands")
OVR = os.path.join(CMD, "_overrides")
CMP = os.path.join("schema", "composites")

ARR = re.compile(r"^array<\s*([A-Za-z_][\w]*|u8|u16|u32|u64|i8|i16|i32|i64)\s*,")


def elem_len(decl):
    """`34·N` / `114·N` / `80` / `401·ms_count` → 数字部分。"""
    m = re.match(r"^\s*(\d+)", str(decl or ""))
    return int(m.group(1)) if m else None


def main():
    rows = []
    for p in sorted(os.listdir(OVR)):
        if not p.endswith(".json"):
            continue
        d = json.load(io.open(os.path.join(OVR, p), encoding="utf-8"))
        for fname, patch in (d.get("patch") or {}).items():
            if not isinstance(patch, dict):
                continue
            wt = str(patch.get("wire_type") or "")
            m = ARR.match(wt)
            if not m:
                continue
            elem = m.group(1)
            k = elem_len(patch.get("length"))
            cmpp = os.path.join(CMP, elem + ".json")
            clen = None
            if os.path.isfile(cmpp):
                clen = json.load(io.open(cmpp, encoding="utf-8")).get("length")
            rows.append({
                "cmd": d.get("id"), "field": fname, "elem": elem,
                "declared": patch.get("length"), "k": k,
                "composite_len": clen,
                "mismatch": (clen is not None and k is not None and clen != k),
            })
    ok = [r for r in rows if not r["mismatch"]]
    bad = [r for r in rows if r["mismatch"]]
    nocomp = [r for r in rows if r["composite_len"] is None]
    print("数组 override 共 %d 处：一致 %d / 不一致 %d / 无同名复合体 %d"
          % (len(rows), len(ok), len(bad), len(nocomp)))
    print()
    print("== 不一致（override 声明的元素线长 ≠ 元素复合体线长）==")
    for r in bad:
        print("  %-46s %-14s elem=%-26s declared=%-8s composite=%s"
              % (str(r["cmd"])[:46], r["field"][:14], r["elem"][:26],
                 str(r["declared"])[:8], r["composite_len"]))
    print()
    print("== 无同名复合体（无法用本条判据核）==")
    for r in nocomp:
        print("  %-46s %-14s elem=%-26s declared=%s"
              % (str(r["cmd"])[:46], r["field"][:14], r["elem"][:26], r["declared"]))


if __name__ == "__main__":
    sys.exit(main())

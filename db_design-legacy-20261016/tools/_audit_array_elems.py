# -*- coding: utf-8 -*-
"""全量检查：每条命令里 `array<X,...>` 字段声明的**元素线长**是否等于 `composites/X` 的线长。

为什么单列这一项：`audit_sources.py` 拿「声明长度 ↔ 复合体长度」核对，但对数组行
而言，那个「长度」是 `k·N`（元素线长 k、元素数 N）或固定元数时的**总长**，
两种写法都不是复合体长度本身 —— 于是这些行被安静地跳过了。
`SC-0x305D.members` 的 `34·N`（真值 52）就是这么漏掉的。

判据：
  * `array<X,N>` / `array<X>`（**变长**，计数在线上）→ 声明形如 `k·N` / `k·变量`
    或纯 `k`：取前导数字 k 与 `composites/X.json` 的 `length` 比。
  * `array<X,5>`（**固定元数**）→ 声明是**总长**，与 `k × 复合体长度` 比。
"""
import io
import json
import os
import re

CMD = os.path.join("schema", "commands")
CMP = os.path.join("schema", "composites")

ARR = re.compile(r"^array<\s*([A-Za-z_][\w]*)")
SCALAR_ELEM = {"u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64", "f32", "f64", "char", "byte", "bool"}


def leading_int(s):
    m = re.match(r"^\s*(\d+)", str(s or ""))
    return int(m.group(1)) if m else None


def main():
    rows = []
    for name in sorted(os.listdir(CMD)):
        if not name.endswith(".json") or name.startswith("_") or name == "index.json":
            continue
        cmd = json.load(io.open(os.path.join(CMD, name), encoding="utf-8"))
        for f in cmd.get("fields", []):
            wt = str(f.get("wire_type") or "")
            if not wt.startswith("array<"):
                continue
            m = ARR.match(wt)
            if not m:
                continue
            elem = m.group(1)
            if elem in SCALAR_ELEM:
                continue
            cmpp = os.path.join(CMP, elem + ".json")
            if not os.path.isfile(cmpp):
                rows.append({"cmd": cmd["id"], "field": f.get("name"), "elem": elem,
                             "declared": f.get("length"), "clen": None, "why": "无同名复合体"})
                continue
            clen = json.load(io.open(cmpp, encoding="utf-8")).get("length")
            # 固定元数：`array<X,5>` 的第二段是数字
            fixed = re.match(r"^array<[^,]+,\s*(\d+)\s*>", wt)
            d = leading_int(f.get("length"))
            if fixed:
                n = int(fixed.group(1))
                want = (clen or 0) * n
                bad = (d is not None and clen and d != want)
                note = "固定 %d 元：声明应为总长 %s" % (n, want)
            else:
                bad = (d is not None and clen is not None and d != clen)
                note = "变长：声明应为元素线长 %s" % clen
            if d is None:
                continue
            rows.append({"cmd": cmd["id"], "field": f.get("name"), "elem": elem,
                         "declared": f.get("length"), "clen": clen,
                         "why": "" if not bad else note})
    bad = [r for r in rows if r["why"] and r["why"] != "无同名复合体"]
    noc = [r for r in rows if r["why"] == "无同名复合体"]
    print("受检数组字段（元素为结构体）共 %d 处；不一致 %d；无同名复合体 %d"
          % (len(rows), len(bad), len(noc)))
    print()
    for r in bad:
        print("  %-48s %-16s elem=%-24s declared=%-9s composite=%s   %s"
              % (r["cmd"][:48], str(r["field"])[:16], r["elem"][:24],
                 str(r["declared"])[:9], r["clen"], r["why"]))
    if noc:
        print()
        print("== 无同名复合体（该数组元素尚未建模，属已知缺口）==")
        for r in noc:
            print("  %-48s %-16s elem=%s" % (r["cmd"][:48], str(r["field"])[:16], r["elem"]))


if __name__ == "__main__":
    main()

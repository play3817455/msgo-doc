# -*- coding: utf-8 -*-
"""_survey_unmodeled.py —— 普查「聚合字段挂不到 composites/」的命令（站点会显示「未建模」）。

用法：
    python db_design/tools/_survey_unmodeled.py            # 全库
    python db_design/tools/_survey_unmodeled.py --batch 6  # 只看某批

判据与 `build_site.py` 的渲染口径一致：字段线类型像结构体/结构体数组，
但 `composite_ref` / `element_composite_ref` 都挂不上，或挂了却不在 `composites/` 里。
另附一类：字段含义里还留着「内部成员未逐一命名」的过期句。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CMD_DIR = ROOT / "schema" / "commands"
COMP_DIR = ROOT / "schema" / "composites"

SCALAR = {"u8", "i8", "char", "bool", "u16", "i16", "u32", "i32", "u64", "i64",
          "f32", "f64", "str", "bytes", "elem", "struct", "opcode"}

STRUCTY = re.compile(r"^(struct|array\s*<)|^[A-Za-z_]\w*\s*\[\s*\d*\s*\]$")


def load(path: Path):
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def elem_of(wt: str) -> str | None:
    m = re.match(r"^array\s*<\s*([^,>]+)", wt)
    return m.group(1).strip() if m else None


def looks_structy(wt: str) -> bool:
    wt = wt.strip()
    if not wt:
        return False
    if wt.startswith("struct"):
        return True
    e = elem_of(wt)
    if e is not None:
        return e not in SCALAR
    if wt in SCALAR:
        return False
    # `xxx[73]`：元素名非标量才算结构体数组
    m = re.match(r"^([A-Za-z_]\w*)\s*\[\s*\d*\s*\]$", wt)
    if m:
        return m.group(1) not in SCALAR
    return wt not in SCALAR


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=None)
    args = ap.parse_args()

    comps = {p.stem for p in COMP_DIR.glob("*.json") if not p.name.startswith("_")}

    only: set[str] | None = None
    if args.batch is not None:
        work = load(CMD_DIR / "_meta" / ("batch_%d.json" % args.batch))
        only = {t["id"] for t in work["targets"]}

    unmodeled: list[tuple[str, str, str, str]] = []
    stale_clause: list[tuple[str, str]] = []
    for p in sorted(CMD_DIR.glob("*.json")):
        if p.name.startswith("_") or p.name == "index.json":
            continue
        cmd = load(p)
        if only is not None and cmd["id"] not in only:
            continue
        if (cmd.get("asm_verification") or {}).get("status") not in (
                "ASM-VERIFIED", "BEHAVIOR-DONE"):
            continue
        for f in cmd.get("fields", []):
            if f.get("is_closure"):
                continue
            wt = (f.get("wire_type") or "").strip()
            if not looks_structy(wt):
                continue
            refs = [f.get(k) for k in ("composite_ref", "element_composite_ref")]
            ok = any(r and r in comps for r in refs)
            if not ok:
                e = elem_of(wt)
                unmodeled.append((cmd["id"], f.get("name") or "", wt,
                                  (e if e not in (None, "struct") else "") or f.get("name") or ""))
            text = "%s %s" % (f.get("meaning") or "", f.get("purpose") or "")
            if "未逐一命名" in text:
                stale_clause.append((cmd["id"], f.get("name") or ""))

    print("[survey] 聚合字段挂不到 composite 的命令字段：%d" % len(unmodeled))
    for cid, name, wt, hint in unmodeled:
        print("  %-58s %-24s %-26s 候选=%s" % (cid, name, wt, hint))
    print("[survey] 含义里仍留「未逐一命名」过期句：%d" % len(stale_clause))
    for cid, name in stale_clause:
        print("  %-58s %s" % (cid, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())

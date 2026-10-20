#!/usr/bin/env python3
"""内存链审计的**负控**：证明它还会说「不」。

为什么必须有这个：2026-09-24 之前它一天喊 40 条狼来了（抽取器漏槽 ⇒ 假阳性），
修完抽取器变成 128 pass / 0 fail。一个永远说「全过」的审计和永远说「全错」的
审计一样没有用 —— 两者都在侵蚀「机器可证」这条标准。

做法：拿真实复合体，把某个 memory_offset 挪到「不可能被客户端碰过」的位置
（步进取一个不在 ±3 邻域内的值），断言审计必须报出这个字段。
改的是**内存里的副本**，不落盘。

    python tools/_selftest_memory_audit.py
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit_mem", ROOT / "tools" / "audit_memory_chain.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

# (复合体, 要挪动的字段) —— 都是「刚被抽取器补上证据」的那批，最需要防它变松
CASES = [
    ("pilot", "clan_name"),          # 80，靠 comma 收尾的文本槽循环补上
    ("pilot", "cupteam_name"),       # 120
    ("check_quest", "title"),        # 4，靠带转型的文本槽补上
    ("lvjudge_hist", "termstr_now"),  # 204
    ("ms", "adop_items_eq"),         # 188，靠「下标起点非 0 的数组循环」补上
    ("pointdmg", "gaugedmg"),        # 0，靠 if-continue 上界补上
    ("ext_subrule", "param"),        # 4
    ("buildup_info", "build_num"),   # 0
    ("xwar_ext_rule", "row2"),       # 256，靠和式下标补上
]


def declared_offset(comp: dict, field: str) -> int | None:
    for m in comp.get("members", []):
        if m.get("name") == field:
            return m.get("memory_offset")
    return None


def main() -> int:
    composites = audit.load_composites()
    ida_maps = audit.load_ida_memory_maps()
    bad = 0

    for cid, field in CASES:
        base = audit.audit_composite(cid, copy.deepcopy(composites), ida_maps, save=False)
        if base["status"] != "pass":
            print(f"[FAIL] {cid}.{field}: 基线就不是 pass（{base['issues']}）")
            bad += 1
            continue

        shifted = copy.deepcopy(composites)
        off = declared_offset(shifted[cid], field)
        if off is None:
            print(f"[FAIL] {cid}.{field}: 复合体里没有这个字段的 memory_offset")
            bad += 1
            continue
        # 挪 +7：既超过 nearest_ida_slot 的 ±3 容差，又落在常见数组步长之外
        for m in shifted[cid]["members"]:
            if m.get("name") == field:
                m["memory_offset"] = off + 7

        got = audit.audit_composite(cid, shifted, ida_maps, save=False)
        hit = [i for i in got["issues"] if i.startswith(f"{field}:")]
        ok = got["status"] == "fail" and hit
        print(f"[{'OK ' if ok else 'FAIL'}] {cid}.{field}@{off}→{off + 7}  "
              f"status={got['status']}  {'| '.join(hit[:1])}")
        if not ok:
            bad += 1

    print(f"\nRESULT: {len(CASES) - bad}/{len(CASES)} negative controls caught")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Patch cinfo per-field evidence VAs from the reader disassembly (sub_B45940).

问题：`schema/composites/cinfo.json` 的 `evidence_va` 曾按「一批地址批量填」，中段
（level..capture_unlock_num）整段落到了相邻字段的地址上（level/exp 都记成
`0xB45AA1`＝rank_score 的读点、emb_base..rate_vsl_score 都记成 `0xB45AF6`＝
notice_body 循环的读点、尾部三个字段都记成 `0xB45B65`＝feature_word 循环的读点）。
同一批错误地址还被 clan.json 的 cinfo 来源引用。

口径：`evidence_va` = **该字段本身**的取值指令地址——
- 内联存储（`mov [edi+XX], reg`）→ 存储指令地址；
- 定长走子程序（`call sub_B06230/B02DF0/B02DD0`）→ **call 指令**地址。
地址来自 `disasm sub_B45940`（IDA，2026-09-24）。

用法：`py tools/_patch_cinfo_va.py`
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TODAY = str(date.today())

READER = "sub_B45940"

# cinfo 成员 -> 取值指令 VA（disasm sub_B45940）
CINFO_VA = {
    "clan_id": "0xB4595A",           # mov [edi], edx            mem+0x00
    "troops": "0xB4596F",            # mov [edi+4], dl           mem+0x04
    "npc_id": "0xB45985",            # mov [edi+8], edx          mem+0x08
    "npc_id2": "0xB4599B",           # mov [edi+0Ch], edx        mem+0x0C
    "clan_name": "0xB459B3",         # mov [eax+edi+10h], cl     mem+0x10 (31B)
    "level": "0xB459D2",             # mov [edi+2Fh], al         mem+0x2F
    "exp": "0xB459E8",               # mov [edi+30h], edx        mem+0x30
    "emb_base": "0xB45A02",          # mov [edi+34h], dl         mem+0x34
    "emb_parts1": "0xB45A09",        # call sub_B06230 (edi+35h) mem+0x35
    "emb_parts2": "0xB45A1E",        # call sub_B06230 (edi+36h) mem+0x36
    "member_num": "0xB45A33",        # call sub_B02DF0 (edi+38h) mem+0x38
    "member_max": "0xB45A48",        # call sub_B02DF0 (edi+3Ah) mem+0x3A
    "leader_id": "0xB45A5D",         # call sub_B02DD0 (edi+3Ch) mem+0x3C
    "vs_win": "0xB45A6E",            # call sub_B02DD0 (edi+40h) mem+0x40
    "vs_lose": "0xB45A7F",           # call sub_B02DD0 (edi+44h) mem+0x44
    "rank": "0xB45A90",              # call sub_B02DD0 (edi+48h) mem+0x48
    "rank_score": "0xB45AA1",        # call sub_B02DD0 (edi+4Ch) mem+0x4C
    "rank_rate_vsl": "0xB45AB2",     # call sub_B02DD0 (edi+50h) mem+0x50
    "rate_vsl_score": "0xB45AC3",    # call sub_B02DD0 (edi+54h) mem+0x54
    "offer_is_active": "0xB45AD4",   # call sub_B06230 (edi+58h) mem+0x58
    "notice_body": "0xB45AF6",       # call sub_B06230 (edi+59h+i, 433×) mem+0x59
    "active_time_bits": "0xB45B15",  # call sub_B02DD0 (edi+20Ch) mem+0x20C
    "play_style": "0xB45B29",        # call sub_B06230 (edi+210h) mem+0x210
    "capture_unlock_num": "0xB45B3D",  # call sub_B02DD0 (edi+214h) mem+0x214
    "feature_word": "0xB45B65",      # call sub_B06230 (ebx+edi, 4×28) mem+0x218
}


def patch_cinfo() -> int:
    path = COMP / "cinfo.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for m in data.get("members", []):
        va = CINFO_VA.get(m["name"])
        if not va:
            continue
        for ws in m.get("wire_sources", []):
            ws["evidence_va"] = va
            n += 1
        m["asm_verified"] = True
        m["asm_evidence_va"] = va
        m["asm_audit_date"] = TODAY
    audit = data.setdefault("asm_audit", {})
    audit["verified"] = TODAY
    audit["status"] = "pass"
    audit["note"] = (
        "逐字段重校（py tools/_patch_cinfo_va.py，2026-09-24 复看 disasm sub_B45940）："
        "`evidence_va` = 该字段自身的取值指令——内联存储取存储指令、定长走子程序取 call 指令。"
        "此前中段（level..capture_unlock_num）的地址是批量填的邻字段地址："
        "level/exp 记成 0xB45AA1（rank_score 的读点）、emb_base..rate_vsl_score 记成 0xB45AF6"
        "（notice_body 循环的读点）、active_time_bits..capture_unlock_num 记成 0xB45B65"
        "（feature_word 循环的读点）。"
    )
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def patch_referrers() -> list[str]:
    """其余复合体里引用 cinfo 的 wire_source 同步换成校后的地址。"""
    touched: list[str] = []
    for path in sorted(COMP.glob("*.json")):
        if path.name == "cinfo.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        n = 0
        for m in data.get("members", []):
            for ws in m.get("wire_sources", []):
                if ws.get("struct") != "cinfo":
                    continue
                va = CINFO_VA.get(str(ws.get("field_name") or ""))
                if va and ws.get("evidence_va") != va:
                    ws["evidence_va"] = va
                    n += 1
        if n:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            touched.append(f"{path.stem}({n})")
    return touched


def main() -> None:
    n = patch_cinfo()
    touched = patch_referrers()
    print(f"cinfo: {n} 条 wire_source evidence_va 重校（{len(CINFO_VA)} 个字段）")
    print(f"引用方同步：{', '.join(touched) if touched else '无'}")
    print(f"reader={READER} today={TODAY}")


if __name__ == "__main__":
    main()

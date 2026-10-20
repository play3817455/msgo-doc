#!/usr/bin/env python3
"""Fill missing Chinese meanings in schema JSON."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"

REC_MEANINGS = {
    "rec_vs": "对战场次",
    "rec_vs_win": "对战胜场",
    "rec_vs_lose": "对战败场",
    "rec_vsl_td": "对战塔防场次",
    "rec_vsl_td_win": "对战塔防胜场",
    "rec_vsl_td_lose": "对战塔防败场",
    "rec_xwar": "大规模战场次",
    "rec_xwar_win": "大规模战胜场",
    "rec_xwar_lose": "大规模战败场",
    "rec_xwar_last1": "上一场大规模战场次",
    "rec_xwar_win_last1": "上一场大规模战胜场",
    "rec_xwar_lose_last1": "上一场大规模战败场",
    "rec_xwar_win_term": "本届大规模战胜场",
    "rec_xwar_win_term_last1": "上届大规模战胜场",
    "rec_cmd": "指挥战场次",
    "rec_cmd_win": "指挥战胜场",
    "rec_cmd_lose": "指挥战败场",
    "rec_cmd_last1": "上一场指挥战场次",
    "rec_cmd_win_last1": "上一场指挥战胜场",
    "rec_cmd_lose_last1": "上一场指挥战败场",
    "rec_dc": "断线战场次",
    "rec_dc_win": "断线战胜场",
    "rec_dc_lose": "断线战败场",
    "score_assault_a": "评分·强袭 A",
    "score_assault_b": "评分·强袭 B",
    "score_snipe": "评分·狙击",
    "score_cannon": "评分·炮击",
    "score_support": "评分·支援",
}

PATCHES = {
    ("composites", "cinfo.json"): {"npc_id": "战队 NPC ID", "npc_id2": "第二 NPC ID"},
    ("composites", "ms.json"): {"cost": "机体 COST 值"},
}


def patch_members(data: dict, mapping: dict) -> int:
    n = 0
    for m in data.get("members", []):
        name = m.get("name")
        if name in mapping:
            m["meaning"] = mapping[name]
            n += 1
    return n


def patch_entity_fields(data: dict, mapping: dict) -> int:
    n = 0
    for f in data.get("fields", []):
        name = f.get("name")
        if name in mapping:
            f["meaning"] = mapping[name]
            n += 1
    return n


def main():
    total = 0
    for (sub, fname), field_map in PATCHES.items():
        fp = ROOT / sub / fname
        data = json.loads(fp.read_text(encoding="utf-8"))
        total += patch_members(data, field_map)
        fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for base in ("pilots_list", "pcard"):
        for sub in ("composites", "entities"):
            fp = ROOT / sub / f"{base}.json"
            if not fp.is_file():
                continue
            data = json.loads(fp.read_text(encoding="utf-8"))
            if sub == "composites":
                total += patch_members(data, REC_MEANINGS)
            else:
                total += patch_entity_fields(data, REC_MEANINGS)
            fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ent_ms = ROOT / "entities" / "ms.json"
    if ent_ms.is_file():
        data = json.loads(ent_ms.read_text(encoding="utf-8"))
        total += patch_entity_fields(data, {"cost": "机体 COST 值"})
        ent_ms.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Patched {total} field meanings")


if __name__ == "__main__":
    main()

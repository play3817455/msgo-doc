#!/usr/bin/env python3
"""Round 7 CHARA_PARAM cfg enrichment — cap_flag deep xref + param +392/+400 block."""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "db_design" / "schema" / "cfg" / "tables" / "CHARA_PARAM.json"
MD_PATH = ROOT / "datatables" / "01-列注释" / "04-4-CHARA_PARAM.md"
BATCH_PATH = ROOT / "db_design" / "tools" / "enrich_cfg_ida_batch.py"

# csv_index -> field updates (Round 7 IDA: F6 ?? 48/49/4A scan + hangar/list UI xrefs)
UPDATES_BY_CSV: dict[int, dict] = {
    16: {
        "name": "cap_flag_reserved_b840_2",
        "db_column": "cap_flag_reserved_b840_2",
        "display_name": "能力位 b840.2（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +840 bit2（CSV→sub_582390；全二进制无 test [+840]&4 xref；str_table MS_* 无对应键）",
    },
    17: {
        "name": "cap_flag_reserved_b840_3",
        "db_column": "cap_flag_reserved_b840_3",
        "display_name": "能力位 b840.3（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +840 bit3（CSV→sub_582390；无 runtime test xref）",
    },
    19: {
        "name": "cap_flag_reserved_b840_5",
        "db_column": "cap_flag_reserved_b840_5",
        "display_name": "能力位 b840.5（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +840 bit5（CSV→sub_582390；无 runtime test xref）",
    },
    20: {
        "name": "cap_flag_reserved_b840_6",
        "db_column": "cap_flag_reserved_b840_6",
        "display_name": "物理积分旁路位 +840 bit6",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "582390 CSV20非零规范为CHARA_PARAM+840 bit6；47D230末尾读取此位，4AE900在返回true时跳过53D580物理积分。47D230还包含装备/特殊状态分支，因此此位为0不能证明实际物理更新已开启。旧“无runtime xref/预留”说明错误；其他消费者与原服逐机体取值未穷举。",
    },
    21: {
        "name": "cap_flag_reserved_b840_7",
        "db_column": "cap_flag_reserved_b840_7",
        "display_name": "能力位 b840.7（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +840 bit7（CSV→sub_582390；无 runtime test xref）",
    },
    22: {
        "name": "cap_flag_reserved_b841_0",
        "db_column": "cap_flag_reserved_b841_0",
        "display_name": "能力位 b841.0（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +841 bit0（CSV→sub_582390；无 runtime test xref）",
    },
    26: {
        "name": "cap_flag_reserved_b841_4",
        "db_column": "cap_flag_reserved_b841_4",
        "display_name": "能力位 b841.4（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +841 bit4（CSV→sub_582390；无 runtime test xref）",
    },
    27: {
        "name": "cap_flag_reserved_b841_5",
        "db_column": "cap_flag_reserved_b841_5",
        "display_name": "能力位 b841.5（预留）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "能力位 +841 bit5（CSV→sub_582390；无 runtime test xref）",
    },
    29: {
        "name": "cap_flag_reserved_b841_7",
        "db_column": "cap_flag_reserved_b841_7",
        "display_name": "位置碰撞更新旁路位 +841 bit7",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "meaning": "582390 CSV29非零规范为CHARA_PARAM+841 bit7；478DD0读取该位，4AE900在返回true时跳过普通位置/碰撞更新分支（4ADD60或载体引用分支），角色+12 bit0x40000的4A94E0路径在此前独立处理。此位为0不能证明地面碰撞成功。旧“无runtime xref/预留”说明错误；原服逐机体取值未知。",
    },
    42: {
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "关联配置表行 ID（col42→+392；sub_7D97E0/sub_7D8520 机库升级 UI 遍历；sub_78B690 模型链）",
    },
    46: {
        "name": "shop_recycle_gp",
        "db_column": "shop_recycle_gp",
        "display_name": "商店回收GP",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "商店回收 GP 基值（col46→+400；sub_887550 CShopRecycl_ItemIcon；MSMA_RENTAL 同偏移=rental_cost_gp/sub_582EC0）",
    },
    47: {
        "name": "hangar_timer_sec",
        "db_column": "hangar_timer_sec",
        "display_name": "机库计时秒",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "机库/租借计时秒（col47→+404；sub_7DA460/sub_7D97E0；MSMA_RENTAL=rental_duration_sec/sub_582EC0）",
    },
    50: {
        "name": "oc_exp_cp_id",
        "db_column": "oc_exp_cp_id",
        "display_name": "OC经验CP ID",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "OC/经验 CP 选择 ID（col50→+420；sub_847D10 OC 待機選択；sub_81EC60 getter）",
    },
    51: {
        "name": "hangar_list_ui_param",
        "db_column": "hangar_list_ui_param",
        "display_name": "机库列表UI参数",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "机库列表 UI 分支参数（col51→+424；sub_7E25A0/sub_97F077/sub_6B8D90）",
    },
    54: {
        "name": "hangar_ui_slot_a",
        "db_column": "hangar_ui_slot_a",
        "display_name": "机库UI槽A",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "机库 UI 控件槽 A（col54→+428；sub_897480/sub_7E94C0）",
    },
    55: {
        "name": "hangar_ui_slot_b",
        "db_column": "hangar_ui_slot_b",
        "display_name": "机库UI槽B",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "机库 UI 控件槽 B（col55→+432；sub_897480/sub_7E94C0）",
    },
    88: {
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "机库/商店列表分类 ID（col88→+32；sub_887550 回收价=list_category×GP 系数）",
    },
}

CAP_FLAG_BIT_MAP = """
| 内存偏移 | bit | CSV col | db_column | 能力名 | consumer | status |
|---|---:|---:|---|---|---|---|
| +840 | 0 | 13 | cap_flag_transform_alt | 变换备用武装 | sub_49D280 | confirmed |
| +840 | 1 | 15 | cap_flag_melee_chain | 近战连锁 | sub_4A7B10 | confirmed |
| +840 | 2 | 16 | cap_flag_reserved_b840_2 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 3 | 17 | cap_flag_reserved_b840_3 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 4 | 18 | cap_flag_mission_transform | 任务变形态 | sub_477C10, sub_67FEB0 | confirmed |
| +840 | 5 | 19 | cap_flag_reserved_b840_5 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 6 | 20 | cap_flag_reserved_b840_6 | 物理积分旁路 | 582390→47D230→4AE900 | confirmed |
| +840 | 7 | 21 | cap_flag_reserved_b840_7 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 0 | 22 | cap_flag_reserved_b841_0 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 1 | 31 | cap_flag_dual_slot_ui | 双槽切换UI | sub_7E7600, sub_7E4A50 | confirmed |
| +841 | 2 | 24 | cap_flag_skip_ex_anim | 跳过EX演出 | sub_7E7600 | confirmed |
| +841 | 3 | 25 | cap_flag_shield_equip | 盾牌装备 | sub_474480, sub_48FF00 | confirmed |
| +841 | 4 | 26 | cap_flag_reserved_b841_4 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 5 | 27 | cap_flag_reserved_b841_5 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 6 | 28 | cap_flag_tender_mode | 工作舰模式 | sub_478DA0, sub_507810 | confirmed |
| +841 | 7 | 29 | cap_flag_reserved_b841_7 | 位置碰撞更新旁路 | 582390→478DD0→4AE900 | confirmed |
| +842 | 0 | 30 | cap_flag_disable_special | 禁止特殊行动 | sub_4E7FF0, sub_4EF710 | confirmed |
| +842 | 1 | 32 | cap_flag_dual_mode | 双模式标志 | sub_6218F0 | confirmed |
| +842 | 2 | 33(gap) | — | （强制清零） | sub_582390 epilogue | gap |
| +842 | 3 | 34 | cap_flag_no_awakening | 禁止觉醒爆发 | sub_4EC960 | confirmed |
| +842 | 4–7 | — | — | （未知） | — | — |
"""

CP_FLAGS_BATCH: dict[int, tuple[str, str, str, str]] = {
    13: ("cap_flag_transform_alt", "变换备用武装", "能力位 +840 bit0：变身形态备用武装（sub_49D280）", "confirmed"),
    15: ("cap_flag_melee_chain", "近战连锁", "能力位 +840 bit1：近战连锁攻击门控（sub_4A7B10）", "confirmed"),
    16: ("cap_flag_reserved_b840_2", "能力位 b840.2（预留）", "能力位 +840 bit2（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    17: ("cap_flag_reserved_b840_3", "能力位 b840.3（预留）", "能力位 +840 bit3（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    18: ("cap_flag_mission_transform", "任务变形态", "能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0）", "confirmed"),
    19: ("cap_flag_reserved_b840_5", "能力位 b840.5（预留）", "能力位 +840 bit5（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    20: ("cap_flag_reserved_b840_6", "物理积分旁路位 +840 bit6", "582390 CSV20非零规范为CHARA_PARAM+840 bit6；47D230末尾读取此位，4AE900在返回true时跳过53D580物理积分。47D230还包含装备/特殊状态分支，因此此位为0不能证明实际物理更新已开启。旧“无runtime xref/预留”说明错误；其他消费者与原服逐机体取值未穷举。", "confirmed"),
    21: ("cap_flag_reserved_b840_7", "能力位 b840.7（预留）", "能力位 +840 bit7（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    22: ("cap_flag_reserved_b841_0", "能力位 b841.0（预留）", "能力位 +841 bit0（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    31: ("cap_flag_dual_slot_ui", "双槽切换UI", "能力位 +841 bit1：机体选择 UI 双槽切换（sub_7E7600；sub_7E4A50）", "confirmed"),
    24: ("cap_flag_skip_ex_anim", "跳过EX演出", "能力位 +841 bit2：清 0 时跳过 EX 武器演出（sub_7E7600）", "confirmed"),
    25: ("cap_flag_shield_equip", "盾牌装备", "能力位 +841 bit3：盾牌装备能力（sub_474480；sub_48FF00）", "confirmed"),
    26: ("cap_flag_reserved_b841_4", "能力位 b841.4（预留）", "能力位 +841 bit4（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    27: ("cap_flag_reserved_b841_5", "能力位 b841.5（预留）", "能力位 +841 bit5（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    28: ("cap_flag_tender_mode", "工作舰模式", "能力位 +841 bit6：工作舰/母舰 deploy（sub_478DA0；sub_507810）", "confirmed"),
    29: ("cap_flag_reserved_b841_7", "位置碰撞更新旁路位 +841 bit7", "582390 CSV29非零规范为CHARA_PARAM+841 bit7；478DD0读取该位，4AE900在返回true时跳过普通位置/碰撞更新分支（4ADD60或载体引用分支），角色+12 bit0x40000的4A94E0路径在此前独立处理。此位为0不能证明地面碰撞成功。旧“无runtime xref/预留”说明错误；原服逐机体取值未知。", "confirmed"),
    30: ("cap_flag_disable_special", "禁止特殊行动", "能力位 +842 bit0：禁止 deployable 特殊行动（sub_4E7FF0；sub_4EF710）", "confirmed"),
    32: ("cap_flag_dual_mode", "双模式标志", "能力位 +842 bit1：双模式/双形态标志（sub_6218F0→runtime+107）", "confirmed"),
    34: ("cap_flag_no_awakening", "禁止觉醒爆发", "能力位 +842 bit3：禁止觉醒/爆发（sub_4EC960）", "confirmed"),
}


def recount(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_defined"] = len(cols)
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_pending"] = sum(1 for c in cols if c.get("status") == "pending")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_count"] = sum(1 for c in cols if c.get("read_order") is not None)


def sync_md(md_path: Path, data: dict) -> None:
    if not md_path.is_file():
        return
    col_by_csv = {c["csv_index"]: c for c in data.get("columns", [])}
    out: list[str] = []
    in_table = False
    inserted_r7 = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 1.1 Round 6") and not inserted_r7:
            out.append("")
            out.append("## 1.2 Round 7 IDA 深搜（2026-09-21）")
            out.append("")
            out.append("> F6 ?? 48/49/4A 全二进制扫描：+840 仅 bit0/1/4 有 consumer；+841 仅 bit1/2/3/6；+842 bit0/2/3。")
            out.append("> 无 consumer 的 CSV 位 → `cap_flag_reserved_*`（confirmed ○ASM）；+392/+400 区段 → 机库/商店 UI consumer。")
            out.append(CAP_FLAG_BIT_MAP.strip())
            out.append("")
            out.append("**confirmed 47→64**（+17）；partial 17→0；gap 28 不变。")
            out.append("")
            inserted_r7 = True
        if line.startswith("| 读序 |"):
            in_table = True
        if in_table and line.startswith("|") and "`" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                m = re.search(r"`(\d+)`", parts[2])
                if m:
                    col = col_by_csv.get(int(m.group(1)))
                    if col:
                        disp = col.get("display_name") or col.get("name", "")
                        meaning = col.get("meaning", disp)
                        if col.get("status") == "confirmed":
                            cell = f"★**{disp}** — {meaning[:160]}"
                        elif col.get("status") == "gap":
                            cell = f"⛔**{disp}** — {meaning[:120]}"
                        else:
                            cell = f"{disp} — {meaning[:120]}"
                        parts[4] = cell
                        line = "| " + " | ".join(parts[1:4] + [parts[4]]) + " |"
        out.append(line)
    md_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def patch_batch_cp_flags() -> None:
    if not BATCH_PATH.is_file():
        return
    text = BATCH_PATH.read_text(encoding="utf-8")
    start = text.find("CP_FLAGS = {")
    end = text.find("\nCP_STRINGS", start)
    if start < 0 or end < 0:
        return
    lines = ["CP_FLAGS = {"]
    for idx in sorted(CP_FLAGS_BATCH.keys()):
        name, disp, meaning, status = CP_FLAGS_BATCH[idx]
        lines.append(f'    {idx}: ("{name}", "{disp}", "{meaning}", "{status}"),')
    lines.append("}")
    text = text[:start] + "\n".join(lines) + text[end:]
    BATCH_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    before_partial = sum(1 for c in data["columns"] if c.get("status") == "partial")
    before_conf = sum(1 for c in data["columns"] if c.get("status") == "confirmed")

    for col in data["columns"]:
        idx = col["csv_index"]
        if idx in UPDATES_BY_CSV:
            col.update(deepcopy(UPDATES_BY_CSV[idx]))

    recount(data)
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync_md(MD_PATH, data)
    patch_batch_cp_flags()

    print(f"CHARA_PARAM confirmed: {before_conf} -> {data['column_confirmed']}")
    print(f"CHARA_PARAM partial:   {before_partial} -> {data['column_partial']}")


if __name__ == "__main__":
    main()

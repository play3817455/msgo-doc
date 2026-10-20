#!/usr/bin/env python3
"""Round 6 CHARA_MODEL cfg enrichment (IDA consumers for partial cols)."""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "db_design" / "schema" / "cfg" / "tables" / "CHARA_MODEL.json"
MD_PATH = ROOT / "datatables" / "01-列注释" / "05-5-CHARA_MODEL.md"

# csv_index -> field updates (status confirmed + enriched meaning)
UPDATES_BY_CSV: dict[int, dict] = {
    11: {'status': 'confirmed', 'display_name': '物理积分质量 col11', 'meaning': '物理积分质量输入（571380 CSV11→CHARA_MODEL+48；4A5470/498950送入53D340，写CMassPoint+56并构造质量×重力；53D580在质量为0时直接返回，跳过速度和位移积分）。旧相机FOV名称无此消费链依据；保留旧DB列camera_fov仅为字段寻址兼容。原始逐模型质量值及单位未知，不能按FOV、wiki载重量或武器重量填值；当前579条发布记录均空/0。隔离原始指令验证只证明零质量门，不等于现场落地或完整物理恢复。'},
    6: {
        "status": "confirmed",
        "meaning": "机库网格 X 轴镜像（col6→+20；sub_428A40→sub_439930 模型装载）",
    },
    12: {
        "status": "confirmed",
        "meaning": "机库隐藏盾牌网格（col12→+34；sub_44FEE0→sub_AFEFE0 加载门控）",
    },
    13: {
        "status": "confirmed",
        "meaning": "机库隐藏武器网格（col13→+35；sub_559D30/CMsmaMeshCustomizeTable）",
    },
    14: {
        "status": "partial",
        "display_name": "角色可视性条件 col14",
        "meaning": "col14→+54（0x36）bool（571380）；477300 在角色+1168 bit1为0，或角色+216非空且本标记为0时返回false；4C7B00对自身角色的该分支不清除隐藏原因2。字段原名、完整用途与各机体原始取值未知；不能称为隐藏背包。2026-10-07只对已核实模型101010101/184302101开启此布尔条件，恢复自身相机隐藏原因2的正常清除路径；这是按目标客户端行为实现的功能兼容策略，不是找回原服取值，不强制清除其他隐藏原因。",
    },
    26: {
        "name": "mesh_custom_26",
        "db_column": "mesh_custom_26",
        "display_name": "网格定制26",
        "type": "u32",
        "status": "confirmed",
        "meaning": "网格定制 mesh ID（col26→mesh 块 u32 +5C；sub_571380 2×8 循环；sub_439930 装载）",
        "enum_converter": None,
    },
    27: {
        "name": "mesh_custom_27",
        "db_column": "mesh_custom_27",
        "display_name": "网格定制27",
        "type": "u32",
        "status": "confirmed",
        "meaning": "网格定制 mesh ID（col27→mesh 块 u32 +60；sub_571380 2×8 循环；sub_439930 装载）",
        "enum_converter": None,
    },
    28: {
        "name": "mesh_custom_28",
        "db_column": "mesh_custom_28",
        "display_name": "网格定制28",
        "type": "u32",
        "status": "confirmed",
        "meaning": "网格定制 mesh ID（col28→mesh 块 u32 +64；sub_571380 2×8 循环；sub_439930 装载）",
        "enum_converter": None,
    },
    30: {
        "name": "mesh_custom_30",
        "db_column": "mesh_custom_30",
        "display_name": "网格定制30",
        "type": "u32",
        "status": "confirmed",
        "meaning": "网格定制 mesh ID（col30→mesh 块 u32 +6C；sub_571380 2×8 循环；sub_439930 装载）",
        "enum_converter": None,
    },
    38: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col38→+F4；sub_439930 模型参数块）",
    },
    39: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col39→+F8；sub_439930 模型参数块）",
    },
    40: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col40→+FC；sub_439930 模型参数块）",
    },
    43: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col43→+108；sub_439930 模型参数块）",
    },
    45: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col45→+110；sub_439930 模型参数块）",
    },
    47: {
        "status": "confirmed",
        "meaning": "特效路径 A 启用（col47→+118；门控 col50 effect_path_a 加载）",
    },
    48: {
        "status": "confirmed",
        "meaning": "特效路径 B 启用（col48→+119；门控 col51 effect_path_b 加载）",
    },
    49: {
        "status": "confirmed",
        "meaning": "特效路径 C 启用（col49→+11A；门控 col52 effect_path_c 加载）",
    },
    62: {
        "status": "confirmed",
        "meaning": "阴影渲染开关（col62→+194；sub_489820 阴影可见性门控）",
    },
    63: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col63→+198；sub_439930 模型参数块）",
    },
    66: {
        "status": "confirmed",
        "meaning": "模型变体 A（col66→+1A8；>0 启用；sub_439930 变体选择）",
    },
    67: {
        "status": "confirmed",
        "meaning": "模型变体 B（col67→+1A9；>0 启用；sub_439930 变体选择）",
    },
    69: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col69→+1AC；sub_439930 模型参数块）",
    },
    70: {
        "status": "confirmed",
        "meaning": "强制加载模型资源（col70→+1B0；sub_439930 跳过节流）",
    },
    73: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col73→+1BC；sub_439930 尾部参数块）",
    },
    74: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col74→+1C0；sub_439930 尾部参数块）",
    },
    75: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col75→+1C8；sub_439930 尾部参数块）",
    },
    76: {
        "status": "confirmed",
        "meaning": "材质/渲染 u32（col76→+1C4；sub_439930 尾部参数块）",
    },
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
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|") and "`" in line:
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
                        else:
                            cell = f"{disp} — {meaning[:120]}"
                        parts[4] = cell
                        line = "| " + " | ".join(parts[1:4] + [parts[4]]) + " |"
        out.append(line)
    md_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    before_conf = sum(1 for c in data["columns"] if c.get("status") == "confirmed")
    before_partial = sum(1 for c in data["columns"] if c.get("status") == "partial")

    for col in data["columns"]:
        idx = col["csv_index"]
        if idx in UPDATES_BY_CSV:
            patch = deepcopy(UPDATES_BY_CSV[idx])
            if patch.get("enum_converter") is None and "enum_converter" in patch:
                col.pop("enum_converter", None)
                patch.pop("enum_converter")
            col.update({k: v for k, v in patch.items() if v is not None})
    recount(data)
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync_md(MD_PATH, data)

    print(f"confirmed: {before_conf} -> {data['column_confirmed']}")
    print(f"partial:   {before_partial} -> {data['column_partial']}")
    print(f"gap:       {data['column_gap']}")


if __name__ == "__main__":
    main()

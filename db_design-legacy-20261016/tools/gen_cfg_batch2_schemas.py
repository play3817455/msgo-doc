#!/usr/bin/env python3
"""Generate ASM-verified cfg/tables JSON for batch 2 (weapons + items)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD_DIR = ROOT / "datatables" / "01-列注释"
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
META = ROOT / "db_design" / "schema" / "_meta"
DECOMP = META / "ida_cfg_batch2_decompile.json"
ASM_MERGED = META / "ida_cfg_batch2_asm_merged.json"
MANIFEST = ROOT / "db_design" / "schema" / "cfg" / "_asm_manifest.json"

READERS = {
    "WEAPON_SETTING": "sub_597F50",
    "WEAPON_BATTLE_DETAIL": "sub_A47BC0",
    "BULLET": "sub_5709F0",
    "WRESTLE_PARAM": "sub_56F5F0",
    "BUILDUP_WEAPON": "sub_570880",
    "DAMAGE_FIELD_PARAM": "sub_575D00",
    "ITEM": "sub_593B70",
    "ITEM_PART": "sub_5955A0",
    "ITEM_USE": "sub_5959B0",
    "ITEM_TOKEN": "sub_595960",
    "ITEMPACK_INFO": "sub_5933C0",
}

# csv_index -> semantic name overrides (confirmed/partial from MD + decompile)
NAME_MAP: dict[str, dict[int, str]] = {
    "WEAPON_SETTING": {
        0: "weapon_setting_id",
        1: "unknown_u32_1",
        2: "model_id_lo",
        3: "model_id_hi",
        4: "variant_id_lo",
        5: "variant_id_hi",
        7: "unknown_u32_7",
        8: "unknown_u32_8",
        9: "inherit_parent_flag",
        10: "enabled_flag",
        11: "unknown_u32_11",
        12: "unknown_u32_12",
        13: "equip_slot_type",
        14: "magazine_size",
        15: "melee_shield_subtype",
        16: "weapon_shot_subtype",
        17: "lock_on_flag",
        18: "close_range_flag",
        19: "use_parent_close_flag",
        20: "use_parent_lock_flag",
        21: "weapon_category",
        22: "weapon_category_derived",
        23: "damage_type",
        24: "burst_param_1",
        25: "burst_param_2",
        26: "burst_param_3",
        27: "burst_param_4",
        28: "burst_param_5",
        29: "burst_param_6",
        30: "unknown_enum_30",
        31: "fire_type",
        32: "unknown_enum_32",
        33: "damage_attribute",
        34: "flag_bit_33",
        35: "flag_bit_34",
        36: "power_multiplier",
        38: "range_multiplier",
        40: "accuracy_multiplier",
        41: "optional_name_flag",
        43: "recoil_multiplier",
        45: "reload_multiplier",
        47: "cooldown_multiplier",
        49: "switch_time_multiplier",
        51: "lockon_multiplier",
        53: "stability_multiplier",
        55: "rapid_delay_multiplier",
        56: "optional_effect_flag",
        57: "optional_sound_flag",
        59: "spread_multiplier",
        64: "ammo_type_id",
        65: "ammo_count",
        66: "ammo_reserve",
        67: "unknown_u32_67",
        68: "unknown_u32_68",
        69: "unknown_u32_69",
        70: "unknown_u32_70",
        71: "unknown_u32_71",
        72: "unknown_u32_72",
        73: "unknown_u32_73",
        74: "effect_name_list",
        77: "hit_effect_list",
        79: "muzzle_effect_list",
        81: "trail_effect_list",
        87: "sound_set_list",
        89: "voice_set_list",
        91: "camera_shake_list",
        93: "screen_flash_list",
        95: "buff_effect_list",
        98: "debuff_effect_list",
        100: "spawn_effect_list",
        103: "float_param_103",
        104: "reload_type",
        105: "reload_param",
        106: "unknown_u32_106",
        107: "unknown_u32_107",
        108: "float_param_108",
        109: "float_param_109",
        110: "unknown_u32_110",
        111: "float_param_111",
        112: "max_lock_count",
        113: "lock_range",
        114: "unknown_u32_114",
        115: "unknown_u32_115",
        116: "unknown_u32_116",
        117: "unknown_u32_117",
        118: "float_param_118",
        119: "float_param_119",
        120: "float_param_120",
        121: "float_param_121",
        122: "float_param_122",
        123: "flag_bit_123",
        124: "flag_bit_124",
        125: "aim_mode",
        126: "float_param_126",
        127: "float_param_127",
        128: "special_effect",
        129: "float_param_129",
        131: "unknown_u32_131",
        132: "display_mode",
        133: "unknown_u32_133",
        134: "unknown_u32_134",
        135: "unknown_u32_135",
        136: "tag_list",
        137: "melee_shield_subtype_alt",
        138: "unknown_list_138",
        139: "unknown_u32_139",
        140: "unknown_u32_140",
        141: "unknown_u32_141",
        145: "unknown_u32_145",
        146: "special_effect_alt",
        147: "unknown_u32_147",
    },
    "BULLET": {0: "bullet_id"},
    "WRESTLE_PARAM": {0: "wrestle_param_id"},
    "DAMAGE_FIELD_PARAM": {0: "damage_field_id"},
    "ITEM": {
        0: "item_id",
        1: "sort_group",
        2: "name",
        3: "description",
        4: "item_type",
        5: "stack_limit",
        6: "linked_table_id",
        7: "icon_variant",
    },
    "ITEM_USE": {0: "use_item_id", 2: "linked_item_id", 3: "enabled_flag"},
    "ITEM_TOKEN": {0: "token_item_id", 2: "token_type", 3: "unknown_u32_3", 4: "unknown_u32_4"},
    "ITEMPACK_INFO": {
        0: "itempack_id",
        1: "pack_item_id",
        2: "quantity",
        3: "unknown_u32_3",
    },
    "WEAPON_BATTLE_DETAIL": {
        0: "attr_name",
        1: "weapon_id_key",
        2: "attr_value",
    },
}

CONFIRMED: dict[str, set[int]] = {
    "ITEM": {0, 2, 3, 4},
    "ITEM_USE": {0, 2, 3},
    "ITEMPACK_INFO": {0, 1, 2, 3},
    "WEAPON_BATTLE_DETAIL": {0, 1, 2},
}

# Hand-verified from IDA disasm/decompile (batch 2)
MANUAL_ASM: dict[str, dict[int, dict]] = {
    "ITEM": {
        0: {"asm_va": "0x593b9e", "memory_offset": 0, "type": "u32"},
        1: {"asm_va": "0x593bac", "memory_offset": 4, "type": "u32"},
        2: {"asm_va": "0x593bc0", "memory_offset": 8, "type": "str"},
        3: {"asm_va": "0x593bfa", "memory_offset": 36, "type": "str"},
        4: {"asm_va": "0x593c59", "memory_offset": 64, "type": "enum"},
        5: {"asm_va": "0x593c74", "memory_offset": 74, "type": "u16"},
        6: {"asm_va": "0x593c80", "memory_offset": 68, "type": "u32"},
        7: {"asm_va": "0x593c8b", "memory_offset": 72, "type": "u16"},
    },
    "ITEM_USE": {
        0: {"asm_va": "0x5959b9", "memory_offset": 0, "type": "u32"},
        2: {"asm_va": "0x5959eb", "memory_offset": 32, "type": "u32"},
        3: {"asm_va": "0x5959fc", "memory_offset": 36, "type": "u32"},
    },
    "ITEM_TOKEN": {
        0: {"asm_va": "0x595975", "memory_offset": 0, "type": "u32"},
        2: {"asm_va": "0x595991", "memory_offset": 4, "type": "enum"},
        3: {"asm_va": "0x59599c", "memory_offset": 8, "type": "u32"},
        4: {"asm_va": "0x5959a7", "memory_offset": 12, "type": "u32"},
    },
    "ITEMPACK_INFO": {
        0: {"asm_va": "0x5933d5", "memory_offset": 0, "type": "u32"},
        1: {"asm_va": "0x5933df", "memory_offset": 4, "type": "u32"},
        2: {"asm_va": "0x5933ea", "memory_offset": 8, "type": "u32"},
        3: {"asm_va": "0x5933f5", "memory_offset": 12, "type": "u32"},
    },
    "WEAPON_BATTLE_DETAIL": {
        0: {"asm_va": "0xa47cb1", "memory_offset": None, "type": "str_enum"},
        1: {"asm_va": "0xa47c0e", "memory_offset": None, "type": "str"},
        2: {"asm_va": "0xa47ccf", "memory_offset": None, "type": "u32"},
    },
    "WEAPON_SETTING": {
        0: {"asm_va": "0x597f81", "memory_offset": 0, "type": "u32"},
        13: {"asm_va": "0x59807b", "memory_offset": 56, "type": "enum"},
        15: {"asm_va": "0x5980a6", "memory_offset": 68, "type": "enum"},
        16: {"asm_va": "0x5980c0", "memory_offset": 72, "type": "enum"},
        21: {"asm_va": "0x59817a", "memory_offset": 84, "type": "enum"},
        29: {"asm_va": "0x598330", "memory_offset": 92, "type": "enum"},
        30: {"asm_va": "0x598375", "memory_offset": 96, "type": "enum"},
        31: {"asm_va": "0x59838d", "memory_offset": 100, "type": "enum"},
        32: {"asm_va": "0x5983c8", "memory_offset": 108, "type": "enum"},
        128: {"asm_va": "0x5990ce", "memory_offset": 2124, "type": "enum"},
        137: {"asm_va": "0x59925b", "memory_offset": 2224, "type": "enum"},
        146: {"asm_va": "0x599304", "memory_offset": 2132, "type": "enum"},
    },
}

MANUAL_MD_ROWS: dict[str, list[dict]] = {
    "WEAPON_BATTLE_DETAIL": [
        {"read_order": 0, "csv_index": 0, "type": "str_enum", "meaning": "★属性名★（sub_595CC0 词表分派 11 张子表）"},
        {"read_order": 1, "csv_index": 1, "type": "str", "meaning": "★键★（武器ID 字符串）"},
        {"read_order": 2, "csv_index": 2, "type": "u32", "meaning": "★值★（子表 vtable 读 col2，int 或 float）"},
    ],
}

PARTIAL_ENUM = re.compile(r"enum|★|sub_")
ID_RE = re.compile(r"主键|索引ID|物品ID|武器组ID")
WS_ENUM_COLS = {13, 15, 16, 19, 21, 27, 28, 29, 30, 31, 32, 92, 100, 106, 128, 137, 146}

COL_CALL = re.compile(
    r"sub_(BBB370|BBB470|BBB3F0|BBB4F0|456D90|5976F0|BBB920)\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)\s*;\s*/\*(0x[0-9a-fA-F]+)\*/"
)
ENUM_PAIR = re.compile(
    r"sub_BBB4F0\([^,]+,\s*(0x[0-9a-fA-F]+|\d+)u?\)[^;]*;/\*(0x[0-9a-fA-F]+)\*/[^;]*sub_(5968A0|596990|596A80|596B70|596510|596C60|5965F0|5964A0|596D50|596E40|570950|56F4B0|56F3A0|575A60|5954A0|5951D0|5952C0|5953B0|593770|595870|402310)\("
)
MEM_RE = re.compile(
    r"\*\(_(?:DWORD|BYTE|WORD|QWORD|float)\s*\*\)\((?:v7|a3|\*a3|\*a4|a4|esi|\w+)\s*\+\s*(0x[0-9a-fA-F]+|\d+)\)"
)
VAR_ASSIGN = re.compile(r"\b(v\d+|a2)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*;/\*(0x[0-9a-fA-F]+)\*/")
VAR_CALL = re.compile(
    r"sub_BBB370\([^,]+,\s*(v\d+|a2|v128|v127|v126|v125|v124|v130|v129)\)[^;]*;/\*(0x[0-9a-fA-F]+)\*/"
)


def parse_md_columns(md_path: Path) -> list[dict]:
    text = md_path.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "`" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5 or parts[1] in ("读序", "---"):
            continue
        try:
            read_order = int(parts[1])
            csv_index = int(parts[2].strip("`"))
            col_type = parts[3].lower()
            meaning = parts[4]
        except ValueError:
            continue
        rows.append(
            {
                "read_order": read_order,
                "csv_index": csv_index,
                "type": col_type,
                "meaning": meaning,
            }
        )
    return rows


def parse_decompile(code: str) -> dict[int, dict]:
    """Return csv_index -> {asm_va, memory_offset, type}."""
    code = code.replace("\n", " ")
    var_val: dict[str, int] = {}
    out: dict[int, dict] = {}

    for m in VAR_ASSIGN.finditer(code):
        var_val[m.group(1)] = int(m.group(2), 0)

    chunks = code.split(";")
    for i, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue

        va_m = re.search(r"/\*(0x[0-9a-fA-F]+)\*/\s*$", chunk)
        va = va_m.group(1) if va_m else None

        col = None
        kind = None

        m = COL_CALL.search(chunk + ";")
        if m:
            fn, col_s, va2 = m.group(1), m.group(2), m.group(3)
            col = int(col_s, 0)
            va = va or va2
            kind = {
                "BBB370": "u32",
                "BBB470": "float",
                "BBB3F0": "i64",
                "BBB4F0": "str_enum",
                "456D90": "str",
                "5976F0": "str_cond",
                "BBB920": "str_opt",
            }[fn]
        else:
            em = ENUM_PAIR.search(chunk + ";" + (chunks[i + 1] if i + 1 < len(chunks) else ""))
            if em:
                col = int(em.group(1), 0)
                va = va or em.group(2)
                kind = "enum"
            else:
                vm = VAR_CALL.search(chunk + ";")
                if vm:
                    vname, va3 = vm.group(1), vm.group(2)
                    if vname in var_val:
                        col = var_val[vname]
                        va = va or va3
                        kind = "u32"

        if col is None:
            continue

        mem = None
        search = ";".join(chunks[i : i + 5])
        for mm in MEM_RE.finditer(search):
            off = int(mm.group(1), 0)
            if off < 0x800:  # skip bitfield pseudo offsets
                mem = off
                break

        prev = out.get(col, {})
        out[col] = {
            "type": kind or prev.get("type", "u32"),
            "asm_va": va or prev.get("asm_va"),
            "memory_offset": mem if mem is not None else prev.get("memory_offset"),
        }

    return out


def buildup_columns() -> dict[int, dict]:
    """Manual from sub_570880 loop: cols 1-10 bool, 11-20 u32."""
    cols = {0: {"type": "u32", "asm_va": "0x570895", "memory_offset": 0}}
    for n in range(1, 11):
        cols[n] = {"type": "u32", "asm_va": "0x5708d6", "memory_offset": n}
        cols[n + 10] = {"type": "u32", "asm_va": "0x5708eb", "memory_offset": 4 + n * 4}
    return cols


def weapon_battle_detail_columns() -> dict[int, dict]:
    return {
        0: {"type": "str_enum", "asm_va": "0xa47cb1", "memory_offset": None},
        1: {"type": "str", "asm_va": "0xa47c0e", "memory_offset": None},
        2: {"type": "u32", "asm_va": "0xa47ccf", "memory_offset": None},
    }


def status_for(table: str, col: dict, md_row: dict, asm: dict | None) -> tuple[str, str]:
    csv_i = md_row["csv_index"]
    if csv_i in CONFIRMED.get(table, set()):
        return "confirmed", "★确证"
    name = NAME_MAP.get(table, {}).get(csv_i, "")
    if table == "WEAPON_SETTING" and csv_i in WS_ENUM_COLS and asm and asm.get("asm_va"):
        return "partial", "○枚举ASM"
    if asm and asm.get("asm_va"):
        if name and not name.startswith("unknown") and not name.startswith("pending"):
            if md_row["type"] == "enum" or "enum" in (asm.get("type") or ""):
                return "partial", "○枚举确证"
            return "confirmed", "★确证"
        return "partial", "○ASM确证"
    if table == "ITEM" and csv_i in (6, 7) and asm and asm.get("memory_offset") is not None:
        return "partial", "○ASM+xref"
    if PARTIAL_ENUM.search(md_row["meaning"]) or md_row["type"] == "enum":
        return "partial", "○文档"
    if ID_RE.search(md_row["meaning"]):
        return "partial", "○主键"
    return "pending", "△"


def build_table(
    table_id: str, manifest_entry: dict, decomp_entry: dict, asm_merged: dict[int, dict]
) -> dict:
    md_path = ROOT / manifest_entry["source_md"]
    existing_path = TABLES_DIR / f"{table_id}.json"
    base = json.loads(existing_path.read_text(encoding="utf-8")) if existing_path.exists() else {}

    md_rows = parse_md_columns(md_path) or MANUAL_MD_ROWS.get(table_id, [])
    if table_id == "BUILDUP_WEAPON":
        asm_map = buildup_columns()
    else:
        asm_map = parse_decompile(decomp_entry.get("decompile", ""))
    manual = MANUAL_ASM.get(table_id, {})
    for csv_i, info in asm_merged.items():
        asm_map[csv_i] = {**asm_map.get(csv_i, {}), **info}
    for csv_i, info in manual.items():
        asm_map[csv_i] = {**asm_map.get(csv_i, {}), **info}

    reader = READERS[table_id]
    columns = []
    for row in md_rows:
        csv_i = row["csv_index"]
        asm = asm_map.get(csv_i, {})
        names = NAME_MAP.get(table_id, {})
        name = names.get(csv_i)
        if not name:
            if row["type"] == "float":
                name = f"float_param_{csv_i}"
            elif row["type"] in ("str",):
                name = "name" if "名称" in row["meaning"] else f"str_{csv_i}"
            elif row["type"] == "enum":
                name = f"enum_{csv_i}"
            elif ID_RE.search(row["meaning"]):
                name = f"{table_id.lower()}_id" if csv_i == 0 else f"unknown_u32_{csv_i}"
            else:
                name = f"unknown_u32_{csv_i}"

        status, confidence = status_for(table_id, row, row, asm)
        col_type = asm.get("type") or row["type"]
        if col_type == "str_enum":
            col_type = "enum" if "enum" in row["meaning"].lower() or row["type"] == "enum" else "str"
        if col_type == "str_cond" or col_type == "str_opt":
            col_type = "str"

        db_col = name if status == "confirmed" else f"col{csv_i}"

        meaning = row["meaning"]
        if table_id == "ITEM" and csv_i == 1:
            meaning = "排序/分组 ID（内存 +4；sub_436280 未直接消费名称外字段）"
        elif table_id == "ITEM" and csv_i == 6:
            meaning = "关联表行 ID（+68；ITEM_USE/TOKEN 经 sub_5944D0 查目标物品）"
        elif table_id == "ITEM" and csv_i == 5:
            meaning = "堆叠上限（u16 @+74）"
        elif table_id == "ITEM" and csv_i == 7:
            meaning = "图标变体（u16 @+72）"

        columns.append(
            {
                "read_order": row["read_order"] + 1,
                "csv_index": csv_i,
                "name": name,
                "db_column": db_col,
                "type": col_type,
                "memory_offset": asm.get("memory_offset"),
                "asm_reader": reader,
                "asm_va": asm.get("asm_va"),
                "meaning": meaning,
                "display_name": meaning.split("（")[0].replace("★", "").strip()[:80],
                "status": status,
                "confidence": confidence,
            }
        )

    confirmed = sum(1 for c in columns if c["status"] == "confirmed")
    partial = sum(1 for c in columns if c["status"] == "partial")
    pending = sum(1 for c in columns if c["status"] == "pending")

    out = {
        **{k: v for k, v in base.items() if k not in ("columns", "column_confirmed", "column_partial", "column_pending", "column_defined", "asm_status", "asm_reader")},
        "asm_reader": reader,
        "columns": columns,
        "column_defined": len(columns),
        "column_confirmed": confirmed,
        "column_partial": partial,
        "column_pending": pending,
        "asm_status": "complete" if pending == 0 else ("partial" if confirmed + partial else "pending"),
    }
    return out


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    decomp_all = json.loads(DECOMP.read_text(encoding="utf-8"))
    merged_all = json.loads(ASM_MERGED.read_text(encoding="utf-8")) if ASM_MERGED.exists() else {}
    manifest_by_id = {t["id"]: t for t in manifest["tables"]}

    summaries = []
    for table_id in READERS:
        entry = manifest_by_id[table_id]
        asm_table = merged_all.get(table_id, {})
        # normalize int keys
        asm_table = {int(k): v for k, v in asm_table.items()}
        data = build_table(table_id, entry, decomp_all.get(table_id, {}), asm_table)
        out_path = TABLES_DIR / f"{table_id}.json"
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summaries.append(
            {
                "table": table_id,
                "columns": data["column_defined"],
                "confirmed": data["column_confirmed"],
                "partial": data["column_partial"],
                "pending": data["column_pending"],
                "asm_status": data["asm_status"],
            }
        )
        print(f"{table_id}: {data['column_confirmed']} confirmed, {data['column_partial']} partial, {data['column_pending']} pending")

    (META / "cfg_batch2_summary.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

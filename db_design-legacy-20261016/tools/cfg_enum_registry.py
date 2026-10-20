"""Build enum registry + Chinese labels for cfg HTML site."""

from __future__ import annotations

import json
import re
from pathlib import Path

from enum_translate import exact_zh, is_rough, translate

ROOT = Path(__file__).resolve().parents[2]
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUMS_IDA = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enums_ida.json"
GLOSSARY = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enum_glossary_zh.json"

TOKEN_ZH: dict[str, str] = {
    "NEAR": "近距",
    "MIDDLE": "中距",
    "FAR": "远距",
    "SHIELD": "护盾/盾战",
    "MAIN": "主武装",
    "EX": "EX武装",
    "SUB": "副武装",
    "SUB1": "副武装1",
    "UNKNOWN": "未知/不限",
    "ATTACK": "攻击",
    "DEFENSE": "防御",
    "MOVE": "移动",
    "SPECIAL": "特殊",
    "NORMAL": "普通",
    "COMMON": "通用",
    "NONE": "无",
    "SOLID": "实弹",
    "BEAM": "光束",
    "BLAST": "爆炸",
    "DEAD": "即死",
    "MACHINEGUN": "机枪",
    "SHOTGUN": "霰弹",
    "BAZOOKA": "火箭筒",
    "MISSILE": "导弹",
    "WRESTLE": "格斗",
    "SNIPE": "狙击",
    "REPAIR": "修理",
    "HOMING": "制导",
    "GP": "GP",
    "ITEM": "道具",
    "MSMA": "机体",
    "LOGIN": "登录",
    "XWAR": "大规模战",
    "BRONZE": "铜",
    "SILVER": "银",
    "GOLD": "金",
    "PLATINUM": "白金",
    "EFF": "地球联邦",
    "ZEON": "吉翁",
    "ONEHAND": "单手",
    "TWOHAND": "双手",
    "SHOLDER": "肩扛",
    "LAND": "陆地",
    "WATER": "水中",
    "SPACE": "宇宙",
    "GROUND": "地面",
    "ARMOR": "装甲",
    "ASSAULT": "突击",
    "SUPPORT": "支援",
    "CANNON": "炮击",
    "FREE": "免费",
    "PLAY": "游玩",
    "BUNDLE": "捆绑",
}

KIND_DEFAULT = "enum"


def conv_slug(converter: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", converter).lower()


def anchor_id(name: str) -> str:
    safe = re.sub(r"[^\w\-]", "_", str(name))
    return f"v-{safe}"


def load_glossary() -> dict:
    if GLOSSARY.is_file():
        return json.loads(GLOSSARY.read_text(encoding="utf-8"))
    return {"converters": {}, "global_values": {}}


def load_ida_enums() -> dict:
    if not ENUMS_IDA.is_file():
        return {}
    data = json.loads(ENUMS_IDA.read_text(encoding="utf-8"))
    return data.get("converters", {})


def values_from_enums_json(converter: str, enums: dict) -> list[dict]:
    r = enums.get(converter)
    if not r:
        return []
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": n, "value": v} for n, v in r["table"]]
    lits = r.get("lits") or []
    consts = r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    if lits:
        return [{"name": n, "value": i} for i, n in enumerate(lits)]
    return []


def guess_value_zh(name: str, global_vals: dict) -> str:
    if name in global_vals:
        return global_vals[name]
    if name in TOKEN_ZH:
        return TOKEN_ZH[name]
    parts = re.split(r"[_\-/]+", name)
    bits = []
    for p in parts:
        if not p:
            continue
        if p in TOKEN_ZH:
            bits.append(TOKEN_ZH[p])
        elif p.isdigit():
            bits.append(p)
        else:
            bits.append(p.replace(" ", ""))
    if bits:
        return "·".join(bits)
    return name


def short_zh(s: str, max_len: int = 48) -> str:
    s = re.sub(r"\*+", "", s or "").strip()
    s = re.split(r"[（(；;]", s)[0].strip()
    return s[:max_len] if len(s) > max_len else s


def apply_ida_meta(entry: dict, ida: dict) -> None:
    entry["kind"] = ida.get("kind", KIND_DEFAULT)
    if ida.get("asm_va"):
        entry["asm_va"] = ida["asm_va"]
    if ida.get("title_zh"):
        entry["title_zh"] = ida["title_zh"]
    if ida.get("desc_zh"):
        entry["desc_zh"] = ida["desc_zh"]
    if ida.get("ida_note"):
        entry["ida_note"] = ida["ida_note"]
    if ida.get("data_refs"):
        entry["data_refs"] = ida["data_refs"]
    for ev in ida.get("values") or []:
        nm = ev.get("name", "")
        if not nm:
            continue
        cur = entry["values"].setdefault(
            nm, {"name": nm, "value": ev.get("value"), "label_zh": ""}
        )
        if ev.get("value") is not None:
            cur["value"] = ev["value"]
        if ev.get("label_zh"):
            cur["label_zh"] = ev["label_zh"]


def build_registry(tables: list[dict]) -> dict[str, dict]:
    glossary = load_glossary()
    conv_gloss = glossary.get("converters", {})
    ida_enums = load_ida_enums()
    global_vals = {**TOKEN_ZH, **glossary.get("global_values", {})}
    enums: dict = {}
    if ENUMS_JSON.is_file():
        enums = json.loads(ENUMS_JSON.read_text(encoding="utf-8"))

    registry: dict[str, dict] = {}

    for tbl in tables:
        tid = tbl.get("id", "")
        csv_path = tbl.get("csv_path", "")
        for c in tbl.get("columns", []):
            conv = c.get("enum_converter")
            if not conv or conv == "?":
                continue
            entry = registry.setdefault(
                conv,
                {
                    "converter": conv,
                    "slug": conv_slug(conv),
                    "kind": KIND_DEFAULT,
                    "title_zh": "",
                    "desc_zh": "",
                    "values": {},
                    "usages": [],
                },
            )
            entry["usages"].append(
                {
                    "table": tid,
                    "csv_path": csv_path,
                    "column": c.get("name") or c.get("db_column"),
                    "display_name": c.get("display_name", ""),
                    "csv_index": c.get("csv_index"),
                }
            )
            if not entry["title_zh"]:
                cg = conv_gloss.get(conv, {})
                entry["title_zh"] = cg.get("title_zh") or short_zh(
                    c.get("display_name") or c.get("name", "")
                )
                entry["desc_zh"] = cg.get("desc_zh") or short_zh(
                    c.get("meaning", ""), 120
                )
            for ev in c.get("enum_values") or []:
                nm = ev.get("name", "")
                if not nm:
                    continue
                val = ev.get("value")
                if nm not in entry["values"]:
                    entry["values"][nm] = {"name": nm, "value": val, "label_zh": ""}

    for conv, entry in registry.items():
        cg = conv_gloss.get(conv, {})
        if cg.get("title_zh"):
            entry["title_zh"] = cg["title_zh"]
        if cg.get("desc_zh"):
            entry["desc_zh"] = cg["desc_zh"]
        cv = cg.get("values") or {}

        for ev in values_from_enums_json(conv, enums):
            nm = ev["name"]
            if nm not in entry["values"]:
                entry["values"][nm] = {
                    "name": nm,
                    "value": ev["value"],
                    "label_zh": "",
                }
            elif entry["values"][nm].get("value") is None:
                entry["values"][nm]["value"] = ev["value"]

        if conv in ida_enums:
            apply_ida_meta(entry, ida_enums[conv])

        for nm, meta in entry["values"].items():
            hit = exact_zh(nm)
            if hit:
                meta["label_zh"] = hit
            elif nm in cv:
                meta["label_zh"] = cv[nm]
            elif nm in global_vals and not is_rough(global_vals[nm], nm):
                meta["label_zh"] = global_vals[nm]
            elif not meta.get("label_zh") or is_rough(meta.get("label_zh", ""), nm):
                meta["label_zh"] = translate(nm)
            else:
                meta["label_zh"] = meta.get("label_zh") or guess_value_zh(nm, global_vals)

    for conv, ida in ida_enums.items():
        if conv not in registry:
            registry[conv] = {
                "converter": conv,
                "slug": conv_slug(conv),
                "kind": ida.get("kind", KIND_DEFAULT),
                "title_zh": ida.get("title_zh", conv),
                "desc_zh": ida.get("desc_zh", ""),
                "values": {},
                "usages": [],
            }
            apply_ida_meta(registry[conv], ida)

    for entry in registry.values():
        vals = list(entry["values"].values())

        def sort_key(v: dict):
            val = v.get("value")
            try:
                n = int(val)
            except (TypeError, ValueError):
                n = 999999999
            return (n, v.get("name", ""))

        entry["values_list"] = sorted(vals, key=sort_key)

    return dict(sorted(registry.items(), key=lambda x: x[0].lower()))

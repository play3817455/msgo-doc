#!/usr/bin/env python3
"""Full-scale generate composites, tables, entities from protocol_analysis."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTO = ROOT / "protocol_analysis" / "commands"
SCHEMA = Path(__file__).resolve().parents[1] / "schema"
MANIFEST = SCHEMA / "_meta" / "struct_manifest.json"

TRANSIENT_NAMES = {"result", "opcode", "result_detail"}
EVENT_STRUCTS = {
    "ms", "snapshot", "snapshot_arr", "funnelss", "appear_info", "AI",
    "progress", "wave_res", "buffitem", "fire_points", "check_quest",
}
PERSIST_HINTS = ("_store", "_create", "_edit", "_update", "_set", "_del", "pilot_create", "_get_r", "_add")
MANUAL_TABLES = {"tbl_pilot", "tbl_ms_set", "tbl_equip_set", "tbl_item"}

# 协议里出现但**不该各自建表**的结构（不臆造表，只在这里显式登记）。
#  - sort_info_invite：CS-0x49D1 的排序入参（来源 arg_4），响应从 vt[0x480]
#    原样回显 ⇒ 请求作用域的排序准则，不是玩家存档。
NO_TABLE_STRUCTS = {"sort_info_invite"}

# 同一实体的多个**线形**：键 = 轻量线形，值 = 承载持久化的主结构。
#  - ms_lounge(303B) 是 ms_rokaku(401B) 的前 303B（缺 weapons[3]/limit_*）。
#    各建一张表 = 同一台机体两份存储、两处写入，必然漂移；合成一张 tbl_ms_rokaku，
#    线形差异由命令层按需填充（见 db_design/schema/tables/tbl_ms_rokaku.json）。
STRUCT_ALIASES = {"ms_lounge": "ms_rokaku"}


def is_complete_json(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("status") == "complete"
    except (json.JSONDecodeError, OSError):
        return False


def load_manifest_members() -> dict[str, list[dict]]:
    if not MANIFEST.is_file():
        return {}
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out: dict[str, list[dict]] = {}
    for s in data.get("structs", []):
        name = s["struct"]
        if name == "_root":
            continue
        out[name] = s.get("fields", [])
    return out


def parse_wire_layout(text: str) -> list[tuple[int, str]]:
    """Parse '2×u32 + 3×u32 + u16' -> [(4,u32),(12,u32),(2,u16)] segments."""
    if not text:
        return []
    parts = re.findall(r"(\d+)×(\w+)|(\d+)B|\b(u\d+|i\d+|f\d+|avatar\([^)]+\))\b", text)
    segs: list[tuple[int, str]] = []
    for mul, wt, blen, single in parts:
        if mul and wt:
            n = int(mul)
            size = {"u32": 4, "i32": 4, "u16": 2, "i16": 2, "u8": 1, "i8": 1, "f32": 4}.get(wt, 0)
            if size:
                segs.append((n * size, f"{wt}[{n}]" if n > 1 else wt))
        elif blen:
            segs.append((int(blen), "bytes"))
        elif single:
            size = {"u32": 4, "i32": 4, "u16": 2, "i16": 2, "u8": 1, "i8": 1, "f32": 4}.get(single, 1)
            segs.append((size, single))
    return segs


def parse_inline_members(meaning: str) -> list[dict]:
    """Extract `name`(type) from meaning like 成员（14）：`a`(u32)/`b`(u16)"""
    m = re.search(r"成员[（(]\d+[）)]：(.+)", meaning)
    if not m:
        m = re.search(r"打印器成员：(.+)", meaning)
    if not m:
        return []
    chunk = m.group(1)
    items = re.findall(r"`([^`]+)`(?:\(([^)]+)\))?", chunk)
    members = []
    off = 0
    for name, wt in items:
        wt = wt or "TBD"
        size = {"u32": 4, "u16": 2, "u8": 1, "i8": 1}.get(wt.split("[")[0], 4 if "u32" in wt else 2)
        if "u32[3]" in wt:
            size = 12
        members.append({
            "name": name,
            "offset": off,
            "length": size,
            "wire_type": wt,
            "meaning": "",
            "disposition": "TBD",
        })
        off += size
    return members


def fix_csv_row(row: dict) -> dict:
    """Repair rows where comma inside wire type (e.g. array<struct,104>) shifted columns."""
    wt = (row.get("线类型") or "").strip()
    fname = (row.get("字段名") or "").strip()
    row = dict(row)

    slot_m = re.fullmatch(r"(\d+)>?", fname)
    if wt == "array<struct" and slot_m:
        slot = slot_m.group(1)
        row["线类型"] = f"array<struct,{slot}>"
        row["字段名"] = (row.get("含义") or "").strip()
        row["含义"] = (row.get("用途") or "").strip()
        return row

    inner_m = re.match(r"array<struct<(\w+)>", wt)
    if inner_m and re.fullmatch(r"N\d*>?", fname):
        inner = inner_m.group(1)
        row["线类型"] = f"array<struct<{inner}>,N>"
        row["字段名"] = inner
        return row

    if wt == "array<struct" and re.fullmatch(r"N\d*>?", fname):
        real_name = (row.get("含义") or "").strip()
        row["线类型"] = "array<struct,N>"
        row["字段名"] = real_name
        row["含义"] = (row.get("用途") or "").strip()
    return row


def struct_name_from_wire_type(wire_type: str) -> str:
    wt = (wire_type or "").strip()
    for pat in (
        r"struct\s+(\w+)",
        r"struct<(\w+)>",
        r"array<struct<(\w+)>",
    ):
        m = re.match(pat, wt)
        if m:
            return m.group(1)
    return ""


def is_junk_struct_name(name: str) -> bool:
    if not name or name in TRANSIENT_NAMES:
        return True
    if re.fullmatch(r"\d+_?", name):
        return True
    if re.fullmatch(r"N\d*_?", name):
        return True
    if not re.fullmatch(r"[A-Za-z_]\w*", name):
        return True
    return False


_INLINE_STRUCT_ARR = re.compile(r"array\s*<\s*struct\s*[\(\[]")


def norm_struct_name(field_name: str, wire_type: str) -> str:
    """从字段行推结构名；推不出来就返回空——**不许拿字段名冒充类型名**。

    `array<struct(3×u16),N>`（`fire_points`）就是反例：字段名是**数组的名字**，
    元素类型是个内联元组，没有名字。早先这里回退到字段名，于是凭空长出一个
    「struct fire_points」，一路生成 composite / entity / tbl_fire_points，
    最后在归位里变成一个只有 `TBD` 成员的幻影对象（真正的元素类型由
    `fire_point` 承载，见 SC-0xA78D 的 `field_override`）。
    """
    from_wt = struct_name_from_wire_type(wire_type)
    if from_wt:
        return from_wt
    if _INLINE_STRUCT_ARR.search(wire_type or ""):
        return ""
    fn = field_name.strip().split(".")[0]
    if fn and not is_junk_struct_name(fn):
        return fn
    m = re.search(r"array<struct,(\d+)>", wire_type or "")
    if m:
        return f"struct_slot_{m.group(1)}"
    return ""


def guess_disposition(cmd: str, struct_name: str) -> str:
    if struct_name in TRANSIENT_NAMES:
        return "TRANSIENT"
    if struct_name in EVENT_STRUCTS or "-battle-" in cmd:
        if "-lounge-" in cmd and any(h in cmd for h in PERSIST_HINTS):
            return "TBD"
        if "-battle-" in cmd:
            return "EVENT"
    if "-lounge-" in cmd or "-auth-" in cmd:
        return "PERSIST"
    return "TBD"


def scan_struct_fields() -> dict[str, dict]:
    catalog: dict[str, dict] = {}
    for cmd_dir in sorted(PROTO.iterdir()):
        if not cmd_dir.is_dir():
            continue
        csv_path = cmd_dir / "fields.csv"
        if not csv_path.is_file():
            continue
        cmd = cmd_dir.name
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            for raw in csv.DictReader(f):
                row = fix_csv_row(raw)
                wt = row.get("线类型", "")
                if "struct" not in wt.lower():
                    continue
                fname = row.get("字段名", "").strip()
                if is_junk_struct_name(fname) or "长度闭合" in fname:
                    continue
                sname = norm_struct_name(fname, wt)
                if not sname:
                    continue
                length_s = row.get("长度", "").replace("N", "").strip()
                try:
                    length = int(re.sub(r"[^\d]", "", length_s) or 0)
                except ValueError:
                    length = 0
                entry = catalog.setdefault(
                    sname,
                    {
                        "id": sname,
                        "commands": set(),
                        "lengths": set(),
                        "meanings": [],
                        "wire_types": set(),
                        "protocol_paths": set(),
                    },
                )
                entry["commands"].add(cmd)
                if length:
                    entry["lengths"].add(length)
                entry["wire_types"].add(wt)
                meaning = row.get("含义", "")
                if meaning:
                    entry["meanings"].append(meaning)
                entry["protocol_paths"].add(f"protocol_analysis/commands/{cmd}/README.md")

    for v in catalog.values():
        v["commands"] = sorted(v["commands"])
        v["lengths"] = sorted(v["lengths"])
        v["wire_types"] = sorted(v["wire_types"])
        v["protocol_paths"] = sorted(v["protocol_paths"])
    return catalog


def build_members(sname: str, catalog_entry: dict, manifest_fields: list[dict]) -> list[dict]:
    if manifest_fields:
        members = []
        off = 0
        for mf in manifest_fields:
            if mf.get("struct") == "_root":
                continue
            fn = mf.get("field_name", "TBD")
            if "." in fn:
                fn = fn.split(".", 1)[1]
            try:
                ln = int(mf.get("length", 0))
            except (TypeError, ValueError):
                ln = 0
            members.append({
                "name": fn,
                "offset": mf.get("offset", off),
                "length": ln,
                "wire_type": mf.get("wire_type", ""),
                "meaning": mf.get("meaning", ""),
                "disposition": guess_disposition(mf.get("command", ""), sname),
                "wire_sources": [{
                    "command": mf.get("command"),
                    "struct": sname,
                    "field_name": fn,
                    "offset": mf.get("offset"),
                    "length": ln,
                    "wire_type": mf.get("wire_type"),
                    "protocol_path": mf.get("protocol_path"),
                    "section": mf.get("section", "§3"),
                }],
            })
            if isinstance(off, int) and ln:
                off += ln
        return members

    for meaning in catalog_entry.get("meanings", []):
        inline = parse_inline_members(meaning)
        if inline:
            return inline

    for meaning in catalog_entry.get("meanings", []):
        segs = parse_wire_layout(meaning)
        if segs:
            off = 0
            members = []
            for i, (size, wt) in enumerate(segs):
                members.append({
                    "name": "TBD",
                    "offset": off,
                    "length": size,
                    "wire_type": wt,
                    "meaning": "语义名待定",
                    "disposition": "TBD",
                })
                off += size
            return members

    length = max(catalog_entry["lengths"]) if catalog_entry["lengths"] else 0
    if length:
        return [{
            "name": "TBD",
            "offset": 0,
            "length": length,
            "wire_type": "struct",
            "meaning": "成员待从 protocol 补取证",
            "disposition": "TBD",
        }]
    return []


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cleanup_stale(prefix: str, keep: set[str], directory: Path) -> None:
    """只清理**本工具自动生成**的残留文件。

    历史事故：这里曾按「不在白名单里就删」执行，于是重跑一次就把人工补齐的
    composites/tables/entities（如 ms_rokaku、examination_item）全删了。
    现在改成：只删带 `autogen` 标记、或 status 仍是 proposed/draft/tbd 的文件；
    status=complete/verified 的手写产物一律保留并打印告警。
    """
    if not directory.is_dir():
        return
    removed: list[str] = []
    kept: list[str] = []
    for path in directory.glob(f"{prefix}*.json"):
        if path.stem in keep:
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        marker = data.get("autogen") is True
        status = str(data.get("status", "")).strip().lower()
        if not marker and status not in ("proposed", "draft", "tbd"):
            kept.append(path.name)
            continue
        path.unlink()
        removed.append(path.name)
    if removed:
        print(f"  cleanup {directory.name}: 删除自动生成残留 {len(removed)} 个 -> {sorted(removed)[:5]}")
    if kept:
        print(f"  cleanup {directory.name}: 跳过手写产物 {len(kept)} 个 -> {sorted(kept)[:5]}")


def main() -> None:
    manifest_members = load_manifest_members()
    catalog = scan_struct_fields()

    catalog_path = SCHEMA / "_meta" / "struct_catalog.json"
    write_json(catalog_path, {
        "generated": date.today().isoformat(),
        "struct_count": len(catalog),
        "structs": catalog,
    })

    composites_dir = SCHEMA / "composites"
    tables_dir = SCHEMA / "_legacy_tables"
    entities_dir = SCHEMA / "entities"
    preserve_composites = {
    "avatar", "ms_set", "equip_set", "item", "missionunit_set", "roominfo", "cinfo",
    "pilot_detail", "examination_state", "cshist_item", "rental_module", "favms", "beginner_challenge_info",
    "pilots_list", "pcard", "lpcard", "ms", "snapshot", "funnelss", "unlockw", "adop_list", "recruits", "leaders",
    "bracket", "bracket_node", "bracket_info", "AI", "item_list", "party_member_stat", "order", "rankself", "ranking", "toppilots", "ranking_info", "special_a_info", "special_a_next", "sort_info", "ext_subrule", "xwar_ext_rule", "extrarule_xwar_info", "wbonus", "eq_bonus_modules_lot",     "buffitem", "buffitem_ex", "config", "progress", "bgm_desc", "phase_info", "block_detail", "buildup_info", "challenge_info", "trchallenge_info", "check_quest", "wave_res", "appear_info", "adop_get", "clan_eff", "clan_zeon",     "dailycup_conf", "dailycup_conf_next", "dc_point", "dcpoint_detail", "exam_state",
    "friend_histories", "member", "intro_info", "hack_check",
    "lvjudge_hist", "mprogress", "netcafe_challenge_info", "unlocked_navi",
    "pointdmg", "total_result_wave", "recruit", "replay_info", "season_rb_conf", "precord",
    "pilot", "clan", "cupteam",
}

    table_ids: list[str] = []
    generated_composites: set[str] = set()
    generated_tables: set[str] = set()
    generated_entities: set[str] = set()
    stats = {"composites": 0, "tables": 0, "entities": 0, "persist": 0,
             "event": 0, "tbd": 0, "no_table": 0, "alias": 0}

    # 显式登记为「不建表 / 是别名的轻量线形」的结构：磁盘上若还留着旧的自动产物，
    # 在这里先删掉。清理逻辑是「磁盘上已有的表一律保留」（事故加固的取舍），
    # 所以不做这一步，被否掉的小表会永远留在 relations.json 里继续生成 DDL。
    dropped: list[str] = []
    for orphan in sorted(NO_TABLE_STRUCTS | set(STRUCT_ALIASES)):
        stale = tables_dir / f"tbl_{orphan}.json"
        if stale.is_file():
            stale.unlink()
            dropped.append(stale.name)
        if orphan in NO_TABLE_STRUCTS:
            stale_ent = entities_dir / f"{orphan}.json"
            if stale_ent.is_file():
                stale_ent.unlink()
                dropped.append(stale_ent.name)
    if dropped:
        print(f"  否决表/别名：删除陈旧自动产物 {len(dropped)} 个 -> {sorted(dropped)}")

    for sname, info in sorted(catalog.items()):
        members = build_members(sname, info, manifest_members.get(sname, []))
        length = max(info["lengths"]) if info["lengths"] else sum(m.get("length", 0) for m in members if isinstance(m.get("length"), int))

        disp = guess_disposition(info["commands"][0] if info["commands"] else "", sname)
        for cmd in info["commands"]:
            d = guess_disposition(cmd, sname)
            if d == "PERSIST":
                disp = "PERSIST"
                break
            if d == "EVENT" and disp != "PERSIST":
                disp = "EVENT"

        comp_path = composites_dir / f"{sname}.json"
        if sname not in preserve_composites and not is_complete_json(comp_path):
            comp = {
                "id": sname,
                "title": f"{sname}（{length}B）",
                "length": length,
                "status": "proposed",
                "autogen": True,
                "evidence": {
                    "commands": info["commands"][:5],
                    "protocol_paths": info["protocol_paths"][:3],
                },
                "members": members,
            }
            write_json(composites_dir / f"{sname}.json", comp)
            generated_composites.add(sname)
            stats["composites"] += 1

        tid = f"tbl_{sname}"
        table_path = tables_dir / f"{tid}.json"
        col_disp = disp if disp != "TRANSIENT" else "TBD"
        primary_cmd = info["commands"][0]
        proto = info["protocol_paths"][0]

        if sname in NO_TABLE_STRUCTS:
            # 入参/回显型结构：不建表、不建实体（composite 仍保留，线形要能查）。
            stats["no_table"] += 1
            continue

        alias_of = STRUCT_ALIASES.get(sname)
        if alias_of:
            # 轻量线形：只登记「这形属于哪张表」，不另建表。
            write_json(entities_dir / f"{sname}.json", {
                "id": sname,
                "title": f"{sname}（{alias_of} 的轻量线形）",
                "autogen": True,
                "description": (f"协议实体 {sname}；{length}B；是 {alias_of} 的前缀线形，"
                                f"持久化落在 tbl_{alias_of}"),
                "alias_of": alias_of,
                "table_ref": f"tbl_{alias_of}",
                "disposition": disp,
                "wire_forms": [{
                    "name": sname,
                    "length": length,
                    "prefix_of": alias_of,
                    "commands": info["commands"][:5],
                    "protocol_path": proto,
                }],
                # 别名实体自身的 `fields` **留空**：成员清单的唯一出处是
                # `composites/<id>.json`（口径见 db_design/README.md「成员清单在 composites
                # 一处维护、站点就地展开」）。`build_site.build_entity_detail` 对空 `fields`
                # 会走 `composite_members(fid, composites)` 摊平（含 `prefix_of` 前缀截取）。
                # ★ 反面教材：这里原先写 `members if members else [{name, length, …}]`，
                # 给没有 inline 成员的别名壳塞了一个**占位 blob**，于是
                # `entities/ms_lounge.json` 顶着 `fields: [TBD 303B, TBD 312B]` 的假成员清单，
                # 既挡住站点的摊平回退、又让 `check_meanings.py` 报「语义名待定」。
                "fields": [],
            })
            generated_entities.add(sname)
            stats["alias"] += 1
            continue

        if tid in MANUAL_TABLES or is_complete_json(table_path):
            if is_complete_json(table_path):
                table_ids.append(sname)
            continue

        table_disp = "proposed"
        if col_disp == "PERSIST":
            stats["persist"] += 1
        elif col_disp == "EVENT":
            stats["event"] += 1
        else:
            stats["tbd"] += 1

        table = {
            "id": tid,
            "title": f"{sname}（提议表）",
            "status": "proposed",
            "autogen": True,
            "purpose": f"协议结构 {sname}；证据来自 {len(info['commands'])} 条命令",
            "entity_ref": sname,
            "table_disposition": col_disp,
            "evidence_commands": info["commands"][:8],
            "column_groups": [{"name": sname, "columns": [sname]}],
            "columns": [{
                "name": sname,
                "disposition": "COMPOSITE" if members else col_disp,
                "composite_ref": sname if members else None,
                "meaning": info["meanings"][0][:200] if info.get("meanings") else "",
                "wire_sources": [{
                    "command": primary_cmd,
                    "struct": sname,
                    "length": length,
                    "wire_type": info["wire_types"][0] if info["wire_types"] else "",
                    "protocol_path": proto,
                }],
            }],
        }
        if not members:
            table["columns"][0].pop("composite_ref", None)
        write_json(tables_dir / f"{tid}.json", table)
        table_ids.append(sname)
        generated_tables.add(tid)
        stats["tables"] += 1

        entity = {
            "id": sname,
            "title": sname,
            "autogen": True,
            "description": f"协议实体 {sname}；{length}B；{len(info['commands'])} 命令引用",
            "table_ref": tid,
            "disposition": col_disp,
            "wire_forms": [{
                "name": sname,
                "length": length,
                "commands": info["commands"][:5],
                "protocol_path": proto,
            }],
            "fields": members if members else [{
                "name": sname,
                "length": length,
                "disposition": col_disp,
                "wire_sources": [{"command": primary_cmd, "protocol_path": proto}],
            }],
        }
        ent_path = entities_dir / f"{sname}.json"
        if sname == "pilot":
            pass  # keep manual pilot.json
        else:
            write_json(ent_path, entity)
            generated_entities.add(sname)
            stats["entities"] += 1

    # 磁盘上已有的表一律保留并登记：人工表（如 tbl_pilot_evflag3 / tbl_ms_rokaku）不在
    # protocol 目录里，若只按 catalog 推导就会被 cleanup 删掉、也被 relations.json 漏掉
    # （历史事故：人工表被删 + 生成器报「缺表」）。
    on_disk_tables = {p.stem for p in tables_dir.glob("tbl_*.json")}
    on_disk_entities = {p.stem for p in entities_dir.glob("*.json")}
    preserved_tables = on_disk_tables | MANUAL_TABLES | generated_tables
    preserved_entities = on_disk_entities | generated_entities | {"pilot"}

    cleanup_stale("", preserve_composites | generated_composites, composites_dir)
    cleanup_stale("tbl_", preserved_tables, tables_dir)
    cleanup_stale("", preserved_entities, entities_dir)

    all_table_ids = sorted(preserved_tables)

    # 旧 `schema/relations.json`（旧表注册表）已退役：它只是把 `_legacy_tables/*.json`
    # 的 id/status/purpose/disposition 抄一份，抄出来的那份还得靠人工补字段
    # （`tbl_pilot` 的 disposition 就只写在这里），两处并存迟早对不上。旧表所需的全部
    # 事实（含旧库唯一键列序/列清单）现在由 `schema/_meta/legacy_evidence.json` 承载
    # （`tools/freeze_legacy.py` 冻结），站点也改读它。所以这里**不再写**注册表。

    meta_path = SCHEMA / "_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    meta["updated"] = date.today().isoformat()
    meta["phase"] = "P1-full"
    meta.setdefault("stats", {})
    meta["stats"].update({
        "structs_cataloged": len(catalog),
        "composites_generated": stats["composites"],
        "tables_generated": len(all_table_ids),
        "entities_generated": stats["entities"] + 1,
        "tables_persist_hint": stats["persist"],
        "tables_event_hint": stats["event"],
        "tables_tbd_hint": stats["tbd"],
    })

    # 命令维度（schema/commands/）：由 import_commands.py 导入、verify_commands_ida.py 复核、
    # derive_behavior.py 补行为；这里只做**投影统计**，不生成命令模型本体。
    cmd_idx_path = SCHEMA / "commands" / "index.json"
    cmd_stats: dict = {}
    if cmd_idx_path.is_file():
        try:
            ci = json.loads(cmd_idx_path.read_text(encoding="utf-8"))
            counts = ci.get("counts", {})
            by_status = counts.get("by_status", {})
            cmd_stats = {
                "commands_modeled": counts.get("commands", 0),
                "command_fields": counts.get("fields", 0),
                "commands_asm_verified": by_status.get("ASM-VERIFIED", 0)
                                         + by_status.get("BEHAVIOR-DONE", 0),
                "commands_behavior_done": by_status.get("BEHAVIOR-DONE", 0),
                "commands_with_db_effects": counts.get("commands_with_db_effects", 0),
            }
            meta["stats"].update(cmd_stats)
        except (json.JSONDecodeError, OSError):
            cmd_stats = {}
    write_json(meta_path, meta)

    # 统计一律从磁盘现读：这份进度页是 db_design 的门面，硬编码名单在补了
    # ms_rokaku/evflag3 这类新产物后就开始说谎（此前写死 `tbl_pilot/tbl_ms_set/
    # tbl_equip_set/tbl_item`，后来手写表翻了一倍多）。
    def _count(sub: str) -> int:
        return len(list((SCHEMA / sub).glob("*.json")))

    # 「人工精修」的可核对口径：**声明了 `row_key`**——生成器从不写这个字段，
    # 它只可能来自人（槽位键/成员键/外部键这一族，见 `schema/tables/*.json`）。
    hand_tables = []
    for p in sorted((SCHEMA / "_legacy_tables").glob("*.json")):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if obj.get("row_key"):
            hand_tables.append(p.stem)
    hand_table_list = " / ".join(f"`{t}`" for t in hand_tables) or "（无）"

    queue_path = SCHEMA / "_meta" / "completion_queue.json"
    progress_path = SCHEMA / "_meta" / "进度.md"
    skip_progress = False
    if queue_path.is_file():
        try:
            q = json.loads(queue_path.read_text(encoding="utf-8"))
            # 「队列已跑完就不再重写首页」是个省事的优化，但**文件本身丢了就不能再省**：
            # 首页是 db_design 的门面，`docs/01-命令模型.md` 也拿它当统计口径的出处。
            skip_progress = (
                progress_path.is_file()
                and q.get("next") is None
                and len(q.get("completed", [])) >= len(catalog)
            )
        except (json.JSONDecodeError, OSError):
            pass
    if not skip_progress:
        cmd_block = ""
        if cmd_stats:
            cmd_block = f"""
## 命令知识库（schema/commands/）

| 项 | 数量 |
|---|---|
| 建模命令 | {cmd_stats['commands_modeled']} |
| 字段行 | {cmd_stats['command_fields']} |
| ASM-VERIFIED 及以上 | {cmd_stats['commands_asm_verified']} |
| BEHAVIOR-DONE | {cmd_stats['commands_behavior_done']} |
| 已映射 DB 影响 | {cmd_stats['commands_with_db_effects']} |

口径见 `docs/01-命令模型.md` / `docs/02-命令能力表.md`；状态阶梯
`IMPORTED → ASM-VERIFIED → BEHAVIOR-DONE`，IDA 汇编是类型与去向的唯一权威。
"""
        progress = f"""# db_design 提炼进度（全量推进）

> 生成日期：{date.today().isoformat()}  
> 工具：`generate_all.py`

## 统计

| 项 | 数量 |
|---|---|
| 协议 struct 种类 | {len(catalog)} |
| composites（磁盘） | {_count('composites')} |
| 提议表 | {len(all_table_ids)} |
| entities（磁盘） | {_count('entities')} |
| 其中已声明 `row_key`（人工精修） | {len(hand_tables)} |
{cmd_block}
## 说明

- `table_disposition` / 列 `disposition` 为**启发式初稿**，需人工复核
- 战斗域 struct 默认 `EVENT`（不入库候选）
- 生成器**只补缺、不覆写**已存在的 `composites/`/`tables/`/`entities/`；`cleanup_stale()`
  只删带 `autogen: true` 且未定稿（`proposed/draft/tbd`）的文件
- 别名壳（`layout_same_as` / `prefix_of`）的成员由 `materialize_alias_members.py` **摊平落盘**：
  站点本来也会沿别名展开，但 JSON 层不能是空的（不能只写「见 XXX」）；`--check` 报漂移
- **别名实体（`entities/*.json`，`STRUCT_ALIASES` 命中的那些）反过来：本生成器写 `fields: []`** ——
  成员只在 `composites/<id>.json` 一处维护，站点 `build_entity_detail` 对空 `fields` 就地摊平。
  （曾往别名实体塞占位 blob，让 `entities/ms_lounge.json` 顶着两个 `TBD` 成员清单。）
- 已声明行键（人工精修，生成器不写此字段）：{hand_table_list}

## 命令

```powershell
python db_design/tools/sync_structs_from_protocol.py
python db_design/tools/generate_all.py
python db_design/tools/materialize_alias_members.py --check   # 别名壳成员是否漂移（composite 摊平 + 别名实体 fields 该空）
python db_design/tools/materialize_alias_members.py          # 把 layout_same_as/prefix_of 的成员摊平落盘
python db_design/tools/import_commands.py          # 命令模型（幂等；不改已复核状态）
python db_design/tools/verify_commands_ida.py plan --batch N   # 挑批次
python db_design/tools/verify_commands_ida.py emit --batch N   # 写 IDA 作业 → 在 IDA 里跑 ida_verify_batch.py
python db_design/tools/verify_commands_ida.py ingest --batch N # 六项检查 + diff 回填
python db_design/tools/derive_behavior.py --write  # behavior/capabilities/db_effects
python db_design/tools/derive_behavior.py --validate
python db_design/tools/build_site.py
```
"""
        progress_path.write_text(progress, encoding="utf-8")

    print(f"Catalog: {len(catalog)} structs")
    print(f"Generated: {stats['composites']} composites, {stats['tables']} tables, {stats['entities']} entities")
    print(f"On disk: {_count('composites')} composites / {len(all_table_ids)} tables / {_count('entities')} entities"
          f"（声明行键 {len(hand_tables)}）")
    print(f"Relations: {len(all_table_ids)} tables")
    if cmd_stats:
        print("Commands: {commands_modeled} 条 / 字段 {command_fields} / "
              "ASM-VERIFIED+ {commands_asm_verified} / BEHAVIOR-DONE {commands_behavior_done} / "
              "DB 影响 {commands_with_db_effects}".format(**cmd_stats))


if __name__ == "__main__":
    main()

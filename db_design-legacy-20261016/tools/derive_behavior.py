#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive_behavior.py —— 为命令模型补 `behavior[] / capabilities[] / db_effects[]`。

口径来源
--------
* `docs/01-命令模型.md`：状态阶梯（IMPORTED → ASM-VERIFIED → BEHAVIOR-DONE）与证据要求。
* `docs/02-命令能力表.md`：能力受控标签表（动词 + `域.对象`）。
* `schema/commands/_schema.json`：`behavior_step` / `db_effect` 的字段与取值域（严格校验）。

三条产出规则（**每条都要指得回汇编 VA**）
----------------------------------------
1. `behavior[]` —— 逐字段的读写步骤 + 守卫/分配/闭合/去向/报错路径。
   step 的按序来源：opcode → (C→S 分配) → 守卫 → 逐字段 → 闭合/提交 → 去向 → 报错/通知。
   证据 VA 优先取 `asm_verification.checks` 的实测值，退化到字段自身的 `evidence_va`
   （后者本来就是 `protocol_analysis` 里的汇编证据 VA）。
2. `capabilities[]` —— 受控标签；**只有 ASM-VERIFIED 及以上的命令才写**（schema 明令：
   无汇编证据前必须为空）。动词标签由命名学给出，`capabilities_derived` 原样保留作对照。
3. `db_effects[]` —— **只认既有证据**：`schema/tables/*.json` 的 `columns[].wire_sources[]`
   与 `schema/entities/*.json` 的 `wire_forms[].commands[]`。没有证据的命令留空并写
   `db_effects_note`，绝不凭命名臆造表/字段。

用法
----
    python tools/derive_behavior.py --summary           # 只统计，不写
    python tools/derive_behavior.py --write             # 全量写回
    python tools/derive_behavior.py --write --only SC-0xF11C-...
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
CMD_DIR = SCHEMA / "commands"
TABLE_DIR = SCHEMA / "_legacy_tables"
ENTITY_DIR = SCHEMA / "entities"

# ---------------------------------------------------------------- 能力标签表

#: 动词标签：**顺序即优先级**（同一命令可命中多个，最多取 3 个）
VERB_TAGS: list[tuple[str, str]] = [
    ("delete", r"(_del\b|_del_|_delete|_discard|_leave|_kick|_refuse|_cancel|_remove"
               r"|_clear|_disband|_drop|_unregist)"),
    ("create", r"(_create|_add\b|_add_|_new\b|_post\b|_entry|_buy|_gacha|_make|_regist"
               r"|_install|_deploy|_spawn|_build|_open\b)"),
    ("settle", r"(_settle|_result|_reward|_ranking|_score|_charge|_pay\b|_trade"
               r"|_exchange|_deposit|_withdraw|_repair|_heal|_refuel|_supply)"),
    ("validate", r"(_verify|_validate|_auth|_login|_probe|_captcha)"),
    ("battle_action", r"(_attack|_damage|_fire|_weapon|_skill|_combat|_battle"
                      r"|_hp\b|_respawn|_snapshot)"),
    ("notify", r"(_notice|_notify|_broadcast|_announce|_sync|_push|_ack)"),
    ("report", r"(_report|_record|_trace|_stat\b|_log\b)"),
    ("update", r"(_set\b|_set_|_edit|_update|_store|_change|_apply|_rename|_unlock"
               r"|_equip|_modify|_use\b|_upgrade|_move|_put\b|_save)"),
    ("flow", r"(_begin|_end\b|_start|_stop|_enter|_exit|_suspend|_resume|_ready"
             r"|_init|_close|_quit|_join|_leave_)"),
    ("query", r"(_get|_list|_search|_info|_select|_check|_query|_find|_load|_read)"),
]
VERB_RE = [(tag, re.compile(rx)) for tag, rx in VERB_TAGS]

#: 标签里不参与「对象名」的通用词
STOP_TOKENS = {"r", "a", "n", "req", "res", "ack", "proto", "msma"}

#: 命令名动词 → DB 影响（`db_effect.op` 的取值域只有 read/create/update/delete/none）
DB_OP = {
    "query": "read", "create": "create", "update": "update",
    "delete": "delete", "settle": "update", "battle_action": "update",
    "validate": "read", "flow": "update", "notify": "read", "report": "none",
}

SCALAR = {"u8", "i8", "char", "bool", "u16", "i16", "u32", "i32", "u64", "i64",
          "f32", "f64", "u8[]", "u16[]"}

#: `str` 必须是词边界：`struct xxx` 也以 "str" 开头（别用 startswith）
STR_LIKE_RE = re.compile(r"^str(?![a-z])|^string(?![a-z])|^blob(?![a-z])|^char\[")


def load_json(path: Path):
    with open(path, encoding="utf-8") as fp:
        return json.load(fp)


def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=1)


def first_va(*vals) -> str | None:
    """把 `B7B7F8|B7B807` / `0xB7B7F8` / `0xB7B7F8, 0xB7B807` 归一为第一个带 0x 的 VA。"""
    for v in vals:
        if not v:
            continue
        for part in re.split(r"[|,;\s]+", str(v)):
            m = re.search(r"([0-9A-Fa-f]{5,})", part)
            if m:
                return "0x" + m.group(1).upper()
    return None


# ---------------------------------------------------------------- DB 证据

def load_db_evidence() -> dict[str, list[dict]]:
    """命令 id → 既有实体/表证据（表侧优先，因为表侧带列名与 wire_source VA）。"""
    ev: dict[str, list[dict]] = {}

    def add(cid: str, eff: dict) -> None:
        ev.setdefault(cid, [])
        key = (eff.get("table_ref"), eff.get("entity"), eff.get("fields", [None])[0], eff.get("op"))
        for old in ev[cid]:
            if (old.get("table_ref"), old.get("entity"), old.get("fields", [None])[0],
                    old.get("op")) == key:
                return
        ev[cid].append(eff)

    for p in sorted(TABLE_DIR.glob("*.json")):
        tbl = load_json(p)
        for col in tbl.get("columns", []) or []:
            for ws in col.get("wire_sources", []) or []:
                cid = ws.get("command")
                if not cid:
                    continue
                add(cid, {
                    "entity": tbl.get("entity_ref"),
                    "table_ref": tbl.get("id"),
                    "op": None,            # 由命令动词定
                    "fields": [f for f in [ws.get("field_name") or col.get("name")] if f],
                    "disposition": col.get("disposition") or tbl.get("table_disposition"),
                    "evidence_va": first_va(ws.get("evidence_va"), ws.get("reader"),
                                            ws.get("printer")) or "?",
                    "source": "tables/%s.json" % tbl.get("id"),
                    "wire_type": ws.get("wire_type"),
                    "offset": ws.get("offset"),
                    "length": ws.get("length"),
                })
    for p in sorted(ENTITY_DIR.glob("*.json")):
        ent = load_json(p)
        for wf in ent.get("wire_forms", []) or []:
            for cid in wf.get("commands", []) or []:
                va = first_va(wf.get("evidence_va"), wf.get("reader"), wf.get("printer"))
                add(cid, {
                    "entity": ent.get("id"),
                    "table_ref": ent.get("table_ref"),
                    "op": None,
                    "fields": [wf.get("name") or ent.get("id")],
                    "disposition": ent.get("disposition"),
                    "evidence_va": va or "?",
                    "source": "entities/%s.json" % ent.get("id"),
                    "wire_type": "struct",
                    "offset": None,
                    "length": wf.get("length"),
                })
    return ev


# ---------------------------------------------------------------- 能力标签

def verb_tags(name: str) -> list[str]:
    n = "_" + str(name).lower()
    out = [tag for tag, rx in VERB_RE if rx.search(n)]
    return out[:3] or ["unclassified"]


def object_tag(proto: str | None, name: str) -> str | None:
    toks = [t for t in re.split(r"_+", str(name).lower()) if t]
    keep: list[str] = []
    for t in toks:
        if t in STOP_TOKENS or t.isdigit():
            continue
        if any(rx.search("_" + t) for _tag, rx in VERB_RE):
            break
        keep.append(t)
        if len(keep) == 2:
            break
    if not keep:
        return None
    return "%s.%s" % (proto or "?", "_".join(keep))


def capabilities_of(cmd: dict) -> tuple[list[str], list[str]]:
    """返回 `(capabilities, capabilities_derived)`，同一受控词表。

    * `capabilities_derived` = 只由命令名得到的动词标签（命名学，恒有）；
    * `capabilities` = 动词标签 + `域.对象`，**只有该命令证据齐全时才给**
      （见 `decide()`：`behavior[]` 每步都能指回汇编 VA）。
    """
    verbs = verb_tags(cmd.get("name", ""))
    obj = object_tag(cmd.get("proto"), cmd.get("name", ""))
    caps = list(verbs)
    if obj:
        caps.append(obj)
    return caps, verbs


# ---------------------------------------------------------------- 行为步骤

def field_kind(cmd: dict, f: dict, count_driven: set[str]) -> str:
    wt = str(f.get("wire_type") or "")
    sc = cmd.get("direction") == "SC"
    if f.get("name") in count_driven:
        return "read_count" if sc else "write_count"
    if STR_LIKE_RE.match(wt) and not wt.startswith("struct"):
        return "read_string" if sc else "write_string"
    if wt.startswith("array<") or re.search(r"\[\d+\]$", wt):
        return "read_array" if sc else "write_array"
    if wt.startswith("struct") or wt.startswith("composite"):
        return "read_struct" if sc else "write_struct"
    return "read_scalar" if sc else "write_scalar"


def behavior_of(cmd: dict) -> list[dict]:
    direction = cmd.get("direction")
    asm = cmd.get("asm_verification") or {}
    chk = asm.get("checks") or {}
    extra = cmd.get("extra") or {}
    fields = [f for f in cmd.get("fields", []) if not f.get("is_closure")]
    # 成员占位行（`父.成员`）不是独立行为步：父行的 composite 已在同一步里摊平成员。
    fields = [f for f in fields if not f.get("is_member_row")]

    # 计数字段：被 struct 成员的 count_field 引用
    count_driven: set[str] = set()
    for st in (cmd.get("structs") or {}).values():
        for m in st.get("members", []):
            if m.get("count_field"):
                count_driven.add(m["count_field"])

    steps: list[dict] = []

    def push(kind: str, detail: str, va) -> None:
        steps.append({"step": 0, "kind": kind, "detail": detail,
                      "evidence_va": va or "?"})

    op = next((f for f in fields if f.get("seq") == 0), None)
    payload = [f for f in fields if f.get("seq", 0) >= 1 and not f.get("is_member_row")]
    push("read_scalar" if direction == "SC" else "write_scalar",
         "opcode %s（分发器 switch 选择子）" % cmd.get("opcode"),
         first_va(extra.get("opcode_field_va"), extra.get("opcode_write_va"),
                  (op or {}).get("evidence_va")) or "0x%04X" % 0)

    cap = chk.get("capacity") or {}
    cap_va = cap.get("va") or cmd.get("capacity_va")
    if direction == "CS" and cap_va:
        push("alloc", "分配发送缓冲 %s B（`[X+78h]` 分配器 + `push IMM`）"
                      % (cmd.get("capacity") or cap.get("value")), cap_va)

    guard = ((chk.get("field_window") or {}).get("guard") or {})
    if guard.get("va"):
        push("guard", "进入解码窗口：守卫 `%s`（模块 id %s）→ 之后逐字段读线"
                      % (guard.get("func"), guard.get("module_id")), guard["va"])

    for f in payload:
        wt = f.get("wire_type")
        cnt = f.get("count_field") or f.get("element_count_field")
        detail = "%s：`%s`（线长 %s）—— %s" % (
            f.get("name"), wt, f.get("length"), str(f.get("meaning") or "")[:110])
        if cnt:
            detail += "；条数驱动 = %s" % cnt
        info = "".join(str(f.get(k) or "") for k in ("enum",))
        if "上限" in info:
            detail += "；%s" % info[:60]
        push(field_kind(cmd, f, count_driven), detail,
             first_va(*(f.get("evidence_va") or [])))

    closer = chk.get("closer") or {}
    cl_va = closer.get("va") or cmd.get("closer_va")
    if direction == "SC" and cl_va:
        push("close_check", "闭合校验：读游标 == 报文末尾（%s）"
             % (closer.get("kind") or "见 README 闭合行"), cl_va)
    if direction == "CS":
        commit_va = closer.get("va") if closer.get("kind") == "commit" else (cl_va if cl_va else None)
        if commit_va:
            push("commit", "提交/发送 `sub_B02FF0(buf)`：定长报文提交点", commit_va)

    disp = chk.get("dispatch_slot") or {}
    d_va = disp.get("va") or cmd.get("dispatch_va")
    slot = disp.get("slot") or cmd.get("dispatch_slot")
    if d_va and slot:
        argc = disp.get("argc")
        if direction == "CS":
            push("send", "去向 `%s(buf, 负载长度)`%s"
                 % (slot, "，实参 %d 个" % argc if argc else ""), d_va)
        else:
            push("dispatch", "交业务 `%s`%s" % (slot, "，实参 %d 个" % argc if argc else ""), d_va)

    err = disp.get("error_slot") or {}
    if err.get("va") or extra.get("error_vas"):
        push("error_path", "失败路径 `vt[0x64](1, 错误码)`（不是业务去向）",
             err.get("va") or first_va(*(extra.get("error_vas") or [])))
    if extra.get("notify_va"):
        push("notify", "附加通知回调 `[obj+79A8h]`（模块 id，非字段）",
             first_va(extra.get("notify_va")))

    if not payload:
        push("read_scalar" if direction == "SC" else "write_scalar",
             "零负载：无报文体字段，仅 opcode + 去向", cl_va or d_va or "?")

    for i, s in enumerate(steps, 1):
        s["step"] = i
    return steps


# ---------------------------------------------------------------- 组装

def db_effects_of(cmd: dict, ev: dict) -> tuple[list[dict], str | None]:
    raw = ev.get(cmd["id"]) or []
    if not raw:
        return [], ("无既有实体/表证据（`schema/entities|tables` 里没有指向本命令的 "
                    "wire_source）→ 待批次复核时补映射")
    tags = verb_tags(cmd.get("name", ""))
    op = DB_OP.get(tags[0], "none")
    out = []
    for r in raw:
        eff = {
            "entity": r.get("entity"),
            "table_ref": r.get("table_ref"),
            "op": op,
            "fields": r.get("fields") or [],
            "disposition": r.get("disposition") or "TBD",
            "evidence_va": r.get("evidence_va") or "?",
        }
        out.append(eff)
    return out, None


def decide(cmd: dict, steps: list[dict], caps: list[str], effs: list[dict],
           db_note: str | None) -> tuple[str, bool]:
    """返回 `(新状态, 行为是否已就绪)`。

    行为就绪（`ready`）= `behavior[]` 非空且每步都有汇编 VA，`capabilities[]` 非空，
    且 `db_effects[]` 非空或已写明 `db_effects_note`。
    状态只有在该命令已经 `ASM-VERIFIED` 时才会被推到 `BEHAVIOR-DONE`。
    """
    asm = cmd.get("asm_verification") or {}
    status = asm.get("status", "IMPORTED")
    ok_steps = bool(steps) and all(s["evidence_va"] not in (None, "", "?") for s in steps)
    ready = bool(ok_steps and caps and (effs or db_note))
    if status in ("ASM-VERIFIED", "BEHAVIOR-DONE") and ready:
        return "BEHAVIOR-DONE", True
    return status, ready


BEHAVIOR_KINDS = {
    "guard", "alloc", "read_scalar", "read_string", "read_count", "read_array",
    "read_struct", "close_check", "dispatch", "send", "notify", "error_path",
    "write_scalar", "write_string", "write_count", "write_array", "write_struct",
    "commit",
}
DB_OPS = {"read", "create", "update", "delete", "none"}
DISPOSITIONS = {"PERSIST", "CONFIG", "DERIVED", "TRANSIENT", "EVENT", "COMPOSITE", "TBD"}
STATUSES = {"IMPORTED", "ASM-VERIFIED", "BEHAVIOR-DONE", "BLOCKED"}


def validate_commands() -> int:
    """对 `schema/commands/*.json` 做**严格**结构校验（镜像 `_schema.json` 的硬约束）。

    只为 `behavior_step` / `db_effect` / `asm_verification` 这几处
    `additionalProperties: false` 与枚举写死校验 —— 这是站点与下游代码的契约。
    """
    problems: list[str] = []
    n = 0
    for p in sorted(CMD_DIR.glob("*.json")):
        if p.name.startswith("_") or p.name == "index.json":
            continue
        cmd = load_json(p)
        cid = cmd.get("id") or p.stem
        n += 1
        for k in ("id", "opcode", "direction", "proto", "name", "fields", "structs",
                  "wire", "asm_verification"):
            if k not in cmd:
                problems.append("%s 缺必填键 %s" % (cid, k))
        for i, s in enumerate(cmd.get("behavior") or [], 1):
            extra = set(s) - {"step", "kind", "detail", "evidence_va"}
            if extra:
                problems.append("%s behavior[%d] 多余键 %s" % (cid, i, sorted(extra)))
            if s.get("kind") not in BEHAVIOR_KINDS:
                problems.append("%s behavior[%d] kind 非法：%r" % (cid, i, s.get("kind")))
            if s.get("step") != i:
                problems.append("%s behavior[%d] step 序号不连续：%r" % (cid, i, s.get("step")))
            if not str(s.get("detail") or "").strip():
                problems.append("%s behavior[%d] detail 为空" % (cid, i))
            if not s.get("evidence_va"):
                problems.append("%s behavior[%d] 无 evidence_va" % (cid, i))
        for i, e in enumerate(cmd.get("db_effects") or [], 1):
            extra = set(e) - {"entity", "table_ref", "op", "fields", "disposition",
                              "evidence_va"}
            if extra:
                problems.append("%s db_effects[%d] 多余键 %s" % (cid, i, sorted(extra)))
            if e.get("op") not in DB_OPS:
                problems.append("%s db_effects[%d] op 非法：%r" % (cid, i, e.get("op")))
            if e.get("disposition") not in DISPOSITIONS:
                problems.append("%s db_effects[%d] disposition 非法：%r"
                                % (cid, i, e.get("disposition")))
            if not (e.get("entity") or e.get("table_ref")):
                problems.append("%s db_effects[%d] entity/table_ref 全空" % (cid, i))
        av = cmd.get("asm_verification") or {}
        if av.get("status") not in STATUSES:
            problems.append("%s asm_verification.status 非法：%r" % (cid, av.get("status")))
        if av.get("status") == "BEHAVIOR-DONE" and not (cmd.get("capabilities") or []):
            problems.append("%s 标 BEHAVIOR-DONE 但 capabilities 为空" % cid)
        for f in cmd.get("fields") or []:
            if f.get("disposition") not in DISPOSITIONS:
                problems.append("%s fields[%s].disposition 非法：%r"
                                % (cid, f.get("name"), f.get("disposition")))
    print("[validate] 校验 %d 条命令：%s" % (n, "通过" if not problems else "发现 %d 处问题"
                                            % len(problems)))
    for s in problems[:60]:
        print("  - %s" % s)
    if len(problems) > 60:
        print("  … 其余 %d 处省略" % (len(problems) - 60))
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="补 behavior/capabilities/db_effects")
    ap.add_argument("--write", action="store_true", help="写回 schema/commands/*.json")
    ap.add_argument("--summary", action="store_true", help="只打印统计")
    ap.add_argument("--validate", action="store_true", help="严格结构校验（只读）")
    ap.add_argument("--only", nargs="*", default=None, help="只处理这些命令 id")
    args = ap.parse_args()

    if args.validate:
        return validate_commands()

    ev = load_db_evidence()
    files = sorted(CMD_DIR.glob("*.json"))
    cmds = []
    for p in files:
        if p.name.startswith("_") or p.name == "index.json":
            continue
        cmds.append((p, load_json(p)))
    if args.only:
        want = set(args.only)
        cmds = [(p, c) for p, c in cmds if c.get("id") in want]

    stat = Counter()
    step_stat = Counter()
    updated = []
    for p, cmd in cmds:
        steps = behavior_of(cmd)
        caps, dverbs = capabilities_of(cmd)
        effs, db_note = db_effects_of(cmd, ev)
        status, ready = decide(cmd, steps, caps, effs, db_note)
        ok_steps = bool(steps) and all(s["evidence_va"] not in (None, "", "?") for s in steps)

        stat["命令"] += 1
        stat["有 behavior"] += 1 if steps else 0
        stat["step 全带 VA"] += 1 if ok_steps else 0
        stat["有 db_effects"] += 1 if effs else 0
        stat["行为就绪"] += 1 if ready else 0
        stat["BEHAVIOR-DONE"] += 1 if status == "BEHAVIOR-DONE" else 0
        for s in steps:
            step_stat[s["kind"]] += 1

        if args.write:
            cmd["behavior"] = steps
            cmd["behavior_derived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cmd["capabilities_derived"] = dverbs
            # 能力标签只在证据齐全时写（`docs/02-命令能力表.md` §5）
            cmd["capabilities"] = caps if ok_steps else []
            cmd["capabilities_evidence"] = ("behavior[] 每步均有汇编 VA" if ok_steps
                                            else "字段证据不全（有 ? VA），能力标签暂不写")
            cmd["db_effects"] = effs
            cmd["db_effects_note"] = db_note
            cmd["db_effects_sources"] = sorted({r.get("source") for r in (ev.get(cmd["id"]) or [])
                                                if r.get("source")})
            if "asm_verification" not in cmd:
                cmd["asm_verification"] = {"status": status, "checks": {}, "mismatches": []}
            cmd["asm_verification"]["status"] = status
            dump_json(p, cmd)
            updated.append(cmd)

    print("[derive] 命令 %d 条：behavior %d，step 全带 VA %d，有 db_effects %d，行为就绪 %d，"
          "BEHAVIOR-DONE %d"
          % (stat["命令"], stat["有 behavior"], stat["step 全带 VA"],
             stat["有 db_effects"], stat["行为就绪"], stat["BEHAVIOR-DONE"]))
    print("[derive] step 类别分布：%s" % dict(step_stat.most_common()))
    if not args.write:
        print("[derive] 试运行（未写文件）；加 --write 落库")
    elif updated:
        update_index(updated)
    return 0


def update_index(updated: list[dict]) -> None:
    idx_path = CMD_DIR / "index.json"
    if not idx_path.is_file():
        return
    index = load_json(idx_path)
    by_id = {c["id"]: c for c in index.get("commands", [])}
    for c in updated:
        e = by_id.get(c["id"])
        if e is None:
            continue
        e["status"] = (c.get("asm_verification") or {}).get("status", e.get("status"))
        e["behavior_steps"] = len(c.get("behavior") or [])
        e["capabilities"] = c.get("capabilities") or []
        e["capabilities_derived"] = c.get("capabilities_derived") or []
        e["capability_evidence"] = c.get("capabilities_evidence")
        e["db_effects"] = len(c.get("db_effects") or [])
        e["db_effects_note"] = c.get("db_effects_note")
    by_status = Counter(c.get("status", "IMPORTED") for c in index.get("commands", []))
    index.setdefault("counts", {})["by_status"] = dict(by_status)
    index["counts"]["behavior_done"] = by_status.get("BEHAVIOR-DONE", 0)
    index["counts"]["commands_with_db_effects"] = sum(
        1 for c in index.get("commands", []) if c.get("db_effects"))
    index["counts"]["commands_with_capabilities"] = sum(
        1 for c in index.get("commands", []) if c.get("capabilities"))
    by_cap = Counter()
    for c in index.get("commands", []):
        for t in c.get("capabilities") or c.get("capabilities_derived") or []:
            by_cap[t] += 1
    index["counts"]["by_capability"] = dict(by_cap.most_common())
    index["counts"]["by_capability_scope"] = "capabilities（证据齐全）优先，否则 capabilities_derived"
    index["behavior_derived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dump_json(idx_path, index)


if __name__ == "__main__":
    raise SystemExit(main())

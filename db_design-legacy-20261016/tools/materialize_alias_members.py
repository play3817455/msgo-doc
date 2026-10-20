#!/usr/bin/env python3
"""把「别名壳」composite 的成员摊平落盘（`members: []` + `layout_same_as` / `prefix_of` → 实成员）。

为什么需要这一步：`build_site.py` 渲染时会沿别名展开成员，**页面上看着是齐的**，
但 `composites/<id>.json` 本身是空的 —— 谁读 JSON（代码生成、建库、跨表对齐）都会
撞上一句「见 lpcard」，这正是「结构体必须就地摊平成员、不写见 XXX」要禁掉的形态。
本工具把基座成员**深拷贝**进来，并保留别名键作**出处与漂移检测**：

- `layout_same_as` → 成员逐个同基座（同读取器 = 同线体，见 `asm_audit.reader`）；
- `prefix_of` + `prefix_length` → 取基座成员的前缀，**累计线长必须恰好等于** `prefix_length`，
  否则报错不改（宁可留空壳，也不猜半截成员）。

可重复执行：已有成员的 composite 一律跳过（手写成员永远优先）。
`--check` 只报告漂移（落盘成员与基座不一致、或该摊平却还是空的），不写文件。

同一把尺子也量**别名实体**（`entities/*.json`）
================================================
实体里的别名壳（`alias_of` + `wire_forms[].prefix_of`，如 `ms_lounge`）**不该自带成员清单**：
唯一出处同样是 `composites/<id>.json`，站点 `build_entity_detail` 对空 `fields` 会就地摊平。
所以这里的判据是「别名实体的 `fields` 必须为空」（若手写非空，则必须与 composite 摊平结果一致，
否则报漂移）。反面教材：`generate_all.py` 的别名分支曾塞占位 blob，让
`entities/ms_lounge.json` 顶着 `fields: [TBD 303B, TBD 312B]`，既挡住摊平回退、又让
`check_meanings.py` 报「语义名待定」。
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSITES = ROOT / "schema" / "composites"
ENTITIES = ROOT / "schema" / "entities"
REPORT = ROOT / "schema" / "_meta" / "composite_materialize_report.json"


def load_all() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(COMPOSITES.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[warn] 读不了 {p.name}: {exc}", file=sys.stderr)
            continue
        out[d.get("id") or p.stem] = d
    return out


def named_members(comp: dict) -> list[dict]:
    return [m for m in (comp.get("members") or [])
            if m.get("name") and not str(m["name"]).startswith("_")]


def member_wire_len(m: dict) -> int | None:
    """成员的线长：多数是整数列；数组/嵌套带条数的由 `length_expr` 或 `count_field` 决定。"""
    raw = m.get("length")
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str) and raw.strip().isdigit():
        return int(raw.strip())
    return None


def prefix_members(base: dict, want: int) -> tuple[list[dict] | None, str]:
    """按累计线长截取基座成员，要求**恰好**落在 `want` 字节边界上。"""
    acc = 0
    out: list[dict] = []
    for m in named_members(base):
        ln = member_wire_len(m)
        if ln is None:
            return None, f"成员 `{m.get('name')}` 线长不是字面量（{m.get('length')!r}），无法按前缀截取"
        if acc + ln > want:
            return None, f"累计到 `{m.get('name')}` 时会越过 {want}B（{acc}+{ln}），没有恰好边界"
        acc += ln
        out.append(m)
        if acc == want:
            return out, "ok"
    return None, f"基座成员累计只有 {acc}B，不足 {want}B"


def materialize(comp: dict, base_id: str, bases: dict[str, dict], today: str) -> tuple[list[dict] | None, str, str]:
    base = bases.get(base_id)
    if base is None:
        return None, "base_missing", f"基座 `{base_id}` 不存在"
    if not named_members(base):
        return None, "base_empty", f"基座 `{base_id}` 自己也没有命名成员"
    if comp.get("prefix_of"):
        want = comp.get("prefix_length")
        if not isinstance(want, int):
            return None, "prefix_length_missing", "`prefix_of` 但没写 `prefix_length`"
        members, why = prefix_members(base, want)
        if members is None:
            return None, "prefix_not_on_boundary", why
        return members, "prefix", f"取 `{base_id}` 前 {want}B"
    return copy.deepcopy(named_members(base)), "layout", f"整份同 `{base_id}`"


def check_alias_entities(comps: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    """别名实体的 `fields` 漂移检查（判据见模块说明末尾）。

    返回 `(ok, drift)`：`ok` 是「按口径留空 / 与 composite 摊平结果一致」的实体，
    `drift` 是自带一份**另一份**成员清单的实体。
    """
    ok: list[dict] = []
    drift: list[dict] = []
    if not ENTITIES.is_dir():
        return ok, drift
    for path in sorted(ENTITIES.glob("*.json")):
        try:
            ent = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        eid = ent.get("id") or path.stem
        wfs = ent.get("wire_forms") or []
        alias = ent.get("alias_of") or next(
            (w.get("prefix_of") for w in wfs if w.get("prefix_of")), "")
        if not alias or alias == eid:
            continue
        fields = [f for f in (ent.get("fields") or [])
                  if f.get("name") and not str(f["name"]).startswith("_")]
        if not fields:
            ok.append({"id": eid, "alias": alias, "note": "fields 留空（成员由 composite 就地摊平）"})
            continue
        # 手写非空：允许，但必须与 composite 的摊平结果**逐名一致**。
        comp = comps.get(eid) or {}
        want = named_members(comp)
        if not want:
            want = prefix_members(comps.get(alias) or {}, int(ent.get("length") or 0))[0] or []
        have_names = [f["name"] for f in fields]
        want_names = [m.get("name") for m in want]
        if want_names and have_names == want_names:
            ok.append({"id": eid, "alias": alias, "note": f"手写 {len(fields)} 员与 composite 一致"})
        else:
            drift.append({
                "id": eid, "alias": alias, "kind": "entity",
                "note": (f"别名实体自带 {len(fields)} 员成员清单，与 composite 摊平结果不符"
                         f"（应留空 `fields: []`，成员只在 composites/<id>.json 一处维护）"),
            })
    return ok, drift


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只报告，不写文件")
    args = ap.parse_args()

    comps = load_all()
    today = date.today().isoformat()
    done: list[dict] = []
    skipped: list[dict] = []
    drift: list[dict] = []

    for cid in sorted(comps):
        comp = comps[cid]
        have = named_members(comp)
        alias = comp.get("layout_same_as") or comp.get("prefix_of") or comp.get("_audit_members_from")
        if not alias or alias == cid:
            continue
        if have:
            base = comps.get(alias)
            if alias in comps and named_members(base) and have != named_members(base) and comp.get("prefix_of") is None:
                drift.append({"id": cid, "alias": alias, "note": "落盘成员与基座不一致（基座改过了？）"})
            continue
        if comp.get("retraction") or str(comp.get("status", "")).lower() == "retracted":
            skipped.append({"id": cid, "reason": "已作废（retraction），不摊平已证伪的布局"})
            continue

        members, kind, why = materialize(comp, alias, comps, today)
        if members is None:
            skipped.append({"id": cid, "reason": f"{kind}: {why}"})
            continue

        if args.check:
            done.append({"id": cid, "alias": alias, "kind": kind, "members": len(members), "note": why})
            continue

        comp["members"] = members
        comp["members_source"] = f"alias:{kind}:{alias}"
        comp["members_materialized_at"] = today
        comp["members_materialized_note"] = (
            f"{why}；成员已就地摊平（口径：结构体不写「见 XXX」）。"
            "别名键保留作出处：基座改了要重跑本工具 --check 对漂移。"
        )
        path = COMPOSITES / f"{cid}.json"
        path.write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        done.append({"id": cid, "alias": alias, "kind": kind, "members": len(members), "note": why})

    ent_ok, ent_drift = check_alias_entities(comps)
    drift.extend(ent_drift)

    total = sum(d["members"] for d in done)
    print(f"[materialize] 摊平 {len(done)} 份（共 {total} 条成员）；跳过 {len(skipped)}；漂移 {len(drift)}")
    print(f"[materialize] 别名实体 {len(ent_ok) + len(ent_drift)} 个："
          f"{len(ent_ok)} 个合规（fields 留空或与 composite 一致）、{len(ent_drift)} 个漂移")
    for d in done:
        print(f"  + {d['id']:<26} ← {d['alias']:<22} {d['kind']:<6} {d['members']} 成员")
    for s in skipped:
        print(f"  - {s['id']:<26} {s['reason']}")
    for d in ent_ok:
        print(f"  = {d['id']:<26} {d['note']}")
    for s in drift:
        print(f"  ! {s['id']:<26} {s['note']}")

    if not args.check:
        REPORT.write_text(json.dumps({
            "generated": today,
            "materialized": done,
            "skipped": skipped,
            "alias_entities_ok": ent_ok,
            "drift": drift,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

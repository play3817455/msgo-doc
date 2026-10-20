#!/usr/bin/env python3
"""归位复核（批次化）——把 `homing/unresolved.md` 切成可人工判的批，并校验裁决。

纪律（仿 `verify_commands_ida.py`）
====================================
  1. 引擎判不了的一律进 unresolved；**人工只判 unresolved**，不改字节模型。
  2. 裁决写进 `schema/homing/_overrides.json`（人工产物，derive_homing 不清它）。
  3. 每批判完必须 `--check` 全绿再进下一批；`--status` 看进度。
  4. 裁决里的名字拼错必须报错（不许静默忽略）。

`_overrides.json` 形态
======================
  {
    "note": "…",
    "fold":  [{"composites": ["favms","favms_add"], "as": "favms"}],
    "pk":    {"buildup_info": ["uniq_msid"]},
    "role":  {"item.item_id": "attribute"},
    "fk":    {"pcard.channel_id": "channel.channelid"},
    "ignore":{"obj.field": "战斗态快照字段，不落库（B6）"}
  }

用法
====
  python tools/review_homing.py --status          # 进度与各批规模
  python tools/review_homing.py --batch 1         # 生成第 1 批待判清单
  python tools/review_homing.py --check           # 校验 _overrides.json
  python tools/review_homing.py --verify          # 复核器：重跑并对账
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCHEMA = TOOLS.parent / "schema"
HOMING = SCHEMA / "homing"

_spec = importlib.util.spec_from_file_location("derive_homing", TOOLS / "derive_homing.py")
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)

# 复核批次的主题与规模（每批一个主题，避免人工在一堆异质项之间来回切）
BATCH_THEMES = (
    ("pk", "根对象无行键：判定对象自己的记录号（或确认只能 (world_id,pilot_id) 单行）"),
    ("fold", "同形线布局未折叠：判定是否同一业务对象"),
    ("ref", "引用未解析：判定 FK 目标或登记为不落库"),
    ("tbd", "生命周期 TBD 成员：判定 PERSIST 还是 EVENT"),
    ("evidence", "有定位但无地址级 VA：补 VA 或接受按 evidence_ref 追溯"),
    ("legacy", "与旧库 UNIQUE 对账不一致：确认新键是改进（旧库压行）还是回归（会丢行）"),
)


def load_overrides() -> dict:
    return D.load_overrides()


def legacy_diff(objects: dict) -> list[dict]:
    """新自然键 vs **冻结的**旧库 UNIQUE 的对账差异（复用 reconcile_legacy_ddl 的口径）。

    以前这里连旧库（psql）现查；旧库删掉后改读 `schema/_meta/legacy_evidence.json`。
    顺带修掉一个隐性失效：`game` schema 已被 P4 洗成新表之后，连库查到的「旧 UNIQUE」
    其实是新表的索引，对账会**恒等于 0 差异**——看着绿，什么都没比。
    """
    spec = importlib.util.spec_from_file_location(
        "reconcile_legacy_ddl", TOOLS / "reconcile_legacy_ddl.py")
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    old = R.legacy_unique_frozen()
    out = []
    for o in sorted(objects.values(), key=lambda x: x["id"]):
        if o.get("disposition") != "PERSIST" or not o.get("is_root"):
            continue
        lt = (o.get("legacy_table") or "").removeprefix("tbl_")
        if not lt or lt not in old:
            continue
        col_of = {c["member"]: c["column"] for c in o.get("columns") or []}
        new_pk = [col_of.get(c, c) for c in o["keys"]["primary_key"]]
        if new_pk in old[lt]:
            continue
        out.append({"object": o["id"], "legacy": lt, "new_pk": new_pk,
                    "old_unique": old[lt], "kind": o["keys"]["pk_kind"]})
    return out


def theme_items(objects: dict, cov: dict, metrics: dict) -> dict[str, list]:
    """把未决项按主题切成批。"""
    pk = []
    for oid in cov["roots_without_pk"]:
        o = objects[oid]
        cand = [x["name"] for x in o["members"]
                if x["role"] in ("ref", "identity", "attribute")
                and D.norm(x["name"]).endswith("id")]
        pk.append({"object": oid, "members": len(o["members"]),
                   "candidates": cand[:8],
                   "folded": o["folded_composites"]})
    fold = [{"composites": grp} for grp in (metrics.get("twins") or [])]
    ref = metrics.get("ref_notes") or []
    tbd = [{"object": oid, "field": x["name"], "wire_type": x["wire_type"],
            "views": x["views"]}
           for oid, o in objects.items() for x in o["members"]
           if x["lifetime"] == "TBD"]
    evidence = collections.Counter(
        oid for oid, o in objects.items() for x in o["members"]
        if not x.get("evidence_va") and x.get("evidence_ref"))
    ev = [{"object": k, "count": v} for k, v in evidence.most_common()]
    return {"pk": pk, "fold": fold, "ref": ref, "tbd": tbd, "evidence": ev,
            "legacy": legacy_diff(objects)}


def write_batch(theme: str, items: list, path: Path) -> None:
    title = dict(BATCH_THEMES).get(theme, theme)
    L = [f"# 归位复核批次 · {theme}", "", f"> {title}", "",
         f"待判 **{len(items)}** 项。裁决写回 `schema/homing/_overrides.json`，"
         "然后 `python tools/review_homing.py --check`。", ""]
    if theme == "pk":
        L += ["| 对象 | 成员数 | 候选身份成员 | 折入线布局 |", "|---|---|---|---|"]
        for it in items:
            L.append(f"| `{it['object']}` | {it['members']} | "
                     f"{', '.join('`'+c+'`' for c in it['candidates']) or '-'} | "
                     f"{', '.join(it['folded'])} |")
        L += ["", "裁决写法：`\"pk\": {\"<对象>\": [\"<成员>\"]}`；"
                  "确认只能单行则写 `\"pk\": {\"<对象>\": []}` 并在 `note` 里说明。"]
    elif theme == "fold":
        L += ["| 同形组 |", "|---|"]
        for it in items:
            L.append(f"| {', '.join('`'+c+'`' for c in it['composites'])} |")
        L += ["", "裁决写法：`\"fold\": [{\"composites\": [\"a\",\"b\"], \"as\": \"a\"}]`"]
    elif theme == "ref":
        L += ["| 对象 | 字段 | 原因 | 证据 VA |", "|---|---|---|---|"]
        for it in items:
            L.append(f"| `{it['object']}` | `{it['field']}` | {it['reason']} | "
                     f"`{it['evidence_va']}` |")
        L += ["", "裁决写法：`\"fk\": {\"<对象>.<字段>\": \"<对象>.<列>\"}`，"
                  "或 `\"ignore\": {\"<对象>.<字段>\": \"<理由>\"}` 登记不落库。"]
    elif theme == "tbd":
        L += ["| 对象 | 字段 | 线类型 | 线视图 |", "|---|---|---|---|"]
        for it in items:
            L.append(f"| `{it['object']}` | `{it['field']}` | `{it['wire_type']}` | "
                     f"{', '.join(it['views'])} |")
        L += ["", "裁决写法：`\"ignore\": {\"<对象>.<字段>\": \"<理由>\"}`（不落库），"
                  "或改 `catalog` 里的 disposition 后重跑。"]
    elif theme == "legacy":
        L += ["| 对象 | 旧表 | 新 PK | 旧 UNIQUE | 依据 |",
              "|---|---|---|---|---|"]
        for it in items:
            L.append(f"| `{it['object']}` | {it['legacy']} | "
                     f"{'+'.join(it['new_pk'])} | "
                     f"{'; '.join('+'.join(x) for x in it['old_unique'])} | "
                     f"{it['kind']} |")
        L += ["",
              "判法：",
              "* **新键比旧键细**（新多一列）→ 多半是新模型更准，旧库把多行压成了一行；"
              "确认后可放行，并在 `note` 里记「旧库压行」。",
              "* **新键比旧键粗**（旧多 `+slot`）→ **危险**：新模型会把多行 upsert 成一行。"
              "要判定旧 `slot` 的业务含义（是数组下标，还是「卡片所属机师」这类被丢掉的维度），"
              "再决定补成员、还是走 `pk` 订正。",
              "* 裁决写法：`\"pk\": {\"<对象>\": [\"<成员>\", ...]}`。"]
    else:
        L += ["| 对象 | 无 VA 成员数 |", "|---|---|"]
        for it in items:
            L.append(f"| `{it['object']}` | {it['count']} |")
        L += ["", "口径：这批不阻塞归位（有 `evidence_ref` 可追溯），"
                  "要严格满足「指回 VA」就得回 IDA 补地址（走 verify 批次）。"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def cmd_status(objects: dict, cov: dict, metrics: dict, items: dict) -> int:
    ov = load_overrides()
    reviewed = ov.get("reviewed") or {}
    print("批次进度")
    for theme, desc in BATCH_THEMES:
        n = len(items.get(theme) or [])
        adj = reviewed.get(f"batch_{BATCH_THEMES.index((theme, desc)) + 1:02d}_{theme}") \
            or reviewed.get(f"batch_{[t for t, _ in BATCH_THEMES].index(theme) + 1:02d}_{theme}")
        state = "完成" if n == 0 else f"待判 {n}"
        mark = f"  [已裁决：{adj['verdict']}]" if adj else ""
        print(f"  {theme:<10} {state:<12} {desc}{mark}")
    print()
    print(f"_overrides.json : fold={len(ov.get('fold') or [])} "
          f"pk={len(ov.get('pk') or {})} role={len(ov.get('role') or {})} "
          f"fk={len(ov.get('fk') or {})} ignore={len(ov.get('ignore') or {})} "
          f"colname={len(ov.get('colname') or {})}")
    if reviewed:
        print(f"  已裁决批次 {len([k for k in reviewed if k.startswith('batch')])}/"
              f"{len(BATCH_THEMES)}（明细见 _overrides.json 的 reviewed 段）")
    return 0


def cmd_check(objects: dict) -> int:
    """校验 _overrides.json：名字必须存在，目标必须可解析。"""
    ov = load_overrides()
    problems: list[str] = []

    for grp in ov.get("fold") or []:
        for c in grp.get("composites") or []:
            if c not in D.Model().composites:
                problems.append(f"fold: 复合体 {c!r} 不存在")
    for name, spec in (ov.get("pk") or {}).items():
        o = objects.get(name)
        if o is None:
            problems.append(f"pk: 对象 {name!r} 不存在")
            continue
        mem = {x["name"] for x in o["members"]}
        for c in spec or []:
            if c not in mem:
                problems.append(f"pk: {name}.{c} 不是本对象成员")
    for key in list(ov.get("role") or {}) + list(ov.get("fk") or {}) \
            + list(ov.get("ignore") or {}) + list(ov.get("colname") or {}):
        x, _ = D._find_member(objects, key)
        if x is None:
            problems.append(f"成员 {key!r} 不存在")
    for key, tgt in (ov.get("fk") or {}).items():
        oname, _, col = str(tgt).rpartition(".")
        if oname.startswith("core.") or oname.startswith("srv."):
            continue
        to = objects.get(oname)
        if to is None:
            problems.append(f"fk: 目标对象 {oname!r} 不存在（{key}）")
        elif col and not any(x["name"] == col or D._snake(x["name"]) == col
                             for x in to["members"]):
            problems.append(f"fk: 目标列 {tgt!r} 在 {oname} 里不存在（{key}）")

    if problems:
        print(f"FAIL  {len(problems)} 处问题：")
        for p in problems:
            print("  -", p)
        return 1
    print("OK  _overrides.json 全部可解析")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--batch", type=int, help="生成第 N 批待判清单")
    ap.add_argument("--check", action="store_true", help="校验 _overrides.json")
    ap.add_argument("--verify", action="store_true", help="重跑引擎并对账")
    args = ap.parse_args()

    m = D.Model()
    objects, _u, metrics = D.build(m)
    cov = D.coverage(objects)
    items = theme_items(objects, cov, metrics)

    if args.batch:
        idx = args.batch - 1
        if not (0 <= idx < len(BATCH_THEMES)):
            print(f"批次号超出范围（1..{len(BATCH_THEMES)}）")
            return 2
        theme = BATCH_THEMES[idx][0]
        out = HOMING / "_meta"
        out.mkdir(parents=True, exist_ok=True)
        p = out / f"batch_{args.batch:02d}.md"
        write_batch(theme, items.get(theme) or [], p)
        print(f"已写出 {p}（{len(items.get(theme) or [])} 项）")
        return 0
    if args.check:
        return cmd_check(objects)
    if args.verify:
        r, d, mref, rref, cref = D.resolve_relations(objects)
        print(f"对象 {len(objects)}  关联 {len(r)}  悬空 {len(d)}  "
              f"主数据 {len(mref)}  战斗句柄 {len(rref)}  模型外 {len(cref)}")
        print(f"未决引用 {len(metrics.get('ref_notes') or [])}  "
              f"无 PK 根对象 {len(cov['roots_without_pk'])}  "
              f"同形未折叠 {len(metrics.get('twins') or [])}")
        for n in metrics.get("override_notes") or []:
            print("  订正问题:", n)
        for n in metrics.get("writers_notes") or []:
            print("  写方登记问题:", n)
        return 0
    return cmd_status(objects, cov, metrics, items)


if __name__ == "__main__":
    sys.exit(main())

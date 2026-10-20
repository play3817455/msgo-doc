#!/usr/bin/env python3
"""归位常驻守卫——`homing/` 的结构完整性（可进 CI / pre-commit）。

盯的是「静默退化」：重跑引擎或改字节模型后，归位结果不能悄悄变差。
比 `review_homing.py` 更硬：只报**不变量**，不做任何人工口径判断。

检查项
======
  1. `homing/` 五个产物齐全（fields.jsonl / objects/ / relations.json /
     roles.json / unresolved.md / summary.json）
  2. 132 个复合体全部折入对象（不许有没归位的线布局）
  3. 每个对象的每个成员都有 `evidence_va` 或 `evidence_ref`（不许无出处）
  4. `role` 只能取闭集；`lifetime` 只能取 PERSIST/EVENT/TBD/COMPOSITE
  5. 每条 relation 的 `to` 都解析到已存在对象（悬空只许出现在 dangling）
  6. `_overrides.json` 可解析、名字都在（等价于 review --check）
  7. fields.jsonl 每行有 object/field/role；落库行必须有 table+column
  8. 根不变量：`game.*` 表名唯一；PERSIST 根对象都有行键或作用域列
  9. 列宽装得下每一条线形（`wire_variants` 里没有比列宽更宽的线形）
 10. 实体声明的线长 == 复合体自算线长
 11. 主数据引用目标真的存在（cfg./srv. 表名与列名逐字校验）
 12. 每条引用都有归宿（fk_target 或 ref_kind ∈ 闭集）
 13. `singleton` 裁决必须被冻结的旧库证据支持（`_meta/legacy_evidence.json`）
 14. 发方表面完整：`_meta/ida_send_names.txt`（客户端发方全集）↔ `commands/` 的 CS 命令集
     **一一对应**——「0 个 CS 写方」这类否定断言的地基（docs/05 §9.7）
 15. 成员行归根表（`_overrides.json.member_rows_in_root`）：子表副本真退场、父表记视图
     链接、目标对象有根表——同一批行不许建两张表（docs/05 §4.G#4）
 16. 关系分桶：`relations[]` 只收**建表源**的边，`wire_refs[]` 只收不建表源的边，两桶之和 == 边数
 17. 退役表登记（`retire_tables`）：每条有 verdict + evidence，且**不得**再出现在任何 `tables[]` 里
 18. 同形孪生逐组裁决（`twin_verdicts`）：`keep` 的组必须仍在引擎的孪生清单里、
     `fold` 的组必须真折进一个对象且登记在 `fold` 段——「判过了」不能变成「按错了」

用法
====
  python tools/_survey_homing.py            # 人类可读
  python tools/_survey_homing.py --quiet    # 只在失败时输出（CI）
"""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SCHEMA = TOOLS.parent / "schema"
HOMING = SCHEMA / "homing"

_spec = importlib.util.spec_from_file_location("derive_homing", TOOLS / "derive_homing.py")
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)

REQUIRED = ("fields.jsonl", "relations.json", "roles.json", "unresolved.md",
            "summary.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    # Windows 控制台/管道默认按 GBK 编码 stdout：本脚本的输出里有 `↔`（U+2194）这类
    # GBK 编不出的符号，不重设就会在**打印成功信息**时抛 UnicodeEncodeError——
    # 检查明明全过了，退出码却是 1。重设成 UTF-8 并允许替换，别让显示层绑架门禁。
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    fails: list[str] = []
    warns: list[str] = []

    for name in REQUIRED:
        if not (HOMING / name).is_file():
            fails.append(f"缺产物 {name}")
    if not (HOMING / "objects").is_dir():
        fails.append("缺 homing/objects/ 目录")
    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        return 1

    m = D.Model()
    objects, _u, metrics = D.build(m)
    cov = D.coverage(objects)
    relations = json.loads((HOMING / "relations.json").read_text(encoding="utf-8"))
    summary = json.loads((HOMING / "summary.json").read_text(encoding="utf-8"))

    # 2. 复合体全覆盖
    if cov["composites_missing"]:
        fails.append(f"未归位的复合体 {len(cov['composites_missing'])} 个："
                     f"{cov['composites_missing'][:8]}")

    # 3. 每个成员都有出处（已知缺口单列，不算失职）
    no_ev = [(oid, x["name"]) for oid, o in objects.items() for x in o["members"]
             if not x.get("evidence_va") and not x.get("evidence_ref")
             and not x.get("known_gap")]
    known_gap = [(oid, x["name"], x.get("gap_reason"))
                 for oid, o in objects.items() for x in o["members"]
                 if not x.get("evidence_va") and not x.get("evidence_ref")
                 and x.get("known_gap")]
    if no_ev:
        fails.append(f"无任何出处且非已知缺口的成员 {len(no_ev)} 个：{no_ev[:8]}")

    # 4. 词表闭集
    bad_role = sorted({x["role"] for o in objects.values() for x in o["members"]}
                      - set(D.ROLES))
    if bad_role:
        fails.append(f"未知 role：{bad_role}")
    bad_life = sorted({x["lifetime"] for o in objects.values() for x in o["members"]}
                      - {"PERSIST", "EVENT", "TBD", "COMPOSITE"})
    if bad_life:
        fails.append(f"未知 lifetime：{bad_life}")

    # 5. relation 目标必须存在
    dangling_to = [r["to"] for r in relations["relations"]
                   if not _resolvable(r["to"], objects)]
    if dangling_to:
        fails.append(f"relation 指向不存在的目标 {len(dangling_to)} 条："
                     f"{dangling_to[:6]}")

    # 6. overrides 可解析
    ov = D.load_overrides()
    if ov:
        problems = []
        for name, spec in (ov.get("pk") or {}).items():
            o = objects.get(name)
            if o is None:
                problems.append(f"pk:{name}")
            else:
                mem = {x["name"] for x in o["members"]}
                problems += [f"pk:{name}.{c}" for c in spec or [] if c not in mem]
        for key in list(ov.get("role") or {}) + list(ov.get("fk") or {}) \
                + list(ov.get("ignore") or {}) + list(ov.get("colname") or {}):
            if D._find_member(objects, key)[0] is None:
                problems.append(key)
        if problems:
            fails.append(f"_overrides.json 名字无效 {len(problems)} 处：{problems[:6]}")

    # 7. fields.jsonl 形状
    n_rows = 0
    for ln, line in enumerate(
            (HOMING / "fields.jsonl").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        n_rows += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            fails.append(f"fields.jsonl 第 {ln} 行不是 JSON")
            continue
        for k in ("object", "field", "role"):
            if not row.get(k):
                fails.append(f"fields.jsonl 第 {ln} 行缺 {k}")
        if row.get("table") and not row.get("column"):
            fails.append(f"fields.jsonl 第 {ln} 行有 table 无 column")

    # 8. 表名唯一 + 非根表形态正确
    #    每个对象可投影多张表（`nested` 每个父一张，§4.F），所以按 `tables[]` 收名。
    tabled = [o for o in objects.values()
              if o.get("is_root") and o["disposition"] == "PERSIST"]
    names: list[str] = []
    for o in tabled:
        ts = o.get("tables") or ([{"name": o["table"]}] if o.get("table") else [])
        if not ts:
            fails.append(f"PERSIST 根对象没有表名：{o['id']}")
        for t in ts:
            if not t.get("name"):
                fails.append(f"对象 {o['id']} 的表缺名")
            else:
                names.append(t["name"])
    tables = collections.Counter(names)
    dup = [t for t, n in tables.items() if n > 1]
    if dup:
        fails.append(f"表名冲突：{dup}")

    # 9. 列宽必须装得下每一条线形（`wire_variants` 是跨线形宽度差异）
    #    DDL 的列宽跟落库线体（`wire_body`）走；若另一条线形比它更宽，那一列就会
    #    截断（`ms_rokaku.is_costover` 的 battle 视图 u8 与机库视图 char[2] 就是这
    #    一类）。成员宽度由 `resolve_member_widths` 定到落库线体，所以这里等于
    #    在问「落库线体是不是最宽的那条」。
    narrow = []
    for oid, o in objects.items():
        if o.get("disposition") != "PERSIST":
            continue
        for x in o["members"]:
            variants = list((x.get("wire_variants") or {}).values())
            worst = max((v.get("length") or 0) for v in variants) if variants else 0
            if worst > (x.get("length") or 0):
                narrow.append(f"{oid}.{x['name']}（列 {x.get('length')}B < "
                              f"线形 {worst}B，落库线体 {o.get('wire_body') or '-'}）")
    if narrow:
        fails.append(
            f"{len(narrow)} 个成员的列宽装不下另一条线形：{narrow[:6]}"
            "（要按最宽线形重建列，或改锚点声明的落库线体）")

    # 10. 实体声明的线长 == 复合体自算线长
    #     `entities/*.json` 的 `wire_forms[].length` 是**冗余抄写**：真正的线长由
    #     `composites/*.json` 从成员偏移实算（IDA 展开 + 逐字段核对）。抄写会陈旧，
    #     而且陈旧得很安静——`entities/ms.json` 的 lounge 线形一直写着 299，
    #     而复合体早已按整函数展开纠正为 303（299 的作废理由就在 ms.json 的 note 里）。
    #     线长是 DDL 列宽与「槽 vs 线」判据的输入，抄错一位就会让下游按错宽度解析，
    #     所以这里把两者钉在一起。
    comps = _load_composites()
    stale = []
    for e in sorted((SCHEMA / "entities").glob("*.json")):
        doc = json.loads(e.read_text(encoding="utf-8"))
        forms = doc.get("wire_forms") or []
        for form in forms:
            cid, how = _form_composite(e.stem, len(forms), form, comps)
            if not cid:
                continue
            want = comps[cid].get("length")
            got = form.get("length")
            if want and got != want:
                stale.append(f"{e.stem}.{form.get('name')} 写 {got}B，"
                             f"复合体 {cid} 实算 {want}B（按 {how} 配对）")
    if stale:
        fails.append(f"{len(stale)} 条实体线长与复合体不符：{stale[:6]}"
                     "（实体只是抄写，以 composites/ 为准）")

    # 11. 主数据引用目标必须真的存在（cfg./srv. 表名与列名逐字校验）
    #     master_refs 是「值域指向」，不建 FK 约束，但**必须**指向真实的表列——
    #     否则站点上会写出一条查不到的引用，比不写还糟。`npc`/`arms` 这类键名不符的
    #     情形一律留在 dangling（带候选），不许写进 master_target。
    bad_master = []
    tables = _master_tables()
    for oid, o in objects.items():
        for x in o["members"]:
            if (x.get("ref_kind") or "") != "master":
                continue
            tgt = x.get("master_target") or ""
            schema, _, rest = tgt.partition(".")
            tid, _, col = rest.rpartition(".")
            cols = tables.get((schema, tid))
            if not tgt or schema not in ("cfg", "srv") or cols is None:
                bad_master.append(f"{oid}.{x['name']} → {tgt!r}（无此表）")
            elif col and col not in cols:
                bad_master.append(f"{oid}.{x['name']} → {tgt!r}（表内无此列）")
    if bad_master:
        fails.append(f"{len(bad_master)} 条主数据目标不存在：{bad_master[:6]}")

    # 12. 每条引用都必须有归宿：fk_target，或 ref_kind ∈ 闭集
    #     `none` 就是「引擎判不了」——它必须为空，否则未决清单又有内容了。
    orphan = [f"{oid}.{x['name']}" for oid, o in objects.items() for x in o["members"]
              if x.get("role") == "ref" and not x.get("fk_target")
              and (x.get("ref_kind") or "") not in
              ("master", "runtime", "self", "notref", "dangling")]
    if orphan:
        fails.append(f"{len(orphan)} 条引用没有归宿（未归类）：{orphan[:8]}")

    # 13. `singleton` 裁决必须被冻结的旧库证据支持（docs/05 §9.4）
    #     「每个作用域一行」这句话的依据原本只在旧库的 `uq_game_<t>_world_pilot (world_id,pilot_id)`
    #     里。旧库删了之后依据只剩 `schema/_meta/legacy_evidence.json`，所以这里把每条裁决
    #     **重新对一遍快照**：要么旧库确有 (world_id,pilot_id) 唯一键（逐列一致），要么是
    #     (world_id,pilot_id,slot) 而 slot 是合成列，要么旧库根本没这张表（裁决文本须写明）。
    #     没有这一门，改 DDL 键形状时没人会发现 `singleton` 的理由已经站不住。
    ev_path = SCHEMA / "_meta" / "legacy_evidence.json"
    if not ev_path.is_file():
        fails.append("缺 schema/_meta/legacy_evidence.json（跑 python tools/freeze_legacy.py）")
    else:
        ev = json.loads(ev_path.read_text(encoding="utf-8")).get("tables") or {}
        ov = json.loads((HOMING / "_overrides.json").read_text(encoding="utf-8"))
        sing = {k: v for k, v in (ov.get("singleton") or {}).items()
                if not str(k).startswith("_")}
        counted = collections.Counter()
        for oid, why in sorted(sing.items()):
            o = objects.get(oid)
            if not o:
                fails.append(f"singleton 裁决 {oid}：没有这个对象")
                continue
            pk = (o.get("keys") or {}).get("primary_key") or []
            if o.get("disposition") != "PERSIST" or pk != ["world_id", "pilot_id"]:
                fails.append(f"singleton 裁决 {oid}：disposition={o.get('disposition')} "
                             f"主键={pk}，不是「作用域单行」形状")
                continue
            stem = str(o.get("legacy_table") or "").removeprefix("tbl_")
            if not stem:
                stem = next((t["name"].removeprefix("game.") for t in o.get("tables") or []
                             if t.get("shape") == "root"), "")
            node = ev.get(stem)
            if node is None:
                fails.append(f"singleton 裁决 {oid}：冻结证据里没有旧表 {stem!r}")
                continue
            live = node.get("live") or {}
            uqs = [i.get("columns") for i in live.get("unique_indexes") or []]
            if ["world_id", "pilot_id"] in uqs:
                counted["旧库单行键逐列一致"] += 1
            elif ["world_id", "pilot_id", "slot"] in uqs:
                counted["旧库多一列合成 slot"] += 1
            elif not live.get("exists"):
                if "旧库无此表" not in str(why) and "旧库没有此表" not in str(why):
                    fails.append(f"singleton 裁决 {oid}：旧库没有 game.{stem}，裁决文本里"
                                 f"必须写明「旧库无此表」并给出替代依据")
                else:
                    counted["旧库确无此表（文本已说明）"] += 1
            else:
                fails.append(f"singleton 裁决 {oid}：旧库 game.{stem} 的唯一键是 {uqs}，"
                             f"既不是 (world_id,pilot_id) 也不是 (world_id,pilot_id,slot)")
        if not args.quiet and not any(f.startswith("singleton") for f in fails):
            print(f"gate: singleton 证据 {len(sing)} 条全对得上快照 "
                  f"（{' · '.join(f'{k} {v}' for k, v in sorted(counted.items()))}）")

    # 14. 发方表面完整性（docs/05 §9.7「0 个 CS 写方」的地基）
    #     `_meta/ida_send_names.txt` 是客户端发方**全集**（IDA 扫断言串导出）。
    #     它与 `schema/commands` 的 CS 命令集必须**一一对应**：只要这条恒成立，
    #     「发方全集里没有它」就等于「这个实体没有写方」——否定断言才是可复核的。
    #     差在任何一侧都说明前提变了（漏建模一条写方 / 客户端版本换了），
    #     §9.7 的裁决与 `no_writer` 那一桶都要重新过一遍。
    send_path = SCHEMA / "_meta" / "ida_send_names.txt"
    if not send_path.is_file():
        fails.append("缺 schema/_meta/ida_send_names.txt（发方全集导出件，见 docs/05 §9.7）")
    else:
        ida_send = {l.strip() for l in send_path.read_text(encoding="utf-8").splitlines()
                    if l.strip() and not l.startswith("#")}
        model_cs = set()
        for p in (SCHEMA / "commands").glob("CS-*.json"):
            m = re.match(r"CS-(0x[0-9A-Fa-f]+)-(.+?)-(.+)\.json$", p.name)
            if not m:
                fails.append(f"CS 命令文件名解析不了：{p.name}")
                continue
            model_cs.add(m.group(3))
        only_ida = sorted(ida_send - model_cs)
        only_model = sorted(model_cs - ida_send)
        if only_ida:
            fails.append(f"{len(only_ida)} 条客户端发方没有建模的 CS 命令（漏了写命令？）："
                         f"{only_ida[:8]}")
        if only_model:
            fails.append(f"{len(only_model)} 条 CS 命令在客户端发方全集里找不到（名字不齐/已过期？）："
                         f"{only_model[:8]}")
        if not args.quiet and not only_ida and not only_model:
            print(f"gate: 发方表面 {len(ida_send)} 条 ↔ 已建模 CS {len(model_cs)} 条，一一对应")

    # 15. 「行在别人的根表里」（`_overrides.json.member_rows_in_root`，docs/05 §4.G#4）
    #     这一节裁决「同一批行只留一张表」：父对象里的数组格降为**视图**，行归目标对象
    #     的根表，子表副本退场。四条都不是文风问题，缺一条就会静默回到「两张表装同一批
    #     行」的老状态，所以逐条钉住：
    #       a) 父对象/成员/目标对象存在，且成员确实是指向目标的 `array` 链接；
    #       b) 目标对象**有根表**（行得真有地方落）；
    #       c) 要退场的那张子表在**所有**对象的 `tables[]` 里都不存在（真退了）；
    #       d) `retire_child_table` 在 `retire_tables` 里登记过（退场理由一处一份）；
    #       e) 父表确实记了 `view_rows` 视图链接（改写落到了投影上，不是只在裁决里）。
    ov_all = D.load_overrides()
    mr_specs = [s for s in (ov_all.get("member_rows_in_root") or [])
                if isinstance(s, dict)]
    if mr_specs:
        mr_bad: list[str] = []
        retired = D.retire_map(ov_all)
        all_tbl = {t.get("name") for o in objects.values() for t in o.get("tables") or []}
        for i, spec in enumerate(mr_specs):
            pid = str(spec.get("parent") or "")
            mem = str(spec.get("member") or "")
            oid = str(spec.get("object") or "")
            label = f"member_rows_in_root[{i}] {pid}.{mem}"
            p, child = objects.get(pid), objects.get(oid)
            if p is None or child is None:
                mr_bad.append(f"{label}: 父对象或目标对象不存在")
                continue
            mx = next((z for z in p["members"] if z["name"] == mem), None)
            if (mx is None or mx.get("link_kind") != "array"
                    or mx.get("element_composite_ref") != oid):
                mr_bad.append(f"{label}: 父对象没有「指向 {oid} 的数组成员」")
            if child.get("shape") != "root":
                mr_bad.append(f"{label}: 目标 {oid} 的形状是 {child.get('shape')}，"
                              "不是 root（行没有自己的表）")
            if not any(t.get("shape") == "root" for t in child.get("tables") or []):
                mr_bad.append(f"{label}: 目标 {oid} 没有根表")
            if not str(spec.get("reason") or "").strip():
                mr_bad.append(f"{label}: 缺 reason")
            if not str(spec.get("evidence_va") or "").strip():
                mr_bad.append(f"{label}: 缺 evidence_va（裁决必须有地址级出处）")
            ct = str(spec.get("retire_child_table") or "")
            if ct and ct not in retired:
                mr_bad.append(f"{label}: {ct} 没在 retire_tables 里登记")
            if ct and ct in all_tbl:
                mr_bad.append(f"{label}: 子表 {ct} 仍在某对象的 tables[] 里（没真退场）")
            want = f"game.{D._stem_of(child)}"
            vr = [v for v in p.get("view_rows") or []
                  if v.get("member") == mem and v.get("root_table") == want]
            if not vr:
                mr_bad.append(f"{label}: 父表没有指向 {want} 的 view_rows 视图链接")
        fails += mr_bad
        if not args.quiet and not mr_bad:
            print(f"gate: 成员行归根表 {len(mr_specs)} 条（子表已退场、父表记视图链接）")

    # 16. 关系分桶（docs/05 §9.9）：`relations[]` 只收**源对象建表**的边。
    #     `DERIVED`/`EVENT`/`CONFIG`/`TBD` 的对象没有表，它出向的引用仍在线体里成立、
    #     仍是证据，但**建不出外键**（库里没有源表）。混着放会让站点「外键」一栏里
    #     包含一批永远建不出的边（本批退役 35 张表后 59 条里有 29 条如此）。三条都钉：
    #       a) `relations[]` 的源对象必须 PERSIST；
    #       b) `wire_refs[]` 的源对象必须**非** PERSIST（否则它该回 relations[]）；
    #       c) 两桶之和 == 从成员推出来的边数（分桶不许丢边）。
    live_rel = relations.get("relations") or []
    wire_rel = relations.get("wire_refs") or []
    bucket_bad: list[str] = []
    for r in live_rel:
        src = str(r.get("from", "")).split(".")[0]
        o = objects.get(src)
        if o is None or o.get("disposition") != "PERSIST":
            bucket_bad.append(f"relations[] 里 {r.get('from')} 的源对象不建表"
                              f"（disposition={(o or {}).get('disposition') or '无此对象'}）")
    for r in wire_rel:
        src = str(r.get("source_object") or str(r.get("from", "")).split(".")[0])
        o = objects.get(src)
        if o is not None and o.get("disposition") == "PERSIST":
            bucket_bad.append(f"wire_refs[] 里 {r.get('from')} 的源对象建了表，"
                              "这条该留在 relations[]")
        if not str(r.get("reason") or "").strip():
            bucket_bad.append(f"wire_refs[] 里 {r.get('from')} 缺 reason（为什么不是外键）")
    want_edges = 0
    for o in objects.values():
        want_edges += len(o.get("declared_fks") or [])
        want_edges += sum(1 for x in o["members"]
                          if x.get("role") == "scope" or x.get("fk_target"))
    if want_edges != len(live_rel) + len(wire_rel):
        bucket_bad.append(f"关系分桶丢边：成员推出 {want_edges} 条，"
                          f"relations {len(live_rel)} + wire_refs {len(wire_rel)}")
    fails += bucket_bad
    if not args.quiet and not bucket_bad:
        print(f"gate: 关系分桶 {len(live_rel)} 建表源 + {len(wire_rel)} 不建表源 "
              f"= {want_edges} 条边（一条不丢）")

    # 17. 退役表登记（`_overrides.json.retire_tables`）：允许退役的唯一入口，
    #     所以每条都要有 `verdict` 与 `evidence`（地址级出处），并且**不得**再出现在
    #     任何对象的 `tables[]` 里——退役之后又被守恒段/链接段悄悄建回来，是这里
    #     唯一要防的失效模式（`unlockw` 踩过：同一批行两张表）。
    retire_rows = [r for r in (ov_all.get("retire_tables") or []) if isinstance(r, dict)]
    retire_bad: list[str] = []
    all_tbl_names = {t.get("name") for o in objects.values()
                     for t in o.get("tables") or []}
    for r in retire_rows:
        nm = str(r.get("table") or "")
        if not nm:
            retire_bad.append("retire_tables 有一条缺 table")
            continue
        if not str(r.get("verdict") or "").strip():
            retire_bad.append(f"{nm}: 缺 verdict")
        if not str(r.get("evidence") or "").strip():
            retire_bad.append(f"{nm}: 缺 evidence（退场理由一处一份）")
        if nm in all_tbl_names:
            retire_bad.append(f"{nm}: 已登记退役，却仍在某对象的 tables[] 里（没真退场）")
    fails += retire_bad
    if not args.quiet and not retire_bad:
        print(f"gate: 退役表登记 {len(retire_rows)} 条（各有 verdict+evidence，"
              "均不在 tables[] 里）")

    # 18. 同形孪生逐组裁决（`_overrides.json.twin_verdicts`，docs/05 §9.10）。
    #     `unlinked_layout_twins` 这个指标的意义是「让人逐组看一遍」；看过之后要能把它
    #     按下去，但**不能按坏**——四条都钉：
    #       a) `verdict` 只认 fold / keep，且每条必须有 reason（不写理由等于没裁）；
    #       b) `keep` 的组必须**仍在**引擎的孪生清单里（真折了却留 keep，说明裁决与状态
    #          已经不一致，指标会永远显示 0）；
    #       c) `fold` 的组必须**真的折进一个对象**（同一批复合体的 owner 唯一）；
    #       d) `fold` 的组必须在 `fold` 段里登记（否则是「按了指标、表还是两张」）。
    tv_rows = {str(k): v for k, v in (ov_all.get("twin_verdicts") or {}).items()
               if not str(k).startswith("_") and isinstance(v, dict)}
    twin_bad: list[str] = []
    if tv_rows:
        all_twins = {D.twin_key(g): g for g in D.layout_twins(D.Model(), objects)}
        fold_sets = {frozenset(str(c) for c in (g.get("composites") or []))
                     for g in (ov_all.get("fold") or []) if isinstance(g, dict)}
        owner_of: dict[str, str] = {}
        for oid, o in objects.items():
            for cid in o["folded_composites"]:
                owner_of[cid] = oid
        for key, spec in sorted(tv_rows.items()):
            comps = key.split("+")
            verdict = str(spec.get("verdict") or "")
            if verdict not in ("fold", "keep"):
                twin_bad.append(f"twin_verdicts.{key}: verdict={verdict!r}（只认 fold/keep）")
                continue
            if not str(spec.get("reason") or "").strip():
                twin_bad.append(f"twin_verdicts.{key}: 缺 reason")
            if verdict == "keep":
                if key not in all_twins:
                    twin_bad.append(f"twin_verdicts.{key}: 判 keep 但它已不在孪生清单里"
                                    "（要么真折了、要么改了线布局）")
            else:
                owners = {owner_of.get(c) for c in comps}
                if len(owners) != 1 or None in owners:
                    twin_bad.append(f"twin_verdicts.{key}: 判 fold 但复合体没折进同一个对象"
                                    f"（owner={sorted(x or '?' for x in owners)}）")
                if frozenset(comps) not in fold_sets:
                    twin_bad.append(f"twin_verdicts.{key}: 判 fold 但 `fold` 段里没有这一组")
    fails += twin_bad
    if not args.quiet and not twin_bad:
        print(f"gate: 同形孪生裁决 {len(tv_rows)} 组"
              f"（fold {len([v for v in tv_rows.values() if v.get('verdict') == 'fold'])}"
              f" / keep {len([v for v in tv_rows.values() if v.get('verdict') == 'keep'])}，"
              f"均在 fold 段或仍在清单里）")

    # 19. 注入行键 × `pk` 订正（docs/05 §9.11.1、tools/README 的两个坑）。
    #     `inject_members` 的 `key: true` 是**默认追加**（`injected_members` 往 `pk_members`
    #     尾部 append），而 `pk` 段是**显式全量替换**（`apply_overrides` 里 `pk_kind=override`
    #     的分支）。两者并存时后者赢 —— 批 20 的 `mshipbid_card` 就踩过：`scope` 收窄后行主
    #     换成氏族，注入的 `mclan_id` 被旧的 `pk: ["pilot_id"]` 盖掉，DDL 上唯一索引仍停留在
    #     「每读方一套列表」，而对象页、CLI 摘要、守卫全绿（没人比过这两个段）。
    #     这一门专钉「注入的 key 列必须真的在最终主键里」。
    inj_specs = {str(k): v for k, v in (ov_all.get("inject_members") or {}).items()
                 if not str(k).startswith("_") and isinstance(v, dict) and v.get("key")}
    pk_specs = {str(k): v for k, v in (ov_all.get("pk") or {}).items()
                if not str(k).startswith("_")}
    inj_bad: list[str] = []
    for key in sorted(inj_specs):
        oid, _, mname = key.partition(".")
        o = objects.get(oid)
        if not o:
            inj_bad.append(f"inject_members.{key}: 没有这个对象")
            continue
        pk = (o.get("keys") or {}).get("primary_key") or []
        if mname not in pk:
            inj_bad.append(
                f"inject_members.{key}: 标了 key=true 但最终主键={pk} 里没有它"
                + (f"（`pk` 订正= {pk_specs.get(oid)!r} 是显式全量，会盖掉注入列的追加 ⇒ "
                   f"应写成 {sorted(set(list(pk_specs.get(oid) or []) + [mname]))!r}）"
                   if oid in pk_specs else "（注入路径没生效？）"))
            continue
        if (o.get("keys") or {}).get("pk_kind") not in ("injected_key", "override"):
            inj_bad.append(f"inject_members.{key}: 进了主键但 pk_kind="
                           f"{(o.get('keys') or {}).get('pk_kind')!r}")
    fails += inj_bad
    if not args.quiet and not inj_bad:
        print(f"gate: 注入行键 {len(inj_specs)} 条全在最终主键里"
              f"（其中 {len([k for k in inj_specs if k.partition('.')[0] in pk_specs])} 条"
              f"与 `pk` 订正并存，已按显式全量核对）")

    # 20. 会话解析列（`inject_members.<key>.resolved_by = "session"`，docs/05 §9.11.4）。
    #     本条的出处**不在任何报文里**：值来自服务端会话上下文（`news.clan_id` = 「我的
    #     氏族」，写侧读侧都不带 clan id，容量也排除了）。这一门钉两件事：
    #       ① 出处仍必须写（地址级证据改为「面板/命令按这个实体打开」的旁证）；
    #       ② 必须是**行键列** —— 会话解析出来的普通列只是缓存，第二行写同一个值就漂了。
    #     生成器侧同口径的硬报错在 `derive_homing.injected_members`，这里再对**产物**核一遍
    #     （防「`_overrides` 写了但重生成没跑」这类半截状态）。
    ses_specs = {str(k): v for k, v in (ov_all.get("inject_members") or {}).items()
                 if not str(k).startswith("_") and isinstance(v, dict)
                 and str(v.get("resolved_by") or "") == "session"}
    ses_bad: list[str] = []
    for key in sorted(ses_specs):
        oid, _, mname = key.partition(".")
        spec = ses_specs[key]
        if not str(spec.get("evidence_va") or "").strip():
            ses_bad.append(f"inject_members.{key}: resolved_by=session 也要写 evidence_va"
                           "（证明「面板/命令按这个实体打开」的旁证）")
        if not spec.get("key"):
            ses_bad.append(f"inject_members.{key}: resolved_by=session 必须是行键列")
        o = objects.get(oid)
        if not o:
            ses_bad.append(f"inject_members.{key}: 没有这个对象")
            continue
        pk = (o.get("keys") or {}).get("primary_key") or []
        if mname not in pk:
            ses_bad.append(f"inject_members.{key}: 会话解析列不在最终主键={pk} 里"
                           "（它只能是行键列）")
        mem = next((x for x in o.get("members") or [] if x["name"] == mname), None)
        if mem is None:
            ses_bad.append(f"inject_members.{key}: 产物里没有这个成员（重生成没跑？）")
        elif not mem.get("injected") or \
                str(mem.get("injected_resolved_by") or "") != "session":
            ses_bad.append(
                f"inject_members.{key}: 产物成员没带上会话解析标记"
                f"（injected={mem.get('injected')!r}, "
                f"injected_resolved_by={mem.get('injected_resolved_by')!r}）"
                " ⇒ 重跑 `derive_homing.py --write`")
    fails += ses_bad
    if not args.quiet and not ses_bad and ses_specs:
        print(f"gate: 会话解析列 {len(ses_specs)} 条都是行键列且带出处"
              f"（{'、'.join(sorted(ses_specs))}）")

    if not args.quiet:
        print(f"对象 {len(objects)}  根 {cov['objects_root']}  值 {cov['objects_value']}")
        print(f"fields.jsonl 行 {n_rows}  关联 {len(relations['relations'])}"
              f"（+ 线上引用 {len(relations.get('wire_refs') or [])}）")
        print(f"gate: 复合体全折 {not cov['composites_missing']}  "
              f"失职成员 {len(no_ev)}  已知缺口 {len(known_gap)}  "
              f"无 PK 根对象 {len(cov['roots_without_pk'])}（未决，非失败）")
        for oid, name, why in known_gap:
            print(f"  已知缺口 {oid}.{name}：{why}")

    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        return 1
    if warns and not args.quiet:
        for w in warns:
            print("  WARN", w)
    print("OK  homing 不变量全绿")
    return 0


def _load_composites() -> dict[str, dict]:
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((SCHEMA / "composites").glob("*.json"))}


def _master_tables() -> dict[tuple[str, str], set[str]]:
    """`(schema, 表 id) → 列名集合`，用于校验 `master_refs` 的目标真的存在。

    cfg 表来自 `schema/cfg/tables/*.json`（每表一行 CSV 投影，`columns[].name` 是
    真实列名）；srv 表来自 `schema/srv/tables/*.json`。两处都只做**名字校验**，
    不猜类型。
    """
    out: dict[tuple[str, str], set[str]] = {}
    for schema in ("cfg", "srv"):
        d = SCHEMA / schema / "tables"
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            doc = json.loads(p.read_text(encoding="utf-8"))
            tid = str(doc.get("id") or p.stem)
            cols = {
                str(c.get("name") or c.get("db_column") or "")
                for c in (doc.get("columns") or [])}
            # cfg 表 id 是裸名（`ITEM`），srv 表 id 带 schema 前缀（`srv.shop_lineup`）
            # ——两种写法都登记，`master_refs` 里写哪种都能校验。
            out[(schema, tid)] = cols
            if "." in tid:
                out[(schema, tid.rsplit(".", 1)[-1])] = cols
    return out


def _form_composite(eid: str, n_forms: int, form: dict,
                    comps: dict[str, dict]) -> tuple[str, str]:
    """实体线形 → 复合体 id（精确配对，宁可不判也不误判）。

    顺序：`struct_type` 指名 → `<实体>_<线形>` → 单一形式的实体用实体名 →
    线形名同名 → 唯一「命令集被包含」的复合体。

    每条规则都是被真实数据逼出来的：
      * `pilot.pilot_detail`（51672）不能因为 `SC-0x063E` 也被
        `beginner_challenge_info`（454）引用就配到后者——`struct pilot_detail`
        已经指名了；
      * `dailycup_conf.config`（73）的线形名叫 `config`，而 `config` 复合体
        （34）是另一个对象——它是本实体唯一的线形，按实体名配对才对；
      * `ms.lounge`（299 应为 303）裸靠命令集配不出来（`SC-0xA832` 同时出现在
        `adop_list`/`unlockw` 里），但 `ms` + `lounge` 拼出 `ms_lounge` 唯一命中；
      * 命令集规则要求**被包含**（不是相交）且唯一，否则返回空——不猜。
    """
    st = str(form.get("struct_type") or "").strip()
    named = re.match(r"^struct[\s(<{]*([A-Za-z_][\w]*)", st)
    fname = str(form.get("name") or "")
    cands = [(named.group(1) if named else "", "struct_type")]
    if eid and fname:
        cands.append((f"{eid}_{fname}", "实体名_线形名"))
    if n_forms == 1:
        cands.append((eid, "唯一线形→实体名"))
    cands.append((fname, "线形名"))
    for cand, how in cands:
        if cand and cand in comps:
            return cand, how
    cmds = set(form.get("commands") or [])
    hits = [cid for cid, c in comps.items()
            if cmds and cmds <= set((c.get("evidence") or {}).get("commands") or [])]
    return (hits[0], "commands⊆") if len(hits) == 1 else ("", "")


def _resolvable(target: str, objects: dict) -> bool:
    if not target:
        return False
    if target.startswith(("core.", "srv.", "cfg.")):
        return True
    oname, _, col = target.rpartition(".")
    o = objects.get(oname)
    if o is None:
        return False
    return any(x["name"] == col or D._snake(x["name"]) == col
               for x in o["members"])


if __name__ == "__main__":
    sys.exit(main())

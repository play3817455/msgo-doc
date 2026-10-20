#!/usr/bin/env python3
"""no_writer 根对象清单：**0 个 CS 写方、且没有自身身份列**的 `PERSIST` 根。

为什么要有这份清单
==================
`derive_homing.py::coverage()` 把「无自身行键的 `PERSIST` 根」分成三桶：
`singleton`（每个作用域一行）、`no_writer`（0 个 CS 写方）、以及**真未决**。
前两桶不阻塞建表，但 `no_writer` 这桶的建表口径是**退化的**——键只剩
`(world_id, pilot_id)`，行却来自「SC 当顶层数组下发的他人数据」：写方一落地就会
互相 upsert 覆盖（docs/05 §9.3）。

这份清单把这 35 个对象的结构事实一次列全，供逐条裁决「该不该有表」：

  * **孪生根**：成员名序与某个**非 no_writer** 对象完全相同的对象（同一张线形被两个
    对象各建一张表）；
  * **子集宿主**：成员集是某个根对象成员集的真子集（同一批行的窗口）；
  * **身份候选**：现成的 `*_id`/`uniqid`/`index` 命名（要判「自己的记录号」还是
    「指向别人的引用」，见 docs/05 §4.B）。

批次 17 已把 35 条全部裁决完（`reviewed.batch_17_no_writer_closure`）：13 `DERIVED`
+ 9 `EVENT` + 1 `CONFIG` + 3 `TBD` + 1 改判 `singleton`，另有 9 个线形折进 `pilot`
（`fold`）——本清单现在的作用是**存档裁决与列残留**：谁因为什么不建表、将来写入方
落地要先补哪一列（理由写在对象的 `no_table_reason` 上）。引擎侧的分桶口径见
docs/05 §9.9（`relations[]` 只收源对象建表的边，其余进 `wire_refs[]`）。

裁决落 `_overrides.json.disposition`（`DERIVED` / `EVENT` / `CONFIG` / `TRANSIENT`）
或 `pk`（有身份列可钉）。本清单只读模型，不读 DDL——两者一致性由
`serverv/tools/verify_no_blob.py` 看住。

生成：
    python tools/report_no_writer.py            # 写 schema/_meta/no_writer_roots.md
    python tools/report_no_writer.py --check    # 只校验文件是否为最新（CI 用）
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
HOMING = SCHEMA / "homing"
OBJECTS = HOMING / "objects"
OUT = SCHEMA / "_meta" / "no_writer_roots.md"

IDENT_HINTS = ("uniqid", "_id", "index", "idx", "slot", "no", "seq")


def load_objects() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(OBJECTS.glob("*.json")):
        o = json.loads(p.read_text(encoding="utf-8"))
        out[o["id"]] = o
    return out


def member_names(o: dict) -> list[str]:
    return [m["name"] for m in o.get("members") or []]


def element_composites(o: dict) -> set[str]:
    """本对象把哪些对象当作（数组/内嵌）成员类型。"""
    refs: set[str] = set()
    for m in o.get("members") or []:
        t = str(m.get("wire_type") or "")
        mm = re.match(r"(?:array<)?(?:struct<)?([A-Za-z0-9_]+)", t)
        if mm:
            refs.add(mm.group(1))
    return refs


def compute_facts(objs: dict[str, dict], nw: list[str]) -> dict[str, dict]:
    host_of: dict[tuple, list[tuple[str, str]]] = {}
    for oid, o in objs.items():
        for m in o.get("members") or []:
            t = str(m.get("wire_type") or "")
            mm = re.match(r"(?:array<)?(?:struct<)?([A-Za-z0-9_]+)", t)
            if mm and mm.group(1) in objs and mm.group(1) != oid:
                host_of.setdefault(tuple(member_names(objs[mm.group(1)])), []).append((oid, m["name"]))

    facts: dict[str, dict] = {}
    for oid in nw:
        a = member_names(objs[oid])
        tw = [x for x in objs
              if x != oid and x not in nw and member_names(objs[x]) == a and len(a) > 1]
        tw_nw = [x for x in nw if x != oid and member_names(objs[x]) == a and len(a) > 1]
        subset = []
        for x, o in objs.items():
            if x in nw or x == oid:
                continue
            b = member_names(o)
            if len(a) > 2 and set(a) < set(b):
                subset.append(x)
            elif len(a) > 2 and a[:5] == b[:5] and len(a) != len(b):
                subset.append(f"{x}（同前缀）")
        facts[oid] = {
            "twin_roots": sorted(tw),
            "twin_nw": sorted(tw_nw),
            "as_member_of": sorted(f"{p}.{m}" for p, m in host_of.get(tuple(a), [])),
            "subset_of": sorted(subset),
            "idents": [n for n in a if n == "id" or any(n.endswith(h) or h in n for h in IDENT_HINTS)],
        }
    return facts


def cmds(entries: list[dict]) -> str:
    return ", ".join(f"`{e.get('command', '')}`" for e in entries if e.get("command"))


def render(objs: dict[str, dict], ov: dict) -> str:
    nw_all = [k for k in (ov.get("no_writer") or {}) if k != "_note"]
    # 名单里可能有**已经被折叠**（并进别的对象）的 id：`no_writer` 这一栏记的是
    # 「历史上判过 0 CS 写方」这件事，并表之后对象本身在模型里已经不存在
    # （`schema/homing/objects/<id>.json` 没了）——不能拿它去索引 `objs`。
    gone = sorted(k for k in nw_all if k not in objs)
    nw = [k for k in nw_all if k in objs]
    fold_host = {}
    for g in ov.get("fold") or []:
        if not isinstance(g, dict):
            continue
        for c in g.get("composites") or []:
            fold_host[str(c)] = str(g.get("as") or "")
    facts = compute_facts(objs, nw)

    # 待裁决 = 仍是 PERSIST（有表）的；已裁决的（DERIVED/EVENT/CONFIG…）单列一节。
    open_ids = [k for k in nw if objs[k].get("disposition") == "PERSIST"]
    done_ids = [k for k in nw if objs[k].get("disposition") != "PERSIST"]
    open_ids.sort()
    done_ids.sort(key=lambda k: (objs[k].get("disposition", ""), k))

    L: list[str] = [
        "# no_writer 根对象：0 个 CS 写方、无自身身份列（待定表去留）",
        "",
        "由 `tools/report_no_writer.py` 生成，**不要手改**；改模型后重跑脚本。",
        "",
        f"`_overrides.json.no_writer` 共 **{len(nw_all)}** 个：**待裁决 {len(open_ids)}**"
        f"（仍是 `PERSIST`、有表）+ **已裁决 {len(done_ids)}**（改判 `DERIVED`/`EVENT`/"
        f"`CONFIG`/`TBD`，DDL 里没有表）+ **已并表退场 {len(gone)}**（对象已被 `fold` "
        "折进别的对象）。",
        "",
        "## 为什么这桶危险",
        "",
        "它们都被 **SC 当顶层数组下发**（他人卡片 / 排行投影 / 战果附属 / 战斗期数组），",
        "而建表口径只剩 `(world_id, pilot_id)`——数组元素按单行建表 = **静默压行**",
        "（docs/05 §9.3）。0 个 CS 写方只是让问题**暂时**不发作：写方一落地就丢行。",
        "",
        "裁决的三条出路（docs/05 §9.8 同口径）：",
        "",
        "1. **孪生/子集** → `DERIVED`：行本来就在别的根表里（或能由它算出），退役副本表；",
        "2. **战斗期数组** → `EVENT`：服务端每场重算，本就不该落库（`fire_point` 先例）；",
        "3. **真有身份列** → 钉 `pk` 保留表（或 `inject_members` 补一列，同 `news` 的 `msg_id`）。",
        "",
        "## 待裁决",
        "",
        "| 对象 | 成员 | PK 类别 | 孪生根（非 no_writer） | 同批孪生 | 作为谁的成员 | 子集宿主 | 身份候选 | SC 读方 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for oid in open_ids:
        o, f = objs[oid], facts[oid]
        L.append(
            f"| `{oid}` | {len(o.get('members') or [])} | {o.get('pk_kind', '')} | "
            f"{', '.join('`%s`' % x for x in f['twin_roots']) or '—'} | "
            f"{', '.join('`%s`' % x for x in f['twin_nw']) or '—'} | "
            f"{', '.join('`%s`' % x for x in f['as_member_of']) or '—'} | "
            f"{', '.join('`%s`' % x for x in f['subset_of']) or '—'} | "
            f"{', '.join(f['idents']) or '—'} | {cmds(o.get('reads') or [])} |")

    L += [
        "",
        "## 已裁决",
        "",
        "| 对象 | 处置 | 理由 | 孪生根 |",
        "|---|---|---|---|",
    ]
    for oid in done_ids:
        o, f = objs[oid], facts[oid]
        L.append(
            f"| `{oid}` | `{o.get('disposition')}` | {o.get('no_table_reason', '') or ov_reason(ov, oid)} | "
            f"{', '.join('`%s`' % x for x in f['twin_roots']) or '—'} |")

    if gone:
        L += [
            "",
            "## 已并表退场（`fold`：十个线形 → 一个对象）",
            "",
            "| 对象 | 并入 | 依据 |",
            "|---|---|---|",
        ]
        for oid in gone:
            L.append(f"| `{oid}` | `{fold_host.get(oid, '?')}` | "
                     "列不丢：成员并进宿主对象（`_overrides.json.fold` 逐条带理由） |")

    L += [
        "",
        "## 备注",
        "",
        "- 「孪生根」= 成员名序**完全相同**的非 no_writer 对象：同一张线形被两个对象各建一张",
        "  表，写方落到哪张另一张就是副本（`c4j` 的 `unlockw` 即此类，处置见 docs/05 §9.8）。",
        "- 「子集宿主」= 成员集是别人真子集（或前 5 个成员同序）：同一批行的一个窗口。",
        "- 「身份候选」只是命名候选：`*_id` 多半是**指向别人**的引用（`docs/05 §4.B`），",
        "  钉成 PK 前先证明它是**自己的**记录号。",
        "- 裁决写 `_overrides.json.disposition`（`DERIVED`/`EVENT`/`CONFIG`/`TRANSIENT` 之一）",
        "  或 `pk`；引擎据此清掉 `table` 并落 `no_table_reason`（非 PERSIST 不建表，",
        "  `verify_no_blob.py` 复核）。",
        "",
    ]
    return "\n".join(L)


def ov_reason(ov: dict, oid: str) -> str:
    """裁决理由：先看 `disposition.<oid>.reason`（P4 起的写法），再看旧的 `reason.<oid>`。"""
    d = ov.get("disposition")
    if isinstance(d, dict):
        spec = d.get(oid)
        if isinstance(spec, dict) and spec.get("reason"):
            return str(spec["reason"])
        if isinstance(spec, str) and spec:
            return f"（`disposition` 写作裸值 `{spec}`，未留理由）"
    r = ov.get("reason")
    if isinstance(r, dict) and r.get(oid):
        return str(r[oid])
    return ""


def main() -> int:
    objs = load_objects()
    ov = json.loads((HOMING / "_overrides.json").read_text(encoding="utf-8"))
    text = render(objs, ov)
    if "--check" in sys.argv:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != text:
            print(f"过期：{OUT}（重跑 python tools/report_no_writer.py）", file=sys.stderr)
            return 1
        print(f"OK  {OUT} 与模型一致")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

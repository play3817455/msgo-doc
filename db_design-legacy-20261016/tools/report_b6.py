#!/usr/bin/env python3
"""非 `PERSIST` 根对象清单：B6 入口（`EVENT` / `TBD`）+ 已裁决退场（`DERIVED` / `CONFIG`）。

为什么要有这份清单
==================
`docs/00 §3` 把 `EVENT` 定为「战斗/会话 ephemeral」→ 不建表；`TBD` 未决定 →
本轮也不建表。于是 `0003_game_persist.up.sql` 里没有它们的表（P4 起由
`schema_design/plan_objects.py` 的 `disposition == PERSIST` 过滤保证），模型里
也不许留幻影表（`derive_homing.py::build_table_graph` 的幻影表门）。

但「不建表」不等于「这些数据不重要」——`EVENT`/`TBD` 是**战斗持久化（B6）**的输入。
这份清单把每个对象的归属（域）、谁在写（CS）、谁在读（SC）、以及现成的身份候选列
一次列全，让 B6 开工时不必重新翻命令表。

`DERIVED` / `CONFIG` 不是 B6 的输入：它们是批 19 起**已裁决退场**的对象
（行在别的根表里 / 可由别的表算 / 运营配置）。它们也在「非 PERSIST」这一层，
所以一并列出——否则「共 N 个」这个总数与表里的行数对不上账。

生成：
    python tools/report_b6.py            # 写 schema/_meta/b6_event_tables.md
    python tools/report_b6.py --check    # 只校验文件是否为最新（CI 用）

判据全部来自 `schema/homing/objects/*.json`，不读 DDL——两者的一致性由
`serverv/tools/verify_no_blob.py` 的幻影表门看住。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
OBJECTS = SCHEMA / "homing" / "objects"
OUT = SCHEMA / "_meta" / "b6_event_tables.md"

# 身份候选：B6 要落库时必须先给每个对象定一个「同一作用域内的行身份」，这些
# 命名是现成的候选（不是结论——`*_id` 多半是指向别人的引用，见 derive_homing
# 的 IDENT_NAMES 注释）。
IDENT_HINTS = ("uniqid", "uniq_id", "index", "idx", "slot", "no", "seq", "key")


def load_objects() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(OBJECTS.glob("*.json")):
        o = json.loads(p.read_text(encoding="utf-8"))
        out[o["id"]] = o
    return out


def identity_candidates(o: dict) -> list[str]:
    names = [x["name"] for x in o["members"]]
    hits = [n for n in names if n == "id" or n.endswith("_id") or n in IDENT_HINTS]
    return hits


def cmds(entries: list[dict]) -> str:
    return ", ".join(f"`{e.get('command', '')}`" for e in entries if e.get("command"))


def reason_brief(o: dict) -> str:
    """裁决理由的首句（`no_table_reason` 统一以「disposition=XXX（不建表）：」开头）。"""
    r = str(o.get("no_table_reason") or "").strip()
    if not r:
        return "—"
    if r.startswith("disposition=") and "：" in r:
        r = r.split("：", 1)[1].strip()
    return (r.split("。")[0].strip() or r[:80]).replace("|", "\\|")


def render(objs: dict[str, dict]) -> str:
    rows = [o for o in objs.values()
            if o.get("is_root") and o.get("disposition") != "PERSIST"]
    rows.sort(key=lambda o: (o["disposition"], o["domain"], o["id"]))

    ev = [o for o in rows if o["disposition"] == "EVENT"]
    tbd = [o for o in rows if o["disposition"] == "TBD"]
    dead = [o for o in rows if o["disposition"] in ("DERIVED", "CONFIG")]

    L: list[str] = [
        "# 非 PERSIST 根对象：B6 入口（EVENT/TBD）+ 已裁决退场（DERIVED/CONFIG）",
        "",
        "由 `tools/report_b6.py` 生成，**不要手改**；改模型后重跑脚本。",
        "",
        f"共 **{len(rows)}** 个根对象不建表，四个桶各自成因不同，处置也不同：",
        "",
        "| 桶 | 条数 | 意思 | 开工时要做什么 |",
        "|---|---|---|---|",
        f"| `EVENT` | {len(ev)} | 战斗/会话 ephemeral（一局一份，结算即弃） | 定身份列 + 定写入方（见下两节） |",
        f"| `TBD` | {len(tbd)} | 分类未定（成员/线宽还有洞） | 先补模型，再判落 `PERSIST` 还是 `EVENT` |",
        f"| `DERIVED` | {sum(1 for o in dead if o['disposition'] == 'DERIVED')} | 行在别的根表里 / 可由别的表算出 | **不建表**（已裁决，理由逐条见末节） |",
        f"| `CONFIG` | {sum(1 for o in dead if o['disposition'] == 'CONFIG')} | 运营配置（主数据侧维护） | **不建表**（已裁决，理由逐条见末节） |",
        "",
        "后两桶（`DERIVED`/`CONFIG`）是**批 19 起的裁决结果**，它们不是 B6 的输入，"
        "只是同在「非 PERSIST」这一层；列在末节是为了让「48 个」这个总数能对上账"
        "（此前只列 EVENT/TBD 两桶，表里 29 条、标题 48 条，读的人会以为漏了 19 个）。",
        "",
        "它们不进 `0003_game_persist.up.sql`（P4 起由生成器的 `disposition == PERSIST` "
        "过滤保证），模型里也没有幻影表（`derive_homing.py` 的幻影表门，"
        "`serverv/tools/verify_no_blob.py` 复核）。",
        "",
        "**B6 开工时要做的两件事**（每个对象各自定，不能一刀切）：",
        "",
        "1. **定身份列**：现在它们只有 `world_id, pilot_id` 兜底，多条记录会互相 "
        "upsert 覆盖。下表「身份候选」列是现成的命名候选（`ent_id`/`room_id`/"
        "`item_id`/`route_no`/`index`…），但要逐个判「是**自己的**记录号还是**指向别人"
        "的**引用」——`*_id` 多半是后者，当 PK 会把「一个实体一条」错钉成「一个引用"
        "目标一条」（`docs/05 §4.B`）。",
        "2. **定写入方**：`CS 写方` 列为空的，说明服务端现在没有落库路径（战斗侧"
        "`battle/room.go` 的 `Room.Settle` 还是 no-op）；有了写入方才有「什么时候写、"
        "写哪一行」的问题，键也才有意义。",
        "",
        "## EVENT（战斗/会话 ephemeral）",
        "",
        "| 对象 | 域 | 线长 | 成员 | CS 写方 | SC 读方 | 身份候选 |",
        "|---|---|---|---|---|---|---|",
    ]
    for o in ev:
        lens = [v.get("length") or 0 for v in o.get("views") or []]
        L.append(
            f"| `{o['id']}` | {o['domain']} | {max(lens) if lens else ''}"
            f" | {len(o['members'])} | {cmds(o.get('writes') or [])} | "
            f"{cmds(o.get('reads') or [])} | {', '.join(identity_candidates(o)) or '—'} |")

    L += [
        "",
        "## TBD（分类未定）",
        "",
        "| 对象 | 域 | 成员 | CS 写方 | SC 读方 | 身份候选 | 说明 |",
        "|---|---|---|---|---|---|---|",
    ]
    for o in tbd:
        why = "成员是占位 / 线宽未定" if any(
            "TBD" == str(x.get("name", "")).upper() for x in o["members"]) else ""
        L.append(
            f"| `{o['id']}` | {o['domain']} | {len(o['members'])} | "
            f"{cmds(o.get('writes') or [])} | {cmds(o.get('reads') or [])} | "
            f"{', '.join(identity_candidates(o)) or '—'} | {why} |")

    L += [
        "",
        "## 已裁决退场（DERIVED / CONFIG，不建表）",
        "",
        "| 对象 | 域 | 裁决 | 理由（`no_table_reason` 首句；全文见对象页） |",
        "|---|---|---|---|",
    ]
    for o in dead:
        L.append(f"| `{o['id']}` | {o['domain']} | {o['disposition']} | "
                 f"{reason_brief(o)} |")

    L += [
        "",
        "## 备注",
        "",
        "- 标 `TBD` 的对象先要补模型（成员/线宽），补完可能落进 `PERSIST` 或 `EVENT`；",
        "  这一层没定之前不要给它建表。",
        "- 「线长」取对象视图里的线体长度；`TBD` 行留空表示还没定形。",
        "- 本清单与 `0003` 的对账口径：**非 PERSIST 对象不得出现在 DDL 里**，",
        "  `verify_no_blob.py` 会在入库前拦一次。",
        "- `DERIVED`/`CONFIG` 桶若将来出现写入方或新列，裁决要回到",
        "  `_overrides.json.disposition` 改，并重跑本脚本（`--check` 会在 CI 拦过期）。",
        "",
    ]
    return "\n".join(L)


def main() -> int:
    text = render(load_objects())
    if "--check" in sys.argv:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != text:
            print(f"过期：{OUT}（重跑 python tools/report_b6.py）", file=sys.stderr)
            return 1
        print(f"OK  {OUT} 与模型一致")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

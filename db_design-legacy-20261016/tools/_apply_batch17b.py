#!/usr/bin/env python3
"""批次 17 收尾（b）：折叠后的**旧锚表退场登记** + `no_writer` 桶清理。

批次 17（`tools/_apply_batch17.py`）把十个「机师/名片」线形折成一个对象 `pilot`，
但 `schema/_meta/legacy_evidence.json` 里仍把 `tbl_pilots_list` / `tbl_pcard` /
`tbl_lpcard` / `tbl_block_detail` / `tbl_friend_histories` 声明为 PERSIST，
`derive_homing.py.build_table_graph` 的「旧表守恒」段会按 `entity_ref` 找到折叠后的
对象，于是**同一个对象又投影出五张根表**（外加五张 `__avatar` 子表）——同一批行六张
表必然漂移，正是 `unlockw`（batch_16）踩过的坑。

所以这里做两件事：

1. 把五张旧锚表 + `game.item_list`（`DERIVED`，旧库声明 PERSIST）登记进
   `_overrides.json.retire_tables`——引擎允许退役的唯一入口，「退场理由一处一份」。
2. 把 `lvjudge_hist` 从 `no_writer` 桶里摘掉：它已改判 `singleton`，
   而 `coverage()` 的两个桶是**互斥**的（同一个 id 同时在两个桶里会被重复计数）。

见 `reviewed.batch_17_no_writer_closure` 与 `fold`。
"""

import json
import pathlib

HOMING = pathlib.Path(__file__).resolve().parents[1] / "schema" / "homing"
OV = HOMING / "_overrides.json"

FOLD_NOTE = (
    "十个线布局是同一个「机师」实体（`pilot` 159B 轻量形 / `pilots_list`/`pcard` 398B "
    "名片形 / `lpcard` 族 113B 轻量名片形），按 `_overrides.json.fold` 折成对象 `pilot`，"
    "表仍是 `game.pilot`（键 (world_id,pilot_id,slot)）。取证明细见 "
    "reviewed.batch_17_no_writer_closure。"
)

RETIRE = [
    {
        "table": "game.pilots_list",
        "verdict": "retire",
        "evidence": (
            "旧库把同一个机师实体切成四张表（`tbl_pilot`/`tbl_pilots_list`/`tbl_pcard`/"
            "`tbl_pilot_detail`，docs/05 §1 第 1 项）。字段化重建后 `pilots_list` 与 `pcard` "
            "是**逐字节同形**的名片线形（58 成员 / 398B，成员名序与偏移完全一致），`pilot`"
            "（24 成员 / 159B）是它的真子集。读方 `SC-0xE13A-lounge-pilot_list_get_r`"
            "（名字串 VA 0xee70a8，派发槽 vt[0x84]）把两个阵营的机师当顶层数组下发，行就是"
            "机师本身。" + FOLD_NOTE + " "
            "退表不丢行：同一行键在 `game.pilot`；退表不丢列：`rec_*`/`score_*`/`last_in`/"
            "`state_bits`/`clan_memb_exp_use` 等 30 列在 `game.pilot` 有娘家（逐成员比对见 "
            "tools/_q_nw_cols.py 口径）。"
        ),
    },
    {
        "table": "game.pcard",
        "verdict": "retire",
        "evidence": (
            "与 `game.pilots_list` 同一条线形（58 成员 / 398B，逐字节相同）：读方 "
            "`SC-0xB4B6-lounge-pilotcard_get_r`（名字串 VA 0xb74012，派发槽 vt[0x150]）。"
            + FOLD_NOTE + " 旧库把名片单列一张表，字段化后它就是 `game.pilot` 那一行的"
            "另一个读法，退场。"
        ),
    },
    {
        "table": "game.lpcard",
        "verdict": "retire",
        "evidence": (
            "他人名片族的**规范形**（113B / 20 成员）：读方 "
            "`SC-0x7051-lounge-clan_memberlist_get_r`（名字串 VA 0xb6606f，派发槽 vt[0x418]）"
            "下发战队成员名片，行属于别人但仍是「机师」这一行。同形的还有 `block_detail`/"
            "`friend_detail`/`friend_histories`/`member_info`/`mshipbid_card`/"
            "`clan_member_card`——它们没有旧库 PERSIST 声明，故退役记录只落在这张规范形上。"
            + FOLD_NOTE + " 退表不丢行：行键 (world_id,pilot_id,slot) 由 `game.pilot` 承载；"
            "坏味道的证据是旧 `LpcardRow` 里 scope 的 `PilotID`（我）与前缀化的线字段 "
            "`LpcardPilotId`（对方）并存——同一行被 scope 压扁（docs/05 §9.3）。"
        ),
    },
    {
        "table": "game.block_detail",
        "verdict": "retire",
        "evidence": (
            "`lpcard` 113B / 20 成员的**同名同序**副本：读方 "
            "`SC-0x7587-lounge-block_list_get_detail_xworld_r`（名字串 VA 0xb679c3，"
            "派发槽 vt[0x378]）下发屏蔽名单里那几名机师的名片（行属于别人），0 CS 写方。"
            + FOLD_NOTE + " 退场。"
        ),
    },
    {
        "table": "game.friend_histories",
        "verdict": "retire",
        "evidence": (
            "`lpcard` 113B / 20 成员的**同名同序**副本：读方 "
            "`SC-0x9F94-lounge-friend_history_get_xworld_r`（名字串 VA 0xb6eab3，"
            "派发槽 vt[0x368]）下发「最近一起玩过的机师」名片（行属于别人），0 CS 写方。"
            + FOLD_NOTE + " 退场。"
        ),
    },
    {
        "table": "game.item_list",
        "verdict": "retire",
        "evidence": (
            "判 `DERIVED`（不建表）：`item_list` 与 BGM 包货架 `bmgpack` 是**同 23B 元素、"
            "同一打印器 `sub_B4E110`、同一组 7 列**（`shopitem_id` + `gp_x01`/`gp_x10`/"
            "`cp_x01`/`cp_x10` + `bit_eff` + `stock`），差别只在读命令与 `stock` 的偏移"
            "（bmgpack 22 / item_list 21，内存对齐差 1B）：`SC-0x99A0-lounge-shop_lineup_r`"
            "（名字串 VA 0xb6e2f4，派发槽 vt[0x3A8]）下道具货架，"
            "`SC-0xE13A-lounge-pilot_list_get_r` 下 BGM 包货架。价格与库存是**运营主数据**，"
            "`shopitem_id` 已判 `master` 引用 ⇒ 主数据侧（`cfg.*`）才是家，玩家维度不留读数表。"
            "0 CS 写方。取证明细见 reviewed.batch_17_no_writer_closure.取证_六问。"
        ),
    },
]


def main() -> int:
    ov = json.loads(OV.read_text(encoding="utf-8"))
    nw = ov.get("no_writer") or {}
    moved = [k for k in nw if k == "lvjudge_hist"]
    for k in moved:
        nw.pop(k)
    ov["no_writer"] = nw

    rt = ov.setdefault("retire_tables", [])
    have = {str(i.get("table")) for i in rt if isinstance(i, dict)}
    added: list[str] = []
    for it in RETIRE:
        if it["table"] in have:
            continue
        rt.append(it)
        added.append(it["table"])

    OV.write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"retire_tables +{len(added)}: {', '.join(added) or '（无）'}")
    print(f"no_writer -{len(moved)}: {', '.join(moved) or '（无）'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

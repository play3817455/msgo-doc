"""批 18：修正批 17 的折叠范围（113B 列表族有自己的行集与写方）。

批 17 把十个线布局当成「同一个机师实体」一起折进 `pilot`。**错了**：`pilot`（159B）
与 `pilots_list`/`pcard`（398B 名册）的行集是「机师本人」（旧库键 `(world_id,pilot_id)`，
`pilot` 形还带 `slot`），而七个 113B 形（20 成员 / 113B）的行集是**「我这份列表里的一条
条目」**——旧库键一律 `(world_id, 我, slot)`（`legacy_evidence.json` 的 `unique_indexes`），
卡片字段描述的是**别人**（前缀化的线字段 `BlockDetailPilotId`/`LpcardPilotId` 与 scope 的
`PilotID` 并存，正是压行的痕迹）。

更关键：其中四个**有真实 CS 写方**，引擎认不出因为它们只带目标机师 id、报文里没有卡片
结构（`attribute_commands` 的口径是「线体里带了这个复合体」）：

  * `CS-0xECDA-lounge-block_list_add`（`pilotid`/`world_id`/`to_pilot_name`，状态串
    @0x00EEC138）与 `CS-0x753A-lounge-block_list_remove`（@0xeec168）→ 屏蔽名单
  * `CS-0xA30C-lounge-friend_list_remove`（`pilotid`，@0xEEC018）与
    `CS-0xBA4E-lounge-friend_list_mail_accept`（`mailid`/`pilotid`，@0xEEBFE0）→ 好友名单

按批 17 的口径②（0 CS 写方 + 行可派生 ⇒ 不建表）它们**不适用**：有写方，且行（列表成员
关系）不可派生。所以这批：

  1. `fold.composites` 缩到 `{pilot, pilots_list, pcard}`（同一批行：机师本人 / 名册）；
  2. `block_detail` / `friend_detail` / `friend_histories` / `mshipbid_card` 恢复 `PERSIST`，
     身份 = **目标机师** `pilot_id`（`pk` 订正；scope 仍是 `(world_id, 我)`）；
  3. 漏掉的写方逐条点名登记（`writers` 段，带 name-str VA）——「说 0 写方之前先把
     『只带目标 id』的命令枚举干净」；
  4. `lpcard` / `clan_member_card` / `member_info` 维持退表，但改判 `DERIVED`：
     20 列全是 `pilot` 并集的子集，而**成员关系可由 `pilot.clan_id` 推出**（同氏族 =
     同 `clan_id` 的机师集合）、`member_info` 就是「我」那一行 ⇒ 行可派生；
  5. `game.block_detail` / `game.friend_histories` 从 `retire_tables` 撤回（表回来了）。

`mshipbid_card` 的欠账：竞标者是**「某氏族在某台 MS 的竞标」下的行**，而 113B 线里没有
bid 上下文列（氏族 / MS）——按 `(world_id, pilot_id)` 建会撞行（同一机师竞标多台 MS）。
本轮先建表并把欠账写清：等竞标写入方落地时补 `inject_members`（clan_id/ms_id）。

用法：`python -X utf8 tools/_apply_batch18.py`（幂等；跑完可删）。
"""
from __future__ import annotations

import json
from pathlib import Path

OV = Path(__file__).resolve().parent.parent / "schema/homing/_overrides.json"

FOLD_REASON = (
    "三条线布局是**同一批行**（机师本人）的详略形：`pcard` 与 `pilots_list` 成员名序/"
    "偏移/总长**逐字节相同**（58 成员 / 398B），`pilot`（24 成员 / 159B）的成员名是它的"
    "真子集，行键同族（`(world_id,pilot_id[,slot])`，`slot` 是 `pilot` 形的分槽）。"
    "见 reviewed.batch_17_no_writer_closure 与 reviewed.batch_18_list_family_correction："
    "批 17 曾把七个 113B **列表**形（行是「我列表里的一条」，旧库键 `(world_id,我,slot)`）"
    "一起折进来，批 18 已把它们移出（其中四个有真实 CS 写方，见 `writers` 段）。"
)

DISPOSITIONS = {
    "lpcard": {
        "as": "DERIVED",
        "reason": (
            "氏族成员名片的**读视图**（113B / 20 成员，与 `friend_detail` 等同形）：20 列"
            "全是 `pilot` 并集的子集，而**成员关系可由 `pilot.clan_id` 推出**——「某氏族的"
            "成员」= 同 `clan_id` 的机师集合（`SC-0x…-clan_memberlist_get_r` 是查询，"
            "0 CS 写方）⇒ 行可派生，不建表。旧库把它按 `(world_id, 我, slot)` 存成每个"
            "请求者一份的副本（压行），批 18 起不再复刻。"),
    },
    "clan_member_card": {
        "as": "DERIVED",
        "reason": (
            "氏族成员名片（孪生根，与 `lpcard` 逐字节同形 / 20 成员）：同判——成员关系在"
            "`pilot.clan_id`，卡片列 ⊂ `pilot` 并集，0 CS 写方 ⇒ 不建第二张成员表。"),
    },
    "member_info": {
        "as": "DERIVED",
        "reason": (
            "「我自己的名片」（`SC-0x…-clan_info_get_self_r` 里的 `member_info`，113B / "
            "20 成员）：行就是**我**这一行，20 列 ⊂ `pilot` 并集 ⇒ 由 `game.pilot` 投影，"
            "不另建表（0 CS 写方）。"),
    },
}

# 恢复建表的列表族：身份 = **目标机师** `pilot_id`（线里的 `pilot_id` 成员）。
RESTORE_PK = {
    "block_detail": (
        "屏蔽名单条目的**目标机师**（线里的 `pilot_id`；`world_id` + scope 的 `pilot_id`"
        "= 我，两者同名不同义，引擎按旧库口径把线字段前缀化）。旧库键是 "
        "`(world_id, 我, slot)`——槽序是列表位置不是身份，改用目标机师做键："
        "同一机师只可能在名单里出现一次（add/remove 就是按它增删），槽序由排序派生。"),
    "friend_detail": (
        "好友名单条目的**目标机师**（线里的 `pilot_id`）。同 `block_detail`：旧库键 "
        "`(world_id, 我, slot)` 的 slot 是列表位置，身份是名单里的那个人。"),
    "friend_histories": (
        "「最近一起玩过」名单的**目标机师**（线里的 `pilot_id`）。行是「我和他同场过」"
        "这条关系，身份是那个人（旧库键 `(world_id, 我, slot)` 同族）。欠账：写入方在"
        "服务端（战斗结束记一笔），本批没有任何 CS 命令碰它——登记在案，等 B6 战斗"
        "持久化落地时接上。"),
    "mshipbid_card": (
        "竞标者条目（`clan_mshipbid_get_list_r` 里的 113B 卡片）的**机师**。**欠账**：这条"
        "行的真正上下文是「某氏族在哪台 MS 上的竞标」（`clan_id` / `ms_id`），而 113B 线里"
        "没有这两个列——按 `(world_id, pilot_id)` 建表在同一机师竞标多台 MS 时会撞行。"
        "等竞标写入方落地时补 `inject_members`（clan_id/ms_id），本轮先把关系留住。"),
}

WRITERS = {
    "block_detail": {
        "commands": [
            "CS-0xECDA-lounge-block_list_add",
            "CS-0x753A-lounge-block_list_remove",
        ],
        "evidence_va": "0x00EEC138 / 0xeec168",
        "reason": (
            "屏蔽名单的写方只带**目标机师 id**：`block_list_add` 的字段是 "
            "`pilotid`/`world_id`/`to_pilot_name`（状态串 @0x00EEC138），"
            "`block_list_remove` 同形（@0xeec168，`to_pilot_name` 是 bytes）。报文里没有 "
            "113B 卡片结构，引擎「线体里带了这个复合体」的口径认不出来 ⇒ 被判 0 CS 写方。"
            "两条都是 CS（add=create / remove=delete），写的正是 `(world, 我) → 目标机师`"
            "这份行集。"),
    },
    "friend_detail": {
        "commands": [
            "CS-0xA30C-lounge-friend_list_remove",
            "CS-0xBA4E-lounge-friend_list_mail_accept",
        ],
        "evidence_va": "0xEEC018 / 0xEEBFE0",
        "reason": (
            "好友名单的写方同样只带目标 id：`friend_list_remove`（`pilotid`，@0xEEC018）、"
            "`friend_list_mail_accept`（`mailid` + `pilotid`，@0xEEBFE0，接受申请即入名单，"
            "回执 `SC-0x84CB` 带 `to_pilotid`）。线体里没有卡片结构，引擎认不出 ⇒ 点名登记。"),
    },
}

RETIRE_UNDO = ["game.block_detail", "game.friend_histories"]

BATCH_NOTE = {
    "verdict": (
        "用户裁决 A（修正批 17）：折叠范围缩到 `{pilot, pilots_list, pcard}`；"
        "`block_detail` / `friend_detail` / `friend_histories` / `mshipbid_card` 恢复建表"
        "（身份 = 目标机师 `pilot_id`）；`lpcard` / `clan_member_card` / `member_info` 改判 "
        "`DERIVED`。"),
    "起因": (
        "批 17 把十个线布局一起折进 `pilot`，理由写的是「行始终是机师本身」。清 serverv "
        "手写面时按旧库 `unique_indexes` 复核，发现**七个 113B 形的旧库行键是 "
        "`(world_id, 我, slot)`**（`block_detail`/`friend_histories`/`lpcard` 的 "
        "`legacy_evidence.json.unique_indexes` 逐条可查），即「我这份列表里的一条条目」，"
        "卡片字段说的是**别人**——行不是机师本人。"),
    "写方证据": (
        "四个 113B 列表有真实 CS 写方，且**只带目标机师 id**（报文里没有卡片结构），"
        "所以引擎的 `attribute_commands`（口径：命令线体里带了这个复合体）认不出："
        "`CS-0xECDA-block_list_add`（`pilotid`/`world_id`/`to_pilot_name` @0x00EEC138）、"
        "`CS-0x753A-block_list_remove`（@0xeec168）、`CS-0xA30C-friend_list_remove`"
        "（`pilotid` @0xEEC018）、`CS-0xBA4E-friend_list_mail_accept`"
        "（`mailid`/`pilotid` @0xEEBFE0）。→ 批 17 口径②（0 CS 写 + 行可派生 ⇒ 不建表）"
        "**不适用**：有写方，且「列表成员关系」不可派生。"),
    "列可派生性": (
        "七个 113B 形的 20 个成员**全部**是 `pilot` 并集的子集（逐名比对），所以退表的"
        "前提在**列**这一侧是成立的——不成立的是**行**：`lpcard`/`clan_member_card` 的"
        "成员关系可由 `pilot.clan_id` 推出、`member_info` 就是我那一行 ⇒ 这三张退；"
        "`block_detail`/`friend_detail`/`friend_histories` 的列表关系（谁把谁拉进了名单）"
        "没有别的娘家 ⇒ 恢复。"),
    "行键订正理由": RESTORE_PK,
    "欠账": [
        "`mshipbid_card`：缺 bid 上下文列（`clan_id`/`ms_id`），按 `(world_id,pilot_id)` "
        "建表在同一机师竞标多台 MS 时撞行——等竞标写入方落地补 `inject_members`。",
        "`friend_histories`：写入方在服务端（战斗结束记一笔），本轮没有 CS 命令碰它。",
        "113B 列表表的卡片列（`name`/`level`/`clan_*`…）是**目标机师行的快照**（旧库即如此）。"
        "下一批可把它们降为「按 FK join `game.pilot` 派生」的列（列级派生视图机制），"
        "本轮先照旧存，保证收得到数据。",
    ],
    "机制": (
        "新增 `_overrides.json.writers` 段（`derive_homing.declared_writers`）：线体里没有"
        "实体、命令只带目标 id 的写方点名登记（命令必须存在且方向是 CS，reason 必填）。"
        "没有这一节，「0 CS 写方」这个负断言就是不完整的——它只证明了「没有命令带这个"
        "复合体」，没证明「没有命令在写这份行集」。"),
}


def main() -> int:
    ov = json.loads(OV.read_text(encoding="utf-8"))

    for g in ov.get("fold") or []:
        if isinstance(g, dict) and g.get("as") == "pilot":
            g["composites"] = ["pilot", "pilots_list", "pcard"]
            g["reason"] = FOLD_REASON

    disp = ov.setdefault("disposition", {})
    for oid, spec in DISPOSITIONS.items():
        disp[oid] = spec

    pk = ov.setdefault("pk", {})
    for oid in RESTORE_PK:
        pk[oid] = ["pilot_id"]

    nw = ov.setdefault("no_writer", {})
    for oid in ("block_detail", "friend_detail", "friend_histories",
                "mshipbid_card"):
        nw.pop(oid, None)

    ov["writers"] = WRITERS

    rows = [r for r in (ov.get("retire_tables") or []) if isinstance(r, dict)]
    kept = [r for r in rows if str(r.get("table")) not in RETIRE_UNDO]
    dropped = [str(r.get("table")) for r in rows if str(r.get("table")) in RETIRE_UNDO]
    ov["retire_tables"] = kept

    reviewed = ov.setdefault("reviewed", {})
    reviewed["batch_18_list_family_correction"] = BATCH_NOTE

    OV.write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n",
                  encoding="utf-8")
    print(f"fold[pilot].composites -> pilot/pilots_list/pcard")
    print(f"disposition += {sorted(DISPOSITIONS)}")
    print(f"pk += {sorted(RESTORE_PK)}")
    print(f"no_writer -= {sorted(RETIRE_UNDO) and ['block_detail','friend_detail','friend_histories','mshipbid_card']}")
    print(f"writers = {sorted(WRITERS)}")
    print(f"retire_tables 撤回 {dropped}（剩 {len(kept)} 条）")
    print("reviewed.batch_18_list_family_correction 已写")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

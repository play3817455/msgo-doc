#!/usr/bin/env python3
"""批 21：氏族链首批（建队 + 自身战队信息）暴露的模型缺口——**氏族内职务**。

缺口：`CS-0xCBD9-clan_subleader_set(pilot_id_sub, is_set, clan_kind)` 的 `is_set`
（1=设 / 0=撤，写线 `0xBA0547`）要求服务端**记住**「谁是本族副队长」，
而 `SC-0x8E92-clan_info_get_self_r` / `SC-0x5800-clan_info_get_other_r` 都要把它
回成 `subleader[]`（元素 113B `member_info`，**上限 4**：`cmp …,4` @`0xB6BE88` /
@`0xB624A3`，元素读取器 `sub_B43100` @`0xB6BEC0`）。全模型里没有一列承载它：

  * `pilot.rank` 是**排名**（`pilotcard_get_r` 的 `rank` @`0xB43079`，meaning=排名），不是职务；
  * `member.is_leader` 是**房间队长**（`SC-0x6B15 btlroom_member_detail_get_r`，52B 房间成员）；
  * `clan` / `cinfo` 都没有职务列。

裁决（用户 2026-09-23 选定 N1）：注入到 `cinfo`——
  * `cinfo` 是**每成员一份的「我的战队视图」**（scope `(world_id, pilot_id)`，单行，
    两个读方 `0x8E92`/`0x5800` 都从成员行取 clan 级信息），职务挂这里与
    `clan_member_card`/`member_info` 的 `DERIVED` 裁决（成员关系由 `pilot.clan_id` 推演）
    不冲突：成员身份仍在 `pilot.clan_id`，只多一列「我在这族的职务」；
  * 不建 `game.clan_member`：那会给同一份成员关系再开一个家（同一事实两处写）；
  * 不注入 `pilot`：`pilot` 是折叠族的宿主线形（`pcard` 398B），线上无此字段，
    注入列进不了线体；
  * 枚举只取 0/1：**氏族长不在这列**——`clan.leader_pilot_id` 已单点承载
    （`leader_change` 的 `pilot_id_new`），写 2=leader 会造出两个真相。

用法：python tools\\_apply_batch21.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OV_PATH = TOOLS.parent / "schema" / "homing" / "_overrides.json"


def main() -> int:
    ov = json.loads(OV_PATH.read_text(encoding="utf-8"))

    ov.setdefault("inject_members", {})["cinfo.clan_pos"] = {
        "wire_type": "u8",
        "meaning": (
            "氏族内职务：0=普通成员、1=副队长。**氏族长不在这列**——"
            "`clan.leader_pilot_id` 单点承载（避免同一事实两个真相）"
        ),
        "role": "attribute",
        "evidence_va": "0xBA0547|0xB6BE88|0xB624A3|0xB6BEC0",
        "basis": (
            "线上没有这一列，但两端的命令都要求它存在："
            "① **写侧** `CS-0xCBD9-clan_subleader_set(pilot_id_sub, is_set, clan_kind)` —— "
            "`is_set` 是 **1=设 / 0=撤**（写线 `0xBA0547`，`pilot_id_sub` @`0xBA052C`），"
            "配对应答 `SC-0x52A2` 把 `pilot_id_sub`+`is_set` 原样回显 ⇒ 服务端必须把「谁是副队长」存下来；"
            "② **读侧** `SC-0x8E92-clan_info_get_self_r` 与 `SC-0x5800-clan_info_get_other_r` 都以 "
            "`subleader[]`（元素 113B `member_info` = `lpcard` 同构卡）下发副队长列表，**上限 4**"
            "（`cmp …,4` @`0xB6BE88` / @`0xB624A3`，元素读取器 `sub_B43100` @`0xB6BEC0`）；"
            "③ **为什么没有娘家**：`pilot.rank` 是**排名**（`SC-0xB4B6-pilotcard_get_r` 的 `rank` "
            "@`0xB43079`，meaning=排名）；`member.is_leader` 是**房间队长**"
            "（`SC-0x6B15-btlroom_member_detail_get_r` 的 52B 房间成员），都不是氏族职务；"
            "`clan`/`cinfo` 与两张 113B 卡（`member_info`/`clan_member_card`）都没有职务列。"
            "**为什么挂 `cinfo` 而不是 `pilot`**：`cinfo` 就是「每成员一份的我的战队视图」"
            "（scope `(world_id, pilot_id)`、单行、旧库 `uq_game_cinfo` 逐列一致），"
            "查某族的副队长 = `WHERE clan_id=X AND clan_pos=1` 筛成员行；而 `pilot` 是折叠族的"
            "宿主线形（`pcard` 398B），线上没有这个字段，注入列进不了线体（同批 17 的 "
            "`model_unreachable` 一类）。**为什么不建 `game.clan_member`**：成员关系已由 "
            "`pilot.clan_id` 推演（batch_17 裁决把 `clan_member_card`/`member_info`/`lpcard` 判 "
            "`DERIVED`），再开一张表等于同一份关系两个家。**为什么不写 2=leader**："
            "`clan.leader_pilot_id`（来自 `CS-0x25A0-clan_leader_change` 的 `pilot_id_new`）已是"
            "单点真相，`cinfo.leader_id` 只是它的视图副本（本轮不动重复列）。"
        ),
    }

    ov.setdefault("reviewed", {})["batch_21_clan_pos"] = {
        "what": "氏族内职务（副队长）注入 `cinfo.clan_pos`（0=成员 / 1=副队长），氏族长仍由 `clan.leader_pilot_id` 单点承载",
        "why": (
            "氏族链首批（`clan_create` + `clan_info_get_self`）要装配 `0x8E92` 的 "
            "`leader[]`/`subleader[]` 两个数组，这才暴露「职务」全模型无落点："
            "`CS-0xCBD9-clan_subleader_set` 的 `is_set`（1=设/0=撤，`0xBA0547`）必须被记住，"
            "而 `0x8E92`/`0x5800` 各自以 `subleader[]`（≤4）回下来。"
            "三处候选（`cinfo` / `pilot` / 新建 `clan_member`）里取 `cinfo`："
            "它是每成员一份的战队视图，职务与 `clan_id` 同处一行，且不打断「成员关系由 "
            "`pilot.clan_id` 推演」的既有裁决；`pilot` 是折叠宿主线形（注入列进不了线体），"
            "`clan_member` 会给同一份关系开第二个家。枚举只留 0/1，是因为 `clan.leader_pilot_id` "
            "已经把「谁是族长」单点说清了（`leader_change.pilot_id_new`），"
            "再写一个 2=leader 就出现两个真相。"
        ),
        "evidence": [
            "CS-0xCBD9-lounge-clan_subleader_set：pilot_id_sub(u32)@0xBA052C / is_set(u32，1=设0=撤)@0xBA0547 / clan_kind(u8)@0xBA054F",
            "SC-0x52A2-lounge-clan_subleader_set_r：result + pilot_id_sub + is_set + clan_kind（原样回显）",
            "SC-0x8E92-lounge-clan_info_get_self_r：subleader_count(u32，上限 4，`cmp [esp+…],4; ja` @0xB6BE88) + subleader[](113B member_info，读取器 sub_B43100 @0xB6BEC0)",
            "SC-0x5800-lounge-clan_info_get_other_r：同形 subleader[]（上限 4 @0xB624A3）",
            "SC-0xB4B6-lounge-pilotcard_get_r：pilot.rank = 排名 @0xB43079（排除「rank 就是职务」）",
            "SC-0x6B15-lounge-btlroom_member_detail_get_r：member.is_leader = 房间队长（52B 房间成员，排除）",
        ],
    }

    OV_PATH.write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OV_PATH}")
    print("  inject_members =", [k for k in ov["inject_members"] if not k.startswith("_")])
    print("  reviewed.batch_21_clan_pos =", "cinfo.clan_pos" in ov["inject_members"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

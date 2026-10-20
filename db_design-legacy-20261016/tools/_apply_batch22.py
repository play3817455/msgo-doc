#!/usr/bin/env python3
"""批 22：氏族级写命令族（S1.5）暴露的两处模型缺口 —— `cinfo` 与 `pilot` 的写方。

背景：`_overrides.json.new_objects.clan` 已经把 `clan` 的 7 条写方点名列全
（`clan_create`/`clan_leave`/`clan_npc_update`/`clan_emblem_update`/
`clan_text_offer_set`/`clan_text_notice_set`/`clan_leader_change`），
但另外两张**被这些命令顺手写的表**在模型里是「0 写方」：

  * `game.cinfo`（`writes: []`）—— 它没有自己的 CS 命令：行是「我的战队视图」，
    由 `clan_create` 建、`clan_subleader_set` 改职务、`clan_leave`/`clan_kick_member` 清。
    引擎认不出来是因为这些命令的线体里**没有 639B cinfo 结构**（它们按 id 定位单行）。
  * `game.pilot`（原来只有 `pilot_create`）—— `clan_name`/`clan_emb_base|parts1|parts2`
    是**副本列**，由氏族级命令刷（`emblem_update` 换徽章后，别人看你的卡片走的就是
    这一行）。**fan-out 是必须的**：159B `pilot` 视图经 7 条 SC 下发他人卡片
    （`pilotcard_get` / `pilot_list_get` / `channellobby_members_get` / `party_member_add` /
    `dailycup_team_info_get` / `roomlobby_pilot_add` / `pilot_create_r`），
    读路径没有 clan 行可 overlay。

裁决（用户 2026-09-23 选定「A：刷副本」+「8 条 CS 全做」）：
  * `clan` 是氏族属性的**唯一权威**；
  * `pilot.clan_name` / `pilot.clan_emb_*` 是**fan-out 副本**（写路径刷，读路径不 overlay）；
  * `cinfo` 的 clan 级列（`clan_name`/`emb_*`/`leader_id`/`notice_body`/`npc_id`/
    `offer_is_active`/`level`）是**视图缓存**：读路径用 `clan` 覆盖
    （`clan_info_get_self` 的 overlayClanInto），写路径**只动身份与职务两处**
    （`clan_id` / `clan_pos`）；
  * `pilot_detail.clan_id` 与另两处一样是身份副本，随成员进出一起清。

用法：python tools\\_apply_batch22.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OV_PATH = TOOLS.parent / "schema" / "homing" / "_overrides.json"

# 「我的战队视图」的四个写方（identity / 职务 / 两只清成员）
CINFO_WRITERS = [
    "CS-0xA5BC-lounge-clan_create",
    "CS-0xCBD9-lounge-clan_subleader_set",
    "CS-0x0038-lounge-clan_leave",
    "CS-0xE1DB-lounge-clan_kick_member",
]

# 刷 `pilot` 副本列的四条（含建族与两只清成员）
PILOT_COPY_WRITERS = [
    "CS-0xA5BC-lounge-clan_create",
    "CS-0x979C-lounge-clan_emblem_update",
    "CS-0x0038-lounge-clan_leave",
    "CS-0xE1DB-lounge-clan_kick_member",
]

CINFO_REASON = (
    "`cinfo` 没有自己的 CS 命令：每一行是「我的战队视图」，由氏族链的四条命令按 "
    "`(world_id, pilot_id)` 定位单行写 —— `clan_create` 建建族者那行"
    "（`clan_id`/`clan_name`/`leader_id`/`clan_pos=0`，权限证据：命令 `CS-0xA5BC` "
    "@`0xB9F902`/`0xB9F8C8`）、`clan_subleader_set` 按 `pilot_id_sub` 改目标行的 "
    "`clan_pos`（1=设 / 0=撤，`is_set` @`0xBA0547`）、`clan_leave`（@`0xB9FB5C`，带 "
    "`clan_id`+`clan_kind`+`is_GMtool`）与 `clan_kick_member`（`pilot_id_kick` "
    "@`0xBA1499`）清掉对应行的氏族列。引擎认不出来的原因很直接：这四条命令的线体里"
    "都没有 639B 的 `cinfo` 结构（它们是按 id 定位单行），所以「线体携带」的口径"
    "看不见它们，只能点名登记。"
)

PILOT_REASON = (
    "只针对 `pilot` 的**氏族副本四列**（`clan_name` / `clan_emb_base` / `clan_emb_parts1` / "
    "`clan_emb_parts2`）——不是整行写方（整行由 `pilot_create` 与 `pilot_rename` 一族管）。"
    "为什么必须刷：159B `pilot` 视图经 7 条 SC 下发给**别人看你的卡片**"
    "（`SC-0xB4B6-pilotcard_get_r` / `SC-0xE13A-pilot_list_get_r` / "
    "`SC-0x1D02-channellobby_members_get_r` / `SC-0x510F-party_member_add` / "
    "`SC-0x8669-dailycup_team_info_get_r` / `SC-0xBDD6-roomlobby_pilot_add` / "
    "`SC-0xC43C-pilot_create_r`），这些读路径手里没有 `clan` 行可 overlay ⇒ 不刷就是"
    "「族长换了徽章，别人的机师列表里自己还是旧徽章」。写侧证据：`clan_create` "
    "（`clan_name` @`0xB9F8CE`）、`clan_emblem_update`（`emb_base` @`0xBA076C` / "
    "`emb_parts1` @`0xBA078B` / `emb_parts2` @`0xBA078D`，一次 UPDATE 刷该 clan_id 的全部 "
    "`pilot` 行）、`clan_leave` @`0xB9FB5C` 与 `clan_kick_member` @`0xBA1499`（清成 0/空）。"
)

BATCH22_REVIEWED = {
    "what": (
        "氏族级写命令族（S1.5，8 条 CS）落库口径：`clan` 权威 + `pilot` 副本 fan-out + "
        "`cinfo` 视图缓存（读时 overlay）+ `cinfo.clan_pos` 手写读写"
    ),
    "why": (
        "上一批只落了建族与自身视图，`clan` 那 15 列里除 5 列外都还没有写方；"
        "这一批把 8 条 CS（`clan_subleader_set` / `clan_leader_change` / `clan_emblem_update` / "
        "`clan_text_offer_set` / `clan_text_notice_set` / `clan_npc_update` / `clan_leave` / "
        "`clan_kick_member`）一次补齐，必须先定「同一事实的四处副本谁说了算」，否则每条命令"
        "都要各写一遍："
        "① `clan` 行 = 权威（氏族级属性只写这里，读时由 `clan_info_get_self` 覆盖 `cinfo` 副本）；"
        "② `pilot.clan_name`/`clan_emb_*` = fan-out 副本（159B 视图给别人看卡片，7 条 SC 发出去，"
        "读路径没有 clan 行 ⇒ 写路径刷）；"
        "③ `cinfo` 的 clan 级列 = 视图缓存（读时 overlay，写路径只动 `clan_id`/`clan_pos`，"
        "避免写放大到每个成员行）；"
        "④ `pilot_detail.clan_id` = 身份副本（成员进出时与另两处一起清）。"
        "欠账（不在本批）：`clan_level_update`（`SC-0x68D7`）只有 S→C，`lv`/`deckcost` 的"
        "写方（氏族经验 / 楼阁点链）未取证 ⇒ 本轮不实现也不凭空发通知；`cinfo.member_max` 可由 "
        "`cfg.LVUP_CLAN[lv].member_cap` 推出（读路径取值，不落写方）；建族 GP 费用（`-13019`）"
        "价目出处未取证；副队长是否有管理权（踢人/改公告）未取证，本轮一律按「仅族长」。"
    ),
    "evidence": [
        "CS-0xCBD9-clan_subleader_set：pilot_id_sub@0xBA052C / is_set(1=设0=撤)@0xBA0547 / clan_kind@0xBA054F；应答 SC-0x52A2 原样回显",
        "CS-0x25A0-clan_leader_change：pilot_id_new@0xBA0B66 / pilot_name_new@0xBA0B6E / clan_kind@0xBA0B88；应答 SC-0xB2ED",
        "CS-0x979C-clan_emblem_update：emb_base@0xBA076C / emb_parts1@0xBA078B / emb_parts2@0xBA078D；应答 SC-0x6FF7",
        "CS-0x55D6-clan_text_offer_set：is_active@0xBA0FE6 / subj@0xBA0FEE / body@0xBA100A / clan_kind@0xBA1024；读侧槽 49/31（SC-0x5F72@0xB64075/@0xB64096）",
        "CS-0xC59B-clan_text_notice_set：body@0xBA0DC6 / clan_kind@0xBA0DEB；读侧槽 433（SC-0x8E92@0xb45af6）",
        "CS-0x0562-clan_npc_update：npc_id@0xBA09A4；应答 SC-0x15B5",
        "CS-0x0038-clan_leave：clan_id@0xB9FB5C / clan_kind@0xB9FB75 / is_GMtool@0xB9FB7D；应答 SC-0x1600（13B，带 deckcost）",
        "CS-0xE1DB-clan_kick_member：pilot_id_kick@0xBA1499 / clan_kind@0xBA14A5；应答 SC-0x924C",
        "客户端 error_code.csv クラン段：-13001 不明なクランID / -13010 権限が無い(クラン管理系) / -13013 サブリーダー多すぎ / -13017 BC不足(エンブレム変更、上官NPC変更) / -13022 既にクランメンバーではない",
        "srv.chargepoint_price：clan_emblem=200 / clan_npc=300（来源 SC-0x9397@B6D20C / @B6D236，消费方在本批落地）",
        "cfg.LVUP_CLAN：clan_level(主键) + member_cap（成员上限）+ deck_cost_level（读表 sub_579960）",
    ],
}


def main() -> int:
    ov = json.loads(OV_PATH.read_text(encoding="utf-8"))

    writers = ov.setdefault("writers", {})
    writers["cinfo"] = {
        "commands": CINFO_WRITERS,
        "evidence_va": "0xB9F902 / 0xBA0547 / 0xB9FB5C / 0xBA1499",
        "reason": CINFO_REASON,
    }
    writers["pilot"] = {
        "commands": PILOT_COPY_WRITERS,
        "evidence_va": "0xB9F8CE / 0xBA076C / 0xB9FB5C / 0xBA1499",
        "reason": PILOT_REASON,
    }

    ov.setdefault("reviewed", {})["batch_22_clan_writes"] = BATCH22_REVIEWED

    OV_PATH.write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OV_PATH}")
    print("  writers keys =", sorted(k for k in writers if not k.startswith("_")))
    print("  reviewed.batch_22_clan_writes =", "batch_22_clan_writes" in ov["reviewed"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

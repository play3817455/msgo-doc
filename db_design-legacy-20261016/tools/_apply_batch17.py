#!/usr/bin/env python3
"""临时：把 batch_17（no_writer 收口）的裁决写进 `_overrides.json`。

写完即删（裁决内容留在 `_overrides.json.reviewed.batch_17_no_writer_closure` 里）。
"""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "schema" / "homing" / "_overrides.json"

FOLD_GROUP = {
    "composites": [
        "pilot", "pilots_list", "pcard", "lpcard", "block_detail",
        "clan_member_card", "friend_detail", "friend_histories", "member_info",
        "mshipbid_card",
    ],
    "as": "pilot",
    "reason": (
        "十个线布局是**同一个「机师」实体**（自己的/别人的名片）的详略形，折叠成一张："
        "`pcard` 与 `pilots_list` 成员名序/偏移/总长**逐字节相同**（58 成员 / 398B / 同一 offset 序列），"
        "`pilot`（24 成员 / 159B）与 `lpcard` 族（113B，20 成员）的成员都是它的真子集，"
        "而「行」始终是机师本身。见 reviewed.batch_17_no_writer_closure。"
    ),
}

# 并表（折叠）的 9 个：`_overrides.json.disposition` 里**不写**（对象会被折叠掉，写了会
# 变成「订正指向不存在的对象」的噪声）；逐条理由记在 batch_17 的「并表明细」里。
FOLDED_VERDICTS: dict[str, str] = {
    "block_detail": (
        "他人卡片族的第 2 张线形（= `lpcard` 113B，20 成员同名同序）：`block_list_get_detail_xworld_r`"
        "下发**屏蔽名单里那几名机师**的轻量名片（行属于别人）。0 CS 写方，scope 只有 `(world_id, 我)`——"
        "`LpcardRow` 里 scope 的 `PilotID`（我）与前缀化的线字段 `LpcardPilotId`（对方）并存，正是 §9.3 的静默压行。"
    ),
    "friend_detail": (
        "他人卡片族（= `lpcard` 113B）：`friend_search_r` / `friend_list_get_detail_r` / "
        "`friend_xworld_search_r` 下发的都是**好友/被搜到的机师**名片。行属于别人，0 CS 写方。"
    ),
    "friend_histories": "他人卡片族（= `lpcard` 113B）：`friend_history_get_xworld_r` 下发「最近一起玩过的机师」名片。行属于别人，0 CS 写方。",
    "lpcard": "他人卡片族的规范形（113B）：`clan_memberlist_get_r` 下发战队成员名片。行属于别人，0 CS 写方。",
    "member_info": "他人卡片族（= `lpcard` 113B）：`clan_info_get_self_r` 里的「我的卡片」也是同一张线形（自己=行仍是机师）。",
    "mshipbid_card": "他人卡片族（= `lpcard` 113B）：`clan_mshipbid_get_list_r` 里竞标者名片。行属于别人，0 CS 写方。",
    "clan_member_card": "他人卡片族（= `lpcard` 113B）的**孪生根**：与 `lpcard` 成员名序完全相同，只是读命令不同（`clan_info_get_other_r`）。同一张线形不留两张表。",
    "pcard": (
        "机师实体（名片形，398B，58 成员）：`pilotcard_get_r` 下发的名片就是 `pilot` 那一行的另一条线形。"
        "旧库把它与 `tbl_pilots_list`/`tbl_pilot`/`tbl_pilot_detail` 并列为四张机师表（docs/05 §1 第 1 项）。"
    ),
    "pilots_list": (
        "机师实体（名片形，398B）：`pilot_list_get_r` 的 `pilots_eff`/`pilots_zeon` 两格是**我两个阵营的机师**，"
        "与 `pcard` 逐字节同形——折叠后 `rec_*`/`score_*`/`last_in`/`state_bits` 一族（30 列）落进 `game.pilot`。"
    ),
}

DISPOSITIONS: dict[str, dict[str, str]] = {
    # ---- DERIVED：行在别的根表 / 排行查询结果 / 运营主数据的读视图 ----
    "bmgpack": {
        "as": "DERIVED",
        "reason": (
            "商店在售商品的**读视图**（23B 元素，与 `item_list` 同一打印器 `sub_B4E110`、同一组列 "
            "`shopitem_id`+`gp_x01/gp_x10/cp_x01/cp_x10`+`bit_eff`+`stock`）：`pilot_list_get_r` 里下发的是"
            "「BGM 包在售清单」，主数据与价格/库存是运营态（`srv.shop_lineup` 一类），`bmgpack.shopitem_id`"
            "本来就被判为指向主数据的 `master` 引用。0 CS 写方 ⇒ 不成玩家维度表。"
        ),
    },
    "item_list": {
        "as": "DERIVED",
        "reason": (
            "商店在售商品（23B 元素）：`shop_lineup_r` 下发「道具店在售清单」，与 `bmgpack` 同形同打印器、"
            "只是商店不同（`batch_02_fold` 说它们「布局全等但域不同」——对，两个货架）。"
            "价格/库存是运营态（主数据侧），0 CS 写方 ⇒ 本轮不成 `game.*` 表。"
        ),
    },
    "coop_room": {
        "as": "DERIVED",
        "reason": (
            "房间列表的读视图：15 个成员名与根对象 `roominfo` 逐个相同（= `roominfo` 的线形），"
            "`btlroom_coop_roomlist_get_r` 下发的是「协同房列表」。房间本体的家在 `roominfo`，"
            "0 CS 写方 ⇒ 不成第二张房表。"
        ),
    },
    "dcpoint_detail": {
        "as": "DERIVED",
        "reason": (
            "结算面板里的**差值投影**：5 个成员名与根对象 `dc_point` 逐个相同"
            "（`bef_dcpoint`/`aft_dcpoint`/`is_dc`/`reward_item_ids`/`reward_item_nums`），"
            "`result_info` 是那场结算的回执。DC 点数的家是 `dc_point`（每个机师一行），"
            "0 CS 写方 ⇒ 不成第二张表。"
        ),
    },
    "extrarule_xwar_info": {
        "as": "DERIVED",
        "reason": (
            "大规模战扩展规则的**战斗侧副本**：7 个成员名与根对象 `xwar_ext_rule` 逐个相同（514B 同形），"
            "`battle-authenticate_r` 只是把开局参数回给客户端。真正的家在 `xwar_ext_rule`（机师预约选项，"
            "本批判单行保留）。"
        ),
    },
    "favms_add": {
        "as": "DERIVED",
        "reason": (
            "**同一批行的结算增量形**：18 个成员名与元素复合体 `favms` 逐个相同，而行本身是"
            "`pilot_detail.favms_arr`（720 格，子表 `game.pilot_detail__favms_arr` 存 18 列）的元素。"
            "`result_info` 下发的是这一场加在哪几台机体上。行已有着落 ⇒ 不另建表。"
        ),
    },
    "ranking": {
        "as": "DERIVED",
        "reason": (
            "排行项的**查询投影**（12 成员：`rank`/`score`/`pilot_id`/`clan_*`/`emb_*`/`avatar`/`level`/`troops`）："
            "`ranking_pilot_get_r` 按分数排序取头部，名次与分数是查询时算出来的，不是机师的源数据列"
            "（`pilot`/`pilot_detail` 里没有 `score` 这一列）。0 CS 写方 ⇒ 不落库。"
        ),
    },
    "toppilots": {
        "as": "DERIVED",
        "reason": "排行项：与 `ranking` 成员名序完全相同（孪生根），同一条 `ranking_pilot_get_r` 的「榜首」窗口。判同上。",
    },
    "rank_pilot": {
        "as": "DERIVED",
        "reason": (
            "精英排行的查询投影（18 成员）：`ranking_elite_pilot_get_page_r` / 赛季命令。"
            "`is_regular`/`is_reserve`/`last_rank`/`last_score`/`season_class_lv`/`tm_upd` 是**赛季态**"
            "（`season_class_lv` 与 `pilot_detail.sc_lv_max` 同族；`msdeck` 是卡组引用，见 ref_stem 的 `msdeck` 一族），"
            "由赛季/排行服务按届算，不是机师行上的源列。0 CS 写方 ⇒ 不落库。"
        ),
    },
    "rank_pilot_light": {
        "as": "DERIVED",
        "reason": "精英排行轻量项（7 成员，`rank_pilot` 的子集）：同上，查询投影（含 `season_class_lv` 赛季态）。",
    },
    "team_pilot": {
        "as": "DERIVED",
        "reason": "赛季队伍成员（5 成员：`pilot_id`/`name`/`level`/`avatar`/`world_id`）全是机师列，行=机师；队伍成员关系在 party 侧，0 CS 写方 ⇒ 查询投影。",
    },
    "invite": {
        "as": "DERIVED",
        "reason": (
            "「可邀请机师」的**分页查询结果**（`invite_count` + `page_now`/`page_max` + `sort_info`）："
            "行=机师（`pilot_id`/`name`/`rank`/`mil_class`），`continued_login_days`/`is_bonus`/`vslocal_cnt`/`xwar_cnt`"
            "是筛选/加成用的**算出来的**值（连续登录天数、场次计数），`last_login`/`last_logout` 与 "
            "`pilot` 侧时间列同族（列名变体，留给 colname 批次）。0 CS 写方 ⇒ 不落库。"
        ),
    },
    "leaders": {
        "as": "DERIVED",
        "reason": (
            "招募列表里的「队长条目」（7 成员）：行=机师（`pilot_id`/`name`/`level`/`avatar`/`rate_vslocal`），"
            "`is_leader`/`pstat` 是**队伍成员关系属性**，家在 `party_member`（本模型已有该表的同名成员）。"
            "0 CS 写方 ⇒ 不落库。"
        ),
    },
    "member": {
        "as": "DERIVED",
        "reason": "房间成员条目（7 成员，与 `leaders` 同形）：行=机师，`is_leader`/`pstat` 是成员关系属性（`party_member` 有同名成员）。0 CS 写方 ⇒ 不落库。",
    },
    # ---- EVENT：战斗期数组 ----
    "funnel_snapshot_entry": {
        "as": "EVENT",
        "reason": "战斗期快照元素（`ent_id`/`move_info`/`wslot_idx`）：孪生根 `funnelss` 已判 EVENT（同一场战斗的位置快照），0 CS 写方 ⇒ 不落库。",
    },
    "mapgimmick_entry": {
        "as": "EVENT",
        "reason": "战斗地图机关（`game_begin` 下发 23 列：`ent_id`/`ctrl_ent_id`/`gauge_max`/`msma_id*`/`param_*`/坐标）：服务端每场重算，0 CS 写方 ⇒ 不落库（同 `fire_point` 先例）。",
    },
    "parts_exec_entry": {
        "as": "EVENT",
        "reason": "战斗部件效果执行（`eqparts_execute` 下发 6 列：`effect_catego`/`effect_msec`/`effect_param`/`effect_value*`/`item_id`）：一场内的执行记录，0 CS 写方 ⇒ 不落库。",
    },
    "respawn_post": {
        "as": "EVENT",
        "reason": "战斗重生点进度（`game_respawn_post_update` 下发 9 列：`gauge_A/B`/`conquer_remain_sec`/`is_keep`/`is_visible`/`near_ms_num`/`team`…）：每场战斗的实时进度，0 CS 写方 ⇒ 不落库。",
    },
    "respawn_post_entry": {
        "as": "EVENT",
        "reason": "战斗重生点初始形（`game_begin` 下发 16 列：坐标/`group_id`/`npc_ba_point_*`/`param1/2`）：与 `respawn_post` 同族的战斗期数组，0 CS 写方 ⇒ 不落库。",
    },
    "result_detail": {
        "as": "EVENT",
        "reason": "战斗结算详情（`result_info` 下发 80 列：`badge_*`/`fight_ms_*`/`expup_*`/`moneyup_*`/`itm_*`/`cnt_*`…）：一场的战斗回执，属于 B6 的战斗持久化议题（docs/05 §4.C/§9），0 CS 写方 ⇒ 本轮不落库。",
    },
    "result_wave": {
        "as": "EVENT",
        "reason": "波段结果元素（10 列）：`wave_res`（同族，已判 EVENT）的结算窗口，同属战斗回执，0 CS 写方 ⇒ 不落库。",
    },
    "score_ranking": {
        "as": "EVENT",
        "reason": "战果排行项（`result_info` 下发 19 列：`kill_cnt`/`atk_point`/`con_point`/`spt_point`/`last_msma`/`last_weapon`…）：一场的得分榜，0 CS 写方 ⇒ 不落库。",
    },
    "support_spot": {
        "as": "EVENT",
        "reason": "战斗支援地点（`commander_support_spot_notice` 下发 11 列：`route_no`/`pos_*`/`dir`/`team`/`stat`/`ai_priority`）：一场的指挥官指令目标，0 CS 写方 ⇒ 不落库。",
    },
    # ---- CONFIG ----
    "bonus_event": {
        "as": "CONFIG",
        "reason": (
            "**运营配置**：`bonus_event_now_update` 下发当期加成活动日程（`game_type`/`begin_time`/`end_time`/"
            "`main_priority`/`accump_rate`/`gp_rate`/`moneyup_rate`/`raredrop_rate`/`reward_num`…），"
            "按世界（或全服）一份、由运营排期，不是玩家状态。13 个费率/日程列在所有保留表里都没有娘家，"
            "也不该有——这属于 `srv.*` 运营态（本轮不建 `game.bonus_event`）。"
        ),
    },
    # ---- TBD：本轮不建表，欠账写清 ----
    "activity": {
        "as": "TBD",
        "reason": (
            "部队公告条目（13 列：`msg` char[241]/`timestamp` char[24]/`send_range`/`is_admin` + 发送者与战队副本）。"
            "0 CS 写方（`CS-0x0680-activity_request` 是**空请求**，只要列表），且没有自己的条目 id"
            "（`timestamp` 是显示文本）——`msg`/`timestamp`/`send_range`/`is_admin` 四列在所有保留表里无娘家。"
            "**欠账**：等公告写入方落地（服务端/运营发公告）时必须先补一列条目 id（`inject_members`），再建表。"
        ),
    },
    "comment": {
        "as": "TBD",
        "reason": (
            "留言板评论条目（10 列：`msg_id`/`parent_msgid`/`body`/`date`/`nice_count`/`is_niced`/发送者副本）。"
            "写方其实已有（`CS-0x45E3-clan_msgboard_msg_insert` 发帖/回复，模型里落给了 `news`），"
            "但**没有自己的条目 id**（`is_niced`/`parent_msgid` 两列在保留表里无娘家）。"
            "**欠账**：接「发评论」写入方时用 `inject_members` 补留言 id，再按 (world_id, msg_id, 留言 id) 建表。"
        ),
    },
    "pbadge": {
        "as": "TBD",
        "reason": (
            "我方徽章持有数（`pilot_record_get_r` 里的 `array<pbadge,3>`，每格 152B = 38 个 u32 计数）。"
            "行身份是**槽序**（3 格），线上没有 id 列；0 CS 写方。**欠账**：写入方落地时按"
            "「根对象 + 合成槽序（elem_index）」补机制——引擎目前只给**子表**生成 `elem_index`，"
            "根对象带合成元素下标还没有先例（`unlockw` 是靠线里的 `db_index` 才成根的），"
            "引擎要不要开这个口子另议。"
        ),
    },
}

SINGLETON = {
    "lvjudge_hist": (
        "我方**等级判定履历**（369B，8 列：`lv_history[24]`/`lv_history_num`/`lv_history_max`/"
        "`term_old[25]`/`termstr_now`/`xwarwin_history[24]`/`xwarlose_history[24]`/`pilot_id`）："
        "每个机师一份、随赛季推进更新（读方 `pilot_record_get_r`），键形状 `(world_id, pilot_id)` 正确，"
        "与 `precord`（战绩）、`pilot_detail`（我方详情）同类。本批**保留表**，只把它从 `no_writer` 挪到 `singleton`。"
    ),
}

BATCH17 = {
    "verdict": "machine_adjudicated (待用户确认)：35 个 `no_writer` 根逐条裁决 —— 8 个并进 `pilots_list`/`pcard`/`lpcard` 族的折叠，13 个 `DERIVED`，9 个 `EVENT`，1 个 `CONFIG`，3 个 `TBD`，1 个改判 `singleton`；孪生根 `clan_member_card`/`item_list` 连带收口。",
    "口径": (
        "用户批准的三条：① 「0 CS 写 + 行可派生 ⇒ 不建表」（`DERIVED`/`EVENT`/`CONFIG`，`no_table_reason` 写明欠账）；"
        "② 孪生根连带收口（否则同一张线形里留一张无主表）；③ 存疑对象先取证再判。"
        "本批**没有**「丢列」：判 `DERIVED` 前先跑「成员名 → 保留表宿主」全量比对（`tools/_q_nw_cols.py` 口径），"
        "凡有列无娘家的一律走折叠（并表）而不是退表。"
    ),
    "取证_六问": {
        "bmgpack↔item_list": (
            "**同一批行？不是同一批——是两个货架，但同为运营主数据的读视图。** 两个元素都是 23B、"
            "同一打印器 `sub_B4E110`、同一组 7 列（`shopitem_id`+`gp_x01/gp_x10/cp_x01/cp_x10`+`bit_eff`+`stock`），"
            "差别只在读命令（`pilot_list_get_r` 下 BGM 包货架 / `shop_lineup_r` 下道具货架）与 `stock` 的偏移"
            "（bmgpack 22 / item_list 21，内存对齐差 1B）。价格与库存是运营态，`shopitem_id` 已被判 `master` 引用 ⇒ "
            "两张表都退，主数据侧才是家。"
        ),
        "pbadge": (
            "**不是 `precord` 的列**：`pilot_record_get_r` 的报文体里 `precord`(242B) 与 `pbadge`(456B = 3×152) "
            "是并列字段，`pbadge` 的 3 格是**徽章持有数数组**（每格 38×u32），precord 的 61 列里没有任何徽章列 ⇒ "
            "判 `TBD`（我方状态、缺身份列，等写入方与「根对象 + 合成槽序」机制）。"
        ),
        "lvjudge_hist": (
            "**不是 `precord` 的列**，也不是它的孪生：同一条报文里 `precord`/`pbadge`/`hav_medal`/`msdeck`/"
            "`lvjudge_hist`/`plvhist` 并列，`lvjudge_hist` 是 369B 独立结构（等级判定履历，含 4 个数组成员）⇒ "
            "改判 `singleton`，保留 `game.lvjudge_hist`（键 `(world_id,pilot_id)` 正确）。"
        ),
        "bonus_event": (
            "**是运营配置**：列全是日程与费率（`game_type`/`begin_time`/`end_time`/`main_priority`/各 `*_rate`/`*_offset`），"
            "`cfg` 侧现有 `MODULE_BONUS`/`MODULE_BONUS_LOT`/`MONTHLY_BONUS_REWARD`/`PLAY_BONUS_REWARD` 都不是这套日程 ⇒ "
            "判 `CONFIG`（`srv.*` 运营态），不进玩家维度。"
        ),
        "activity": (
            "**身份列不成立**：`CS-0x0680-activity_request` 无字段（空请求，只要列表）⇒ 0 CS 写方确认；"
            "13 列里只有 `timestamp`（char[24] 显示文本）与 `pilot_id`/`clan_id` 可当候选，但都不是条目号 ⇒ "
            "判 `TBD`（欠账：写入方落地时补条目 id）。"
        ),
        "invite": (
            "**身份列不成立，但行是查询结果**：`clan_invite_pilotlist_get_r` 带 `page_now`/`page_max`/`sort_info`"
            "⇒ 是分页排序查询；行=机师，`continued_login_days`/`is_bonus`/`vslocal_cnt`/`xwar_cnt` 是算出来的筛选值 ⇒ "
            "判 `DERIVED`。"
        ),
    },
    "折叠_机师名片族": (
        "本批最大的发现：十个线布局其实是**同一个「机师」实体**（`pilot` 159B 轻量形 / `pilots_list`/`pcard` 398B 名片形 / "
        "`lpcard` 族 113B 轻量名片形），而其中 8 个是 0 CS 写方、被 SC 当「（他）机师卡片/列表」下发——"
        "键只剩 `(world_id, 我)`（`*Row` 里 scope 的 `PilotID` 与前缀化的线字段 `*PilotId` 并存就是压行的痕迹）。"
        "判 `DERIVED` 退表会**丢 30 列**（`rec_*`/`score_*`/`last_in`/`state_bits`/`clan_memb_exp_use` 在所有保留表里无娘家），"
        "所以按 `batch_02_fold` 留的「按业务确认后再合」走**折叠**（`_overrides.json.fold`）："
        "十个复合体 → 一个对象 `pilot`（表仍是 `game.pilot`），列全并进去，表与 `__avatar` 子表一并退场。"
        "旧库正是把机师切成四张表（`tbl_pilot`/`tbl_pilots_list`/`tbl_pcard`/`tbl_pilot_detail`，docs/05 §1 第 1 项）。"
    ),
    "所以": (
        "本批退役：8 张并表 + 13 张 `DERIVED` + 9 张 `EVENT` + 1 张 `CONFIG` + 3 张 `TBD`"
        "（+ 孪生根 `clan_member_card` 并表、`item_list` 退表）；`lvjudge_hist` 保留（改判 `singleton`）。"
        "总表数从 126 → 约 100（含 `__avatar` 子表一并退场）。"
    ),
}


def main() -> int:
    ov = json.loads(P.read_text(encoding="utf-8"))

    fold = ov.setdefault("fold", [])
    fold.append(FOLD_GROUP)

    disp = ov.setdefault("disposition", {})
    for oid, spec in DISPOSITIONS.items():
        disp[oid] = spec

    sing = ov.setdefault("singleton", {})
    for oid, reason in SINGLETON.items():
        sing[oid] = reason
    # item_list 改判 DERIVED：原来的 singleton 裁决作废
    sing.pop("item_list", None)

    reviewed = ov.setdefault("reviewed", {})
    BATCH17["并表明细"] = FOLDED_VERDICTS
    reviewed["batch_17_no_writer_closure"] = BATCH17

    P.write_bytes((json.dumps(ov, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print("wrote", P)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# 未决问题 / 记录 —— SC-0xDC00-battle-commander_support_execute_r

- 本批（批次-14）定稿：单字段命令；容量 4 精确吻合。
- 关联：与 `0x7CD8`（commander_support_end）、`0x6D8F`（commander_support_debug_end）同族司令支援命令。
- **配对上行 = `CS-0x6486 commander_support_execute`**（15B）：`support_type(u32)｜target_xyz(3×u16)｜spt_spot_index(u8)｜val(u32)`；回执收件集 = **只回发送者**；同一条上行还播 `SC-0x6295`（全场）。
- **`support_type` 值域（已确证，见 `serverv/docs/05-战斗客户端状态机.md` §3.8）**：客户端 `CCommanderSupportTable`（`574120` 查 `0xD780B0`）：
  `0 BOMB / 1 CARPET_BOMB / 2 TENDER / 3 SEARCH / 4 MINOVSKY / 5 SOLAR_RAY / 6 SUMMON_MA / 7 SUMMON_ACE / 8 BATTLE_SHIP / 9 ASSAULT_SHIP / 10 ORATION / 11 PATROL_AIRCRAFT / 12 AAG / 13 GUNTURRET / 14..18 EQPARTS_EXEC_A..E / 19 GRENADE_NET / 20 GRENADE_TUMBLE / 21 WALL / 22 DUMMY_BEACON / 23 TRANSPORT_SHIP / 24 STGARMS_OLD / 25 STGARMS1 / 26 STGARMS2 / 27 SUBFLIGHT / 28 ASSAULT_STGHOLD / 29 RIDE_ACE / 30 JAMMING`。
- **★必须带合法 `spt_spot_index` 的类型（13 种，客户端要在地图上摆点选）**：`2/6/7/8/9/11/12/13/23/26/27/28/29`。其余（`0/1/3/4/5/25/30` 默认、`10/14..18/19/20/21/22/24` 原地）不带地点。其中 `8/9/11` 客户端额外摆一个 kind-41 路线标记（取 `0x5092` 元素 `+0x20 route_no`）。
  ⇒ 服务端校验：`support_type ∈ [0,30]`；属于那 13 种时 `spt_spot_index` 必须是最近一条 `0x5092` 内的合法下标。

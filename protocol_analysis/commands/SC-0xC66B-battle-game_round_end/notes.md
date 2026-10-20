# 未决问题 / 记录 —— SC-0xC66B-battle-game_round_end

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `progress` 线长 46 / 槽 64：读取器 `sub_B07880` 实算 46B，与打印器 `sub_B0A820` 成员偏移（末成员 `B_dot_dmg`@`+2Ch`，共 46B）完全一致。
- 成员：`remain_msec`(u32)、`coop_step`(u32)、`A_point_now`(u32)、`B_point_now`(u32)、`A_gauge_dmg_scale`(u16)、`B_gauge_dmg_scale`(u16)、`coop_dead_remain`(i8)、`is_prestart`(i8)、`rule_status`(u32)、`rule_timer_msec`(u32)、`rule_param1`(u32)、`rule_param2`(u32)、`A_dot_dmg`(u32)、`B_dot_dmg`(u32)。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。

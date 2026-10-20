# 未决问题 / 记录 —— SC-0xD1B3-battle-game_respawn_post_update

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 元素线长 25 / 槽步进 40（`sub_B05F90` 按 count 推进 0x28/槽）。
- 元素成员（读取器 `sub_B07B00` + 打印器 `sub_B0AD10`）：`team`(u16)、`troops`(u16)、`gauge_A`(u32)、`gauge_B`(u32)、`is_visible`(i8)、`is_lock`(i8)、`is_keep`(i8)、`near_ms_num`(2×u8)、`conquer_remain_sec`(f64 读原语 `sub_B06270` 步进 8)。线上字段止于 f64（结构体内 `+11h..+17h` 为填充 不上线）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。

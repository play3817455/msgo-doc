# 未决问题 / 记录 —— SC-0xE17B-lounge-beginner_challenge_get_r

- 本批（批次-14）定稿：容量 `0x1CC = 4 + 456` 精确吻合；`info` 结构 claim（456）≠ 线长（454）。
- ★元素读取器 `sub_B42440` 整函数扫描 = **454**（u32 + u16 + 32×u16 + 96×u32 = 4+2+64+384）——**循环展开必须按字面量上界**（`cmp edx,20h` / `cmp ecx,60h`），否则会把 32×u16、96×u32 只算 1 次。
- **未定案项**：`info` 内部成员未逐一命名。
- 关联：与 `0x3B34`（pilot_newpilotchallenge_get_r）、`0x6059`（check_progress_quest_r）同族挑战命令。

# 未决问题 / 记录 —— SC-0xDBBC-lounge-mission_info_update_coop

- 本批（批次-14）定稿：★**「整块定长数组」再中 3 例**（三组 `u64[4]`）：`sub_B41300` 用 `add dword ptr [edx],20h` **一次推进整块** 32B，循环上界为**字面量 4**（`cmp edi,4; jb`@`B80788`/`B807C8`/`B80808`）、**无线上 count** ⇒ `u64[4]`；容量 `0x61 = 32×3 + 1` 精确吻合。
- 同一模式此前出现于 `0x9193`/`0x91C9`（批次-11）、`0xAF02.hav_medal`（批次-12）、`0xC779.hav_emblem`/`0xCB1B.grants`（批次-13）。
- 关联：与 `SC-0xB080-lounge-mission_info_update_vs`（对战侧同族更新）对照阅读。

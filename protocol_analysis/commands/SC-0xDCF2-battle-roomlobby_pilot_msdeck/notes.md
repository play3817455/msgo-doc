# 未决问题 / 记录 —— SC-0xDCF2-battle-roomlobby_pilot_msdeck

- 本批（批次-14）定稿：容量 `0x24 = 4+4+4+4×4+4+1×4` 精确吻合（两个数组上限均由 `cmp …,4; ja` 确证为 4）。
- ★两个数组的**槽步进不同**（4 / 1）且**均无独立容量来源**，容量等式同时确证了两个上限。
- 关联：与 `SC-0xD6BC-lounge-msma_deckslot_change_r`、`SC-0xDCF2` 同属「编成/暗牌」族；与 `C→S` 侧 `roomlobby_pilot_msdeck` 请求成对。

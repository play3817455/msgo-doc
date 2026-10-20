# 未决问题 / 记录 —— SC-0xE18C-lounge-party_create_r

- 本批（批次-14）定稿：容量 `0x46 = 4 + 1 + 61 + 4` 精确吻合。
- ★**「1 字节字段 + 紧接变长串」组合**：`is_recruiting`(u8) 之后紧跟 NUL 串，后续字段偏移由串长决定（按「线序 + 长度」记录）。
- 容量抽取注意：`push 46h ; char` 行尾注释（同 `0xD784`/`0xD8E2`/`0xDBBC`/`0xE014`）。
- 关联：与 `0xE18C`（创建）配对的 `0x1E49`（party_enter_r）、`0x2D6F`（btlroom_create_r）同族房间创建命令。

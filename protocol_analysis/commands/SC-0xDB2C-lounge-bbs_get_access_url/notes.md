# 未决问题 / 记录 —— SC-0xDB2C-lounge-bbs_get_access_url

- 本批（批次-14）定稿：与 `SC-0xD847-lounge-replay_get_access_url` **完全同构**（同为单 NUL 串、同槽预算 257、同容量 `0x101`），仅 opcode / 去向槽不同（`vt[0x4EC]` vs `vt[0x4E4]`）。
- 关联：`SC-0xD847`（replay）、`SC-0xDB2C`（bbs）两条「取 URL」命令互为同族对照。

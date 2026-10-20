# 未决问题 / 记录 —— SC-0xDE24-battle-proto_version_check_r

- 本批（批次-14）定稿：与 auth/lounge 两条同 opcode 命令**字段结构完全相同**，仅协议类与去向槽不同（battle `vt[0x6C]`）。
- 关联：`SC-0xDE24-auth-...`、`SC-0xDE24-lounge-...`；battle 分发器块尾紧接着 `0xDCF2`（roomlobby_pilot_msdeck）——见块尾 `cmp eax,0DE24h; jz`@`B2CFCC`。

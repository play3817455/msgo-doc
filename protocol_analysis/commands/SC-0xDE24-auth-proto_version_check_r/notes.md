# 未决问题 / 记录 —— SC-0xDE24-auth-proto_version_check_r

- 本批（批次-14）定稿：★**auth 协议类**的守卫 = `sub_B02C90`（≠ battle `sub_B05DA0`、≠ lounge `sub_B41120`）；**无收尾函数**，闭合点在「读取后的成功分支」`B048A7`。
- ★**同一 opcode `0xDE24` 在三个协议类下各有一条命令**（auth/battle/lounge），字段结构完全相同（version/crc/gentime 三 u32）、仅去向槽不同（auth `vt[0x68]`、battle `vt[0x6C]`、lounge `vt[0x68]`）⇒ **文件夹名必须带协议类短名**（SOP §2 命名规范）。
- 关联：`SC-0xDE24-battle-proto_version_check_r`、`SC-0xDE24-lounge-proto_version_check_r`；`C→S` 侧 `CS-0x34A9`（send_proto_version_check）。

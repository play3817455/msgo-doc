# 分析笔记 —— CS-0x002A-chat_dcteam_up

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自 trace 日志串 `msg=\"`（@`0xB8D8C9` 附近）。
- 容量 `0xBA`=186 ≥ 2 + (181+1) = 184 ✓。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onChatDcteamUp`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- 处置：**无同 opcode 的 `_r`** ⇒ 解码 + 留证、**零回包**、不落库。
- ★裁决：**不广播** —— 受众名册未取证："dcteam = 杯赛队伍（`game.pilot.cupteam_id`）"
  只有命名学依据，`db_design/schema/homing/objects/cupteam.json` 的 `reads` 里
  **没有**任何 `chat_*`，本条与 `SC-0x93AC` 的 `db_effects` 都是 `[]`；
  投错名册比不投更糟（见 docs/01 §㊺①）。发送点在 `sub_472AC0` 聊天频道选择子
  `this+148 == 19` 那一支（与 `sub_43F7F0(...)&&(*(BYTE*)(dword_11E3EA8+454900)&2)`
  不成立时同频道改走的 `sub_B011B0` 相对）。
- 验收：`internal/lounge/misc_test.go` 的 `TestMiscSilentHandlersSendNothing`
  （好包帧数 **0**）、`TestMiscHandlersTolerateBadBody`（串槽无 NUL ⇒ 零帧不崩）。
- 配对：下行同族是 `SC-0x93AC-lounge-chat_dcteam_down`（**不是**同 opcode 的 `_r`）。
- 留账：**受众绑定证据** —— 补它要客户端聊天频道枚举/标签串，或 `db_design` 某列 DDL
  注释点名 `chat_dcteam`；拿到后即可「取 `msg` ⇒ 广播 `SC-0x93AC`」
  （`store.CupteamPilots` 已能把 `cupteam_id` 翻成名册）。

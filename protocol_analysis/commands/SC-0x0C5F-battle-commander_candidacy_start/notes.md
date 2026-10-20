# 未决问题 —— SC-0x0C5F-battle-commander_candidacy_start

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `vt[0x29C]` 的业务定名 | 未知（槽号 `0x29C` 已确证，跨命令未交叉到同槽） | 未交叉 UI 侧实现 | 2026-09-20 |
| Q2 | `remain_sec` 的计时基准（开局票倒计时 / 候选阶段倒计时） | 推测为「指挥官候选阶段剩余秒数」（由命令名 `commander_candidacy_start` + 日志串推得） | 未找到 UI 侧读数点 | 2026-09-20 |
| Q3 | `0xE12A commander_candidacy_end` 是否带对称字段 | 未知（该条仍 DRAFT） | 未分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 同族：`../SC-0xE12A-battle-commander_candidacy_end/`（`0xE12A`，本次未分析）、`../CS-0x6C48-battle-commander_candidacy_inbattle/`（`0x6C48`，本机容量 `0x2`）。
- 本命令**无严格配对请求**：`commander_candidacy_start` 是服务端主动开票通知（客户端侧无 `send_commander_candidacy_start`）。
- 容量口径例证：本命令 `容量 == 线长`（全定长、无数组、无串），与 `_meta\长期记忆.md` §3「容量 = Σ各字段缓冲 claim」一致。

## 取证来源

- 全部汇编证据取自 IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，块 `0xB0E708..0xB0E879`（批次-4 落盘 `_b4_dump.txt`），无需要走 `unpacked\shell` dump 的情形。

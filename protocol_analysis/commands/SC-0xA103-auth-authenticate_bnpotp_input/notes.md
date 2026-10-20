# 未决问题 —— SC-0xA103-authenticate_bnpotp_input

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `[esi+398h]` 是什么对象 | 仅用于日志上下文，**不是线字段**；具体类型未确证 | 未追该成员的全部用途 | 2026-09-20 |
| Q2 | `[esi+8]` 是什么 | 打印在 `" (id:"` 后，像连接/会话 id；**不是线字段** | 未追取值来源 | 2026-09-20 |
| Q3 | 配对请求 `send_authenticate_bnpotp_input_r`（`0xB05190`）的 opcode | `?` | 需在该命令文档中确证后回填 | 2026-09-20 |
| Q4 | `sub_B02C90(4)` 的语义 | 推测为「case 级开关/阈值」（与日志级别或协议版本相关） | 未读该函数 | 2026-09-20 |
| Q5 | 本命令与 `0x60E0 authenticate_you9otp_input`、`0x8F36 authenticate_you9channeling_r` 的先后顺序 | 同族，均为 0 负载通知 | 未做时序分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 请求侧：`_proto_auth_client::send_authenticate_bnpotp_input_r` @ `0xB05190`。
- 同族（同为认证流程、0 负载）：`0x60E0 authenticate_you9otp_input`、
  `0x8F36 authenticate_you9channeling_r`、`0xA5DA authenticate_r`、`0xDE24 proto_version_check_r`。

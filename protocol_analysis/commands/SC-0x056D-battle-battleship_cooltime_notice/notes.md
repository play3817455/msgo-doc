# 未决问题 —— SC-0x056D-battle-battleship_cooltime_notice

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `remain_msec` 是绝对剩余毫秒还是「到期时刻」 | 按字段名 `remain_msec=` 判断为剩余毫秒 | 块内无换算/比较指令；未追 `vt[0x310]` 实现 | 2026-09-20 |
| Q2 | `vt[0x310]` 去向（战舰 UI 冷却条？实体状态） | 未知 | 虚表实现未追 | 2026-09-20 |
| Q3 | 与 `SC-0x5B98 battleship_limittime_notice` 的语义分工 | 本命令 = 冷却提示，`limittime` = 时限提示，二者不同 | 两条命令的消费去向都未追到底 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 同族（战舰）：`CS-0xBA58 battleship_ride`、`SC-0xE014 battleship_ride_r`、`SC-0x5B98 battleship_limittime_notice`、`CS-0xF4B9 battleship_get_down`、`SC-0x1EC7 battleship_get_down_r`、`CS-0x271F battleship_crash_impact`。
- 本命令**无同名发送侧请求**（INDEX 中无 `send_battleship_cooltime_notice`）⇒ 服务端主动推送（notice 语义），G7 以同族链接替代。

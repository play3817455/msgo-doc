# 未决问题 —— SC-0x0587-lounge-pilot_dailyrecord_notice

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `is_open_info` 的取值域（是否仅 0/1，或含「开放等级」） | 名为 `is_open` 倾向布尔，但**未确证** | 块内无比较/分支依赖该值；打印器 `sub_B0C1F0` 口径未读到（本批未展开该函数体） | 2026-09-20 |
| Q2 | `vt[0x160]` 去向（战绩 UI 开关？红点？） | 未知 | 虚表实现未追 | 2026-09-20 |
| Q3 | 与 `SC-0x81F1 pilot_dailyrecord_get_r` 的字段关系 | 「notice」是推送，「get_r」是查询应答，字段集合很可能不同 | 未逐字段比对（跨命令，本批未做） | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 同族（每日战绩）：`CS-0xB184 pilot_dailyrecord_get`、`SC-0x81F1 pilot_dailyrecord_get_r`、`CS-0x2EE8 pilot_dailyrecord_collect_complete`、`SC-0xDFC2 pilot_dailyrecord_collect_complete_r`。
- 本命令**无同名发送侧请求**（INDEX 中无 `send_pilot_dailyrecord_notice`）⇒ 服务端主动通知，G7 以同族链接替代。

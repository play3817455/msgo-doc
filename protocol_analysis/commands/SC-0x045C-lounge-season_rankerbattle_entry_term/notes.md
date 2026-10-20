# 未决问题 —— SC-0x045C-lounge-season_rankerbattle_entry_term

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `term_sec` 是「绝对 Unix 时刻」还是「剩余秒数」 | 字面为「期限秒」，两者都可能 | 客户端只把它 push 给 `vt[0x5A4]`，块内无比较/换算指令；`vt[0x5A4]` 的实现不在本 case 块内（未追） | 2026-09-20 |
| Q2 | `vt[0x5A4]` 的实现去向（写哪个 UI/对象） | 未知 | 静态未追虚表实现；非本命令专属，属跨命令共性待办 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 同族（赛季排位战）：`SC-0xD286 season_rankerbattle_entry_info`、`SC-0x63D3 season_rankerbattle_config_update`、`SC-0xD18B season_rankerbattle_state_update`、`SC-0x9F9B season_rankerbattle_get_entitled_pilot_list_r`、`SC-0xA148 season_rankerbattle_replay_info`、`SC-0xEC71 season_rankerbattle_set_event_flag`。
- 本命令**无同名发送侧请求**（INDEX 中无 `send_season_rankerbattle_entry_term`）⇒ G7 以同族链接替代。

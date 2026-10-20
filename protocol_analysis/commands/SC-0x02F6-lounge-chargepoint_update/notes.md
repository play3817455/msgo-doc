# 未决问题 —— SC-0x02F6-lounge-chargepoint_update

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `chargepoint` 的单位（1 点 = ? 日元/1 元） | `?` | 客户端不做换算；需数据表/UI 脚本交叉 | 2026-09-20 |
| Q2 | `vt[0xF8]` 的具体实现 | 未定（lounge proto 对象虚表项） | 需定位 proto 对象构造/vtable | 2026-09-20 |
| Q3 | 是否存在配对 C→S 请求 | 无同名 `send_chargepoint_update`（视为服务端通知/余额同步） | — | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| 2026-09-20 | 机器草案：`f_0`(u32) 含义 `?` | 块内日志串 `chargepoint=`（`0xB5320A`） | 字段名 `chargepoint`，去向 `vt[0xF8]`（`0xB53263`），状态 DRAFT→DONE |

## 与其他命令的关联

- 同族（充值点）：`chargepoint_get`（C→S `0xAAE5`）、`chargepoint_price_list_get`(`0x7CCB`/`0x9397`)、`chargepoint_charge_url_get`(`0xFFC6`)/`chargepoint_charge_url_get_r`(`0x4DA5`)。
- 结构同型（单 u32 应答）：`dailycup_exit_r`(`0x02C0`)，但去向 vtable 项不同（`0xF8` vs `0x568`）。

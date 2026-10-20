# 未决问题 —— SC-0x00F0-msma_weapon_buildup_reset_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `vt[0x2D8]` 的具体实现 | 未定（lounge proto 对象虚表项） | 需先定位 proto 对象构造/vtable；不影响线格式结论 | 2026-09-20 |
| Q2 | `result` 的取值枚举 | `?` | 无枚举表/字符串表交叉源 | 2026-09-20 |
| Q3 | `item_id` 的取值范围（物品表主键？） | 推测为物品表 ID | 未追到查表调用点 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| 2026-09-20 | 机器草案：3 个字段（u32/u64/u32）含义 `?` | 块内日志串 `result=` / `uniqid_ms=` / `item_id=`（`0xB51BBB` / `0xB51BE9` / `0xB51C0E`） | 字段名确定，去向 `vt[0x2D8]`（`0xB51C79`），状态 DRAFT→DONE |

## 与其他命令的关联

- 发出侧配对：`../CS-0x8DEB-lounge-msma_weapon_buildup_reset/`（`_proto_lounge_client::send_msma_weapon_buildup_reset` @ `0xB976A0`，声明容量 `0xE`）。
- 同族（武器强化族）：`msma_weapon_buildup_r`(`0x0876`)、`msma_weapon_buildup_extra_cnt_update_r`(`0x5B3F`)、`msma_weapon_buildup_complete_r`(`0xDE68`)、`msma_weapon_buildup_estimate_r`(`0x9932`)。
- 同族（机体领取族）：`msma_trialms_back_r`(`0x00C7`)。

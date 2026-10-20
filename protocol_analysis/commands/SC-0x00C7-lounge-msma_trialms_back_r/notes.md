# 未决问题 —— SC-0x00C7-msma_trialms_back_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `vt[0x328]` 的具体实现 | 未定（lounge proto 对象虚表项，`esi`=proto 对象） | 需先定位 proto 对象构造/vtable；不影响线格式结论 | 2026-09-20 |
| Q2 | `result` 的取值枚举 | `?` | 未找到枚举表/字符串表交叉源；线类型与位置已确证 | 2026-09-20 |
| Q3 | `uniqid_ms` 与 `msma` 表主键的对应关系 | 推测为机体唯一 ID（由 `uniqid_ms=` 串判定） | 未追到落库/查表调用点 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| 2026-09-20 | 机器草案：`f_0`(u32) / `f_2`(u64) 含义 `?` | 块内日志串 `result=` / `uniqid_ms=`（`0xB51DF5` / `0xB51E1A`） | 字段名 `result` / `uniqid_ms`，去向 `vt[0x328]`（`0xB51E7E`），状态 DRAFT→DONE |

## 与其他命令的关联

- 发出侧配对：`../CS-0x0C2A-lounge-msma_trialms_back/`（`_proto_lounge_client::send_msma_trialms_back` @ `0xB99C20`，声明容量 `0xA`）。
- 同族（lounge 机体类应答）：`msma_weapon_buildup_reset_r`(`0x00F0`)、`msma_init_get_r_begin`(`0x2ACF`)。

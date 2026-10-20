# 未决问题 —— SC-0x20F5-entity_msma_fix

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | 6 个字段（5×u16 + 1×u8）各自的**含义** | 全部 `?` | 需追 `vt[0x68]` 的实现（`[edi] + 0x68`，`edi` = proto 对象）；该方法才是语义落点 | 2026-09-20 |
| Q2 | `vt[0x68]` 是哪个函数 | 未定（虚表项，需在运行时或由构造处确定） | 静态需先定位 proto 对象的构造/vtable | 2026-09-20 |
| Q3 | `sub_B05DA0(0x5E)` 的语义 | 推测为「case 级开关/阈值」（与 battle 其他 case 同款，如 `0xB31273 push 4Fh; call sub_B05DA0`） | 未读该函数 | 2026-09-20 |
| Q4 | 与发出侧 `0x20F5`（`send_entity_msma_fix` @`0xB0C910`）的字段对应关系 | 双向同号，字段应能互相解释 | 需先完成发出侧字段分析 | 2026-09-20 |
| Q5 | 为什么走 default 分支而不是 switch case | 推测为「该 opcode 由另一套（非 `_client` 命名空间）协议对象处理」，故不登记进 `_client` 的 switch | 未查 `_proto_battle` 与 `_proto_battle_client` 的注册关系 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| 2026-09-20 | （无） | — | 初版：opcode `0x20F5`、总长 13 字节、负载 5×u16+u8、长度闭合在 `0xB0C37C` |

## 与其他命令的关联

- 发出侧配对：`../CS-0x20F5-battle-entity_msma_fix/`（`_proto_battle::send_entity_msma_fix` @ `0xB0C910`，opcode 同为 `0x20F5`）。
- 同族命名：`recv_entity_msma_dead`（`0x918E` 之外的 battle 实体类命令，见 INDEX）。
- 分发路径同类（不经 switch 的 recv）：本目录当前仅此 1 条。

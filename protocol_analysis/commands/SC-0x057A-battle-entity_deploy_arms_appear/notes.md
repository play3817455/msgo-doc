# 未决问题 —— SC-0x057A-battle-entity_deploy_arms_appear

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `team` / `troops` / `type` / `is_gmk` / `is_using_ss` / `hp_percent` / `hp_percent_shield` / `equip_index` 的**符号性** | 线宽 1 字节确证；符号性记 `?` —— 读取器是**无扩展字节拷贝**（`0xB07ED3 mov dl,[eax]`），打印器却用 `movsx` 按有符号打印（`0xB0B4C5` 等），仅 `water_index`/`layer_index` 用 `movzx` | 客户端在块内只打印 + 交给 `vt[0x158]`，无符号敏感运算 ⇒ 静态不可判 | 2026-09-20 |
| Q2 | `state_bit` / `special_bits` / `special_bits2` 的位定义 | 未知（三者分别以十六进制打印：`sub_B032A0` / `sub_ADC810` / `sub_B03420`） | 块内无 `bt/bts` 序列；位定义表未找到 | 2026-09-20 |
| Q3 | `vt[0x158]` 去向（生成实体？喂 UI？） | 未知 | 虚表实现未追 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| 2026-09-20 | 机器草案（`draft-wire.md`）：「未提取到字段」，字段总长「含变长/数组无法求和」，自校验 N/A | 人工续扫：`0xB0D8ED` 的 `sub_B06020` 只是缓冲预留（claim 96B），真正的读取是 `0xB0D8FC` 的复合读取器 `sub_B07EC0` | 单一复合结构体 `appear_info`，**线长 86B（定长）**；容量 96 = 结构体 claim ≠ 线长 |
| 2026-09-20 | 本批中途版本：结构体 **80B**（`snapshot` 37B，`buildup_eff_range`/`special_bits2`「不在线上」） | **函数边界复核**（`ida_funcs.get_func`）：`sub_B07EC0` 实为 `0xB07EC0..0xB0801B`、`sub_B075A0` 实为 `0xB075A0..0xB07757`；两者在**失败分支 `retn` 之后还有「成功路径尾读」**：`0xB0800B`（`add edi,5Ch` + `sub_B02DD0` = `buildup_eff_range` u32）与 `0xB07747`（`add edi,28h` + `sub_B02DF0` = `special_bits2` u16） | 结构体 **86B**（`snapshot` **39B**）；两者**都在线上** |

## 与其他命令的关联

- 相关发送侧：`CS-0x07C9-battle-entity_deploy_arms_attach`（部署挂载，容量 `0x16`）。
- 同族部署：`SC-0x6D20 battle-weapon_fire__deploy_arms_r`。
- 结构体复用：`snapshot` 子结构的成员集合（`pos_*`/`target_*`/`score*`/`hp_percent`/`lockon_ent_id` …）与战斗实体状态类命令高度重合，后续如遇同名成员可直接比对（注意各命令的**线长各自独立**，不得互推）。
- 方法论沉淀（已写入 `_meta/长期记忆.md`）：
  1. **容量 = 结构体 claim ≠ 线长**（本命令 96 vs 86）；
  2. **「成功路径尾读」坑**：复合读取器（及本目录的多个 `sub_Bxxxx` 读取器）在**失败出口 `retn` 之后**往往还有「成功分支」，其中可能仍含读取 ⇒ **必须用 `ida_funcs.get_func()` 取函数真实边界后整函数扫描**，不可见 `retn` 即停（`0x063E` 的 `pilot_detail` 因此从 64B 修正为 51672B）。

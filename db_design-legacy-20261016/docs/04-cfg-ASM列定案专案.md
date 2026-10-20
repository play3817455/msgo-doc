# 配置表 ASM 列定案专案

## 目标

通过 IDA 反编译各表 **逐列读取函数**（`sub_*`），为 79 张 cfg 表全部字段给出：

1. **订案名** `name`（snake_case，DB 物理列名）
2. **语义** `meaning` + **类型** `type`
3. **ASM 证据** `asm_reader` / `asm_va` / `memory_offset`
4. **状态** `confirmed` | `partial` | `pending` | `gap`

## 工作流

```
datatables/01-列注释/*.md     # 已有列位+类型证据
        ↓
extract_cfg_readers.py        # 提取 reader_func → _asm_manifest.json
        ↓
IDA decompile(sub_*)          # 子 agent 分批验证
        ↓
schema/cfg/tables/*.json      # 写回订案（status=confirmed 时 db_column=name）
        ↓
merge_cfg_asm.py              # 汇总 + 导出 cfg_schema.json
        ↓
cfgload                       # 建表用订案列名
build_site.py                 # 刷新 site/cfg/
```

## 订名规则

- 主键：`{entity}_id`（如 `item_id`, `weapon_group_id`）
- 枚举：语义名（`item_type`, `equip_slot_type`）
- 字符串：`name`, `description`
- 布尔：`enabled`, `is_*`
- 未证实但已知类型：`unknown_u32_N` / `flag_bool_N`（**禁止** `colN` / `pending_*` 进 DB）
- `gap`：CSV 有列位但 reader 未读 → `reserved_u32_N`（不写入 DB，cfgload 跳过）

## 分批（子 agent）

| 批 | 组 | 表数 |
|----|-----|------|
| 1 | 机体 B | 13 |
| 2 | 武器+物品 C+D | 15 |
| 3 | 成长+开发 E+F | 19 |
| 4 | 任务+杂项 G-K | 32 |

## IDA 证据标准

- ★ **confirmed**：decompile 中明确 `sub_BBB370(ctx, N)` / 字符串列 / 枚举转换函数 + 可选 xref 消费
- ○ **partial**：类型+列位确证，语义来自枚举字面量或文档推断
- △ **pending**：仅知 u32 占位
- **gap**：reader 未读该 CSV 列

## 进度（2026-09-21）

- **79/79** 表 `asm_status=complete`，**0 pending** 列
- 完成判定：每 CSV 列均已 ASM 审查（confirmed / partial / gap）
- 检查：`python db_design/tools/asm_cfg_loop_status.py`
- DB 重载订案列名：`go run ./tools/cfgload -drop -schema-dir ../db_design/schema/cfg/tables`
- 后续可选：将 `partial`/`unknown_*` 通过 xref 升级为 `confirmed`

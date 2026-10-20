# 未决问题 / 记录 —— SC-0xDDE9-battle-module_toggle_level

- 本批（批次-14）定稿：容量 10 精确吻合；3 个日志名与 3 个字段一一对位。
- 同一「module_toggle_*」族的另两条：`SC-0xD8B9`（`_time`：ent_id/msec/rate）、`SC-0xE2DE`（`_point`），字段结构各不相同，**不得互相套用**（SOP §6.2 高发错误 1）。
- 关联：与 `0x645D`（module_val_update）同族模块状态命令。

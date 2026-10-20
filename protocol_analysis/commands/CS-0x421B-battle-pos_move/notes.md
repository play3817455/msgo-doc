# 分析笔记 —— CS-0x421B-battle-pos_move

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0xAA`；分配器指纹 @ `0xB3521F`。
- 去向槽：`vt[0x58]`（发送）@ `0xB35926`。
- ★ 含变长段：`hack_check_count`(u32，上限 1) + `hack_check[]`（元素线长 **79**、槽步进 **0x58=88**）。
- 该块帧基址用 `ebp`（非 `esp`），参数写作 `[ebp+arg_N]`。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

2026-10-11 v15 configured ida-pro-mcp补证：4D4270在4D42F1..4350通过控制器vt+716取得当前访问目标；普通SelfTargetView D72564该槽是4E5C90→442910(manager+176)。目标mask8必须为0且478C80(CHARA_PARAM+412!=0)才把actor+4写access_ent_id1来源var240；控制器spbits无0x800000时再次清0。4D1B00设置此bit的已证实来源为vt+728→4E23F0(manager+676mask8)或vt+736→4D12D0(controller+4484非空)。因此access1可表达交互意图，不是未知纯保留槽，也不是搬运成功/所属身份。access2来自vt+744→4D12E0(controller+4488句柄非空)时该句柄actor+4，具体关系类别未定。证据serverv/docs/data/ida-v15-pos-move-access-intent-20261011.json；未以字段名推定所有F键/拾取成功。

- `hack_check[]` 元素内部成员未逐一命名（按 `sub_B065D0` 写线序记录 79B）。

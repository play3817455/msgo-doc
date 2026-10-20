# 分析笔记 —— CS-0x050A-ranking_clan_get

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- `sub_B42060` 逐字节核对：写 5 个 u16（线长 10）—— 4 次内联 `mov si,[ecx+k]; mov [edx],si`
  （`k = 0/2/4/6`）+ 末槽 `add ecx,8; call sub_B02DA0`（u16），游标每槽 +2，累计 +10 ✓。
- 字段名取自 trace 日志串 `order=` / `clan_kind=`（@`0xBA3B5A` 起）。
- 容量 `0x12`=18 ≥ 线长 13（2+10+1）✓。

## 与其他命令的关联

- （无同 opcode 反向命令）
- 上行族共享同一 `order` 写入器：`CS-0x3FAF`（@`0xBA38AB`）、`CS-0x8BDF`（@`0xBA77FB`）。

## 复合体判定（2026-09-26 闭合，原「未决 / 存疑」）

- 原存疑：`order` 为 `sub_B42060` 写出的 10 字节（5×u16），"5 个槽语义未定名（记 `?`）"。
- 取证：本命令 @ `0xBA3ABB` 的 `call sub_B42060` 与 `CS-0x3FAF` @ `0xBA38AB`、
  `CS-0x8BDF` @ `0xBA77FB` 调的是**同一个函数**，摊平同一个入参（arg_0，指向 5×u16 的扁平原值）
  ⇒ 这 10B 逐字段同序，就是复合体 `order`。`db_design/schema/composites/order.json` 已有五处
  成员级取证（读者 `sub_B46420` @ `0xB46438`/`0xB4644D`/`0xB46461`/`0xB46475`/`0xB4647D`，
  `asm_verified: true`，线长 = claim = 10）⇒ 不再是"无名位置形"。
- 动作：`fields.csv` 第 2 行线类型 `array<u16,5>` → `struct`（与 `CS-0x3FAF` 同写法）、
  取值列写「见 §3 结构体」，README §3/§4.2/§4.3 同步；本命令登记进 `composites/order.json` 的
  `evidence.commands`（第 7 条线体证据、第 3 条上行线体；`protocol_paths` 只留给有**成员级**
  `wire_sources` 的那两条，本条没有，故不加）；`_legacy_tables/tbl_order.json` 是冻结的旧库证据，不动。
- 收尾：codecgen 生成码由 `[]uint16` 变 `model.Order`（服务端不再按位置摊平），
  `onRankingClanGet` / `onRankingClanGetPage` 直接用 `req.Order`（`internal/lounge/ranking_clan.go`），
  测试侧的喂参同步改。

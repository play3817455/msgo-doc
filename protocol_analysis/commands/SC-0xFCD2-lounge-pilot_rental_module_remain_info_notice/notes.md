# 分析笔记 —— SC-0xFCD2-pilot_rental_module_remain_info_notice

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `hav_rental_modules={` / `empty_rental_modules={`（@`0xB883A7`/`0xB8840B`）。
- ★ 容量校验：`0x600`=1536 = 128×8 + 128×4 ✓（两个数组**均无线上 count**，上限为字面量 128）。
- ★ 「整块定长数组」形态：`sub_B412A0` 用 `mov edx,[ecx]; add edx,400h; mov [ecx],edx` 推进游标，**不形如 `add <mem>,IMM`** ⇒ 机械抽取器会算 0，须人工识别（同族：`sub_B41AA0` 推进 0x1000、`sub_B41280` 推进 0x80、`sub_B41760` 推进 0x12C、`sub_B06140` 推进 0x70）。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

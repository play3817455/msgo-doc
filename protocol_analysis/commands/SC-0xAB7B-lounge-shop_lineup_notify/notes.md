# 未决问题 / 记录 —— SC-0xAB7B-lounge-shop_lineup_notify

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `id_type` 的打印器为 `sub_B4E110`（`log1` + `fmt_u`），逐项以十六进制输出 ⇒ 类型为字节序枚举，非压缩位。
- `item_list` 元素内部成员未逐一命名（记为 `array<struct,24>`，槽步进来自 `sub_B416C0`、线长 23 来自 `sub_B458A0` 整函数展开）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。

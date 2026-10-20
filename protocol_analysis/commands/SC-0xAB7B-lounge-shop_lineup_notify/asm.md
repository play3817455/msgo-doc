# 汇编证据 —— SC-0xAB7B-lounge-shop_lineup_notify

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x30DC` @ `B71905`）

```asm
; VA: B71905（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x30DC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— id_type_num：偏移 0，长度 4，线类型 u32（id_type 条目数（上限 500））
;   B71938|B71964
; 字段 2 —— id_type：偏移 4，长度 n₁，线类型 array<u8,500>（商店阵容类型列表（日志串 `id_type={...}` 逐项十六进制打印））
;   B71976|B7198D
; 字段 3 —— item_num：偏移 var，长度 4，线类型 u32（item_list 条目数（上限 500））
;   B719BC|B719E8
; 字段 4 —— item_list：偏移 var，长度 23·n₂，线类型 array<struct,24>（商店商品列表（元素线长 23 / 槽步进 24））
;   B719FA|B71A1A|B71A26
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B71A48
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x17A）报错
```

## E4 去向（用途锚点）

```asm
; VA: B71C15 —— `vt[0x3B0]`（4 实参）
```

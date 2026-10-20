# 汇编证据 —— SC-0x7300-lounge-clan_rokaku_use_point_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x15` @ `0xb66761`）

```asm
; VA: 0xb66761（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb66761  push    0x15          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb6679c
; 字段 2 —— tree_id：偏移 4，长度 4，线类型 u32；读取点 VA 0xb667dc
; 字段 3 —— node_no：偏移 8，长度 4，线类型 u32；读取点 VA 0xb66800
; 字段 4 —— idx_no：偏移 12，长度 4，线类型 u32；读取点 VA 0xb66824
; 字段 5 —— point_use：偏移 16，长度 4，线类型 u32；读取点 VA 0xb6684c
; 字段 6 —— is_supply：偏移 20，长度 1，线类型 u8；读取点 VA 0xb66874
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb66888
0xb66888  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb66a71（6 实参）
;       `vt[0x490]`
```

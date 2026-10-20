# 汇编证据 —— SC-0x73AA-lounge-msma_equip_shield_change_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xb66abd`）

```asm
; VA: 0xb66abd（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb66abd  push    0x10          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb66af8
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64；读取点 VA 0xb66b38
; 字段 3 —— item_id：偏移 12，长度 4，线类型 u32；读取点 VA 0xb66b5c
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb66b6c
0xb66b6c  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb66cc9（4 实参）
;       `vt[0x25C]`
```

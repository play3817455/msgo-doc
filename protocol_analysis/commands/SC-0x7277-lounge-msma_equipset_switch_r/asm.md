# 汇编证据 —— SC-0x7277-lounge-msma_equipset_switch_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `0xb66269`）

```asm
; VA: 0xb66269（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb66269  push    0x12          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb662a4
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64；读取点 VA 0xb662e4
; 字段 3 —— slot：偏移 12，长度 2，线类型 u16；读取点 VA 0xb66324
; 字段 4 —— cost：偏移 14，长度 4，线类型 u32；读取点 VA 0xb66348
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb66358
0xb66358  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb664e4（5 实参）
;       `vt[0x310]`
```

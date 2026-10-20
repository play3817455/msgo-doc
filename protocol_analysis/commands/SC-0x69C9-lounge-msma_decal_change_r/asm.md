# 汇编证据 —— SC-0x69C9-lounge-msma_decal_change_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `0xb64fd0`）

```asm
; VA: 0xb64fd0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb64fd0  push    0x18          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb6500b
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64；读取点 VA 0xb6504b
; 字段 3 —— decal：偏移 12，长度 4，线类型 u32；读取点 VA 0xb6506f
; 字段 4 —— uniqid_decal：偏移 20，长度 8，线类型 u64；读取点 VA 0xb65093
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb650bb
0xb650bb  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb6524f（6 实参）
;       `vt[0x288]`
```

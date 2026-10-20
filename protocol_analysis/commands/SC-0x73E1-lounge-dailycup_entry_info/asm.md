# 汇编证据 —— SC-0x73E1-lounge-dailycup_entry_info

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xb66ee8`）

```asm
; VA: 0xb66ee8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb66ee8  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— rescode：偏移 0，长度 4，线类型 u32；读取点 VA 0xb66f23
; 字段 2 —— bracket_idx：偏移 4，长度 4，线类型 u32；读取点 VA 0xb66f63
; 字段 3 —— team_id：偏移 8，长度 4，线类型 u32；读取点 VA 0xb66f87
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb66f97
0xb66f97  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb670ec（3 实参）
;       `vt[0x560]`
```

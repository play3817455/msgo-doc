# 汇编证据 —— SC-0x6D8F-battle-commander_support_debug_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `0xb1dbee`）

```asm
; VA: 0xb1dbee（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1dbee  push    0xB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1dc27
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8；读取点 VA 0xb1dc67
; 字段 3 —— support_type：偏移 2，长度 4，线类型 u32；读取点 VA 0xb1dc8b
; 字段 4 —— ent_id：偏移 6，长度 2，线类型 u16；读取点 VA 0xb1dcaf
; 字段 5 —— spt_ms_index：偏移 8，长度 2，线类型 u16；读取点 VA 0xb1dcd7
; 字段 6 —— spt_spot_index：偏移 10，长度 1，线类型 u8；读取点 VA 0xb1dcff
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1dd0f
0xb1dd0f  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1df02（6 实参）
;       `vt[0x2C4]`
```

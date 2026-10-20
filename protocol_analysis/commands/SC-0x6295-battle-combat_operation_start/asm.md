# 汇编证据 —— SC-0x6295-battle-combat_operation_start

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `0xb1be0a`）

```asm
; VA: 0xb1be0a（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1be0a  push    0x18          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1be43
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8；读取点 VA 0xb1be83
; 字段 3 —— support_type：偏移 2，长度 4，线类型 u32；读取点 VA 0xb1bea7
; 字段 4 —— remain_msec：偏移 6，长度 4，线类型 u32；读取点 VA 0xb1becb
; 字段 5 —— target_x：偏移 10，长度 2，线类型 u16；读取点 VA 0xb1bef3
; 字段 6 —— target_y：偏移 12，长度 2，线类型 u16；读取点 VA 0xb1bf1b
; 字段 7 —— target_z：偏移 14，长度 2，线类型 u16；读取点 VA 0xb1bf43
; 字段 8 —— use_worldid：偏移 16，长度 4，线类型 u32；读取点 VA 0xb1bf6b
; 字段 9 —— use_pilotid：偏移 20，长度 4，线类型 u32；读取点 VA 0xb1bf93
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1bfa3
0xb1bfa3  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1c22a（7 实参）
;       `vt[0x2EC]`
```

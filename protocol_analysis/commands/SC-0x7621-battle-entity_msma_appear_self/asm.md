# 汇编证据 —— SC-0x7621-battle-entity_msma_appear_self

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x154` @ `0xb2004b`）

```asm
; VA: 0xb2004b（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb2004b  push    0x154          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb20089
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8；读取点 VA 0xb200c6
; 字段 3 —— ms：偏移 2，长度 244，线类型 struct<ms>；读取点 VA 0xb200ea
; 字段 4 —— snapshot：偏移 246，长度 39，线类型 struct<snapshot>；读取点 VA 0xb2010e
; 字段 5 —— funnelss：偏移 285，长度 10，线类型 struct<funnelss>；读取点 VA 0xb20136
; 字段 6 —— hp_now：偏移 295，长度 4，线类型 u32；读取点 VA 0xb2015e
; 字段 7 —— hp_max：偏移 299，长度 4，线类型 u32；读取点 VA 0xb20186
; 字段 8 —— shield_hp_now：偏移 303，长度 4，线类型 u32；读取点 VA 0xb201ae
; 字段 9 —— shield_hp_max：偏移 307，长度 4，线类型 u32；读取点 VA 0xb201d6
; 字段 10 —— weapon_state_bits：偏移 311，长度 2，线类型 u16；读取点 VA 0xb201fe
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb20212
0xb20212  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb204b6（10 实参）
;       `vt[0x150]`
```

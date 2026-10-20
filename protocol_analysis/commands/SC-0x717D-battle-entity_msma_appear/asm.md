# 汇编证据 —— SC-0x717D-battle-entity_msma_appear

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x156` @ `0xb1eaee`）

```asm
; VA: 0xb1eaee（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1eaee  push    0x156          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1eb2c（B06230）
; 字段 2 —— troops：偏移 1，长度 4，线类型 u32；读取点 VA 0xb1eb69（B02DD0）
; 字段 3 —— world_id：偏移 5，长度 4，线类型 u32；读取点 VA 0xb1eb8d（B02DD0）
; 字段 4 —— pilot_id：偏移 9，长度 4，线类型 u32；读取点 VA 0xb1ebb1（B02DD0）
; 字段 5 —— ms：偏移 13，长度 244，线类型 struct<ms>；读取点 VA 0xb1ebd9
; 字段 6 —— snapshot：偏移 257，长度 39，线类型 struct<snapshot>；读取点 VA 0xb1ec01
; 字段 7 —— funnelss：偏移 296，长度 10，线类型 struct<funnelss>；读取点 VA 0xb1ec29
; 字段 8 —— unattended_state_bit：偏移 306，长度 2，线类型 u16；读取点 VA 0xb1ec51
; 字段 9 —— weapon_state_bits：偏移 308，长度 2，线类型 u16；读取点 VA 0xb1ec79
; 字段 10 —— target_icon：偏移 310，长度 1，线类型 u8；读取点 VA 0xb1eca1
; 字段 11 —— is_respawn：偏移 311，长度 1，线类型 u8；读取点 VA 0xb1ecc9
; 字段 12 —— is_using_ss：偏移 312，长度 1，线类型 u8；读取点 VA 0xb1ecf1
; 字段 13 —— stghold_number：偏移 313，长度 1，线类型 u8；读取点 VA 0xb1ed19
; 字段 14 —— xweapon_fired：偏移 314，长度 1，线类型 u8；读取点 VA 0xb1ed41
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1ed51
0xb1ed51  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1f0cf（9 实参）
;       `vt[0x154]`
```

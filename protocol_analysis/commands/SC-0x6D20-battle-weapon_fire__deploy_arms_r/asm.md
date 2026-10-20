# 汇编证据 —— SC-0x6D20-battle-weapon_fire__deploy_arms_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C` @ `0xb1d6a5`）

```asm
; VA: 0xb1d6a5（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1d6a5  push    0x1C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16；读取点 VA 0xb1d6de
; 字段 2 —— itemid：偏移 2，长度 4，线类型 u32；读取点 VA 0xb1d71e
; 字段 3 —— arms_id：偏移 6，长度 4，线类型 u32；读取点 VA 0xb1d742
; 字段 4 —— target_x：偏移 10，长度 2，线类型 u16；读取点 VA 0xb1d766
; 字段 5 —— target_y：偏移 12，长度 2，线类型 u16；读取点 VA 0xb1d78e
; 字段 6 —— target_z：偏移 14，长度 2，线类型 u16；读取点 VA 0xb1d7b6
; 字段 7 —— target_ent_id：偏移 16，长度 2，线类型 u16；读取点 VA 0xb1d7de
; 字段 8 —— state：偏移 18，长度 1，线类型 u8；读取点 VA 0xb1d806
; 字段 9 —— fx_opt：偏移 19，长度 1，线类型 u8；读取点 VA 0xb1d82e
; 字段 10 —— judge_worldid：偏移 20，长度 4，线类型 u32；读取点 VA 0xb1d856
; 字段 11 —— judge_pilotid：偏移 24，长度 4，线类型 u32；读取点 VA 0xb1d87e
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1d88e
0xb1d88e  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1db7e（11 实参）
;       `vt[0x1C0]`
```

# 汇编证据 —— SC-0x731C-battle-weapon_fire__start_homing_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xb1f107`）

```asm
; VA: 0xb1f107（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1f107  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— grenade_id：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1f142
; 字段 2 —— pos_x：偏移 4，长度 2，线类型 u16；读取点 VA 0xb1f182
; 字段 3 —— pos_y：偏移 6，长度 2，线类型 u16；读取点 VA 0xb1f1a6
; 字段 4 —— pos_z：偏移 8，长度 2，线类型 u16；读取点 VA 0xb1f1ca
; 字段 5 —— target_ent_id：偏移 10，长度 2，线类型 u16；读取点 VA 0xb1f1f2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1f206
0xb1f206  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1f3c5（5 实参）
;       `vt[0x1BC]`
```

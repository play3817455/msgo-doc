# 汇编证据 —— SC-0x759C-battle-deliver_assault_stghold_ace_status

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11` @ `0xb1fa03`）

```asm
; VA: 0xb1fa03（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1fa03  push    0x11          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1fa3e
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8；读取点 VA 0xb1fa7e
; 字段 3 —— ent_id：偏移 2，长度 2，线类型 u16；读取点 VA 0xb1faa2
; 字段 4 —— target_x：偏移 4，长度 2，线类型 u16；读取点 VA 0xb1fac6
; 字段 5 —— target_y：偏移 6，长度 2，线类型 u16；读取点 VA 0xb1faee
; 字段 6 —— target_z：偏移 8，长度 2，线类型 u16；读取点 VA 0xb1fb16
; 字段 7 —— spt_spot_index：偏移 10，长度 1，线类型 u8；读取点 VA 0xb1fb3e
; 字段 8 —— spt_spot_dir：偏移 11，长度 2，线类型 u16；读取点 VA 0xb1fb66
; 字段 9 —— remain_msec：偏移 13，长度 4，线类型 u32；读取点 VA 0xb1fb8e
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1fba2
0xb1fba2  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1fe2a（6 实参）
;       `vt[0x324]`
```

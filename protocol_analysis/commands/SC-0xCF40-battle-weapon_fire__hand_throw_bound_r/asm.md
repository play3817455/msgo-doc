# 汇编证据 —— SC-0xCF40-battle-weapon_fire__hand_throw_bound_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `B2B5AC`）

```asm
; VA: B2B5AC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x12
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— grenade_id：偏移 0，长度 4，线类型 u32（手雷 ID（日志串 `grenade_id=`））
;   0xb2b5d6|0xb2b5e5
; 字段 2 —— hit_x：偏移 4，长度 2，线类型 u16（命中点 X（日志串 `hit_x=`））
;   0xb2b616|0xb2b625
; 字段 3 —— hit_y：偏移 6，长度 2，线类型 u16（命中点 Y（日志串 `hit_y=`））
;   0xb2b63a|0xb2b649
; 字段 4 —— hit_z：偏移 8，长度 2，线类型 u16（命中点 Z（日志串 `hit_z=`））
;   0xb2b65e|0xb2b66d
; 字段 5 —— vec_x：偏移 10，长度 2，线类型 u16（投掷向量 X（日志串 `vec_x=`））
;   0xb2b686|0xb2b695
; 字段 6 —— vec_y：偏移 12，长度 2，线类型 u16（投掷向量 Y（日志串 `vec_y=`））
;   0xb2b6ae|0xb2b6bd
; 字段 7 —— vec_z：偏移 14，长度 2，线类型 u16（投掷向量 Z（日志串 `vec_z=`））
;   0xb2b6d6|0xb2b6e5
; 字段 8 —— vec_power：偏移 16，长度 2，线类型 u16（投掷力度（日志串 `vec_power=`））
;   0xb2b6fe|0xb2b70d
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2B721
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x80）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2B979 —— `vt[0x1B8]`（8 实参）
```

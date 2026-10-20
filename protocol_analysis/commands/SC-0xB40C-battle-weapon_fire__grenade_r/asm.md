# 汇编证据 —— SC-0xB40C-battle-weapon_fire__grenade_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x29` @ `B289C4`）

```asm
; VA: B289C4（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x29
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（发射者实体 ID（日志串 `ent_id=`））
;   B28A08
; 字段 2 —— itemid：偏移 2，长度 4，线类型 u32（武器/物品 ID（日志串 `itemid=`））
;   B28A4B
; 字段 3 —— grenade_id：偏移 6，长度 4，线类型 u32（弹体 ID（日志串 `grenade_id=`））
;   B28A75
; 字段 4 —— parent_id：偏移 10，长度 4，线类型 u32（父实体 ID（日志串 `parent_id=`））
;   B28A99
; 字段 5 —— launch_x：偏移 14，长度 2，线类型 u16（发射点 X（日志串 `launch_x=`））
;   B28AC1
; 字段 6 —— launch_y：偏移 16，长度 2，线类型 u16（发射点 Y（日志串 `launch_y=`））
;   B28AE9
; 字段 7 —— launch_z：偏移 18，长度 2，线类型 u16（发射点 Z（日志串 `launch_z=`））
;   B28B11
; 字段 8 —— target1_x：偏移 20，长度 2，线类型 u16（目标点 1 X（日志串 `target1_x=`））
;   B28B39
; 字段 9 —— target1_y：偏移 22，长度 2，线类型 u16（目标点 1 Y（日志串 `target1_y=`））
;   B28B61
; 字段 10 —— target1_z：偏移 24，长度 2，线类型 u16（目标点 1 Z（日志串 `target1_z=`））
;   B28B89
; 字段 11 —— target2_x：偏移 26，长度 2，线类型 u16（目标点 2 X（日志串 `target2_x=`））
;   B28BB1
; 字段 12 —— target2_y：偏移 28，长度 2，线类型 u16（目标点 2 Y（日志串 `target2_y=`））
;   B28BD9
; 字段 13 —— target2_z：偏移 30，长度 2，线类型 u16（目标点 2 Z（日志串 `target2_z=`））
;   B28C01
; 字段 14 —— target_ent_id：偏移 32，长度 2，线类型 u16（目标实体 ID（日志串 `target_ent_id=`））
;   B28C29
; 字段 15 —— msec：偏移 34，长度 2，线类型 u16（生效毫秒（日志串 `msec=`））
;   B28C51
; 字段 16 —— shot0_impact1：偏移 36，长度 1，线类型 u8（0=射击型 / 1=命中型（日志串 `shot0_impact1=`））
;   B28C79
; 字段 17 —— fx_opt：偏移 37，长度 1，线类型 u8（特效选项（日志串 `fx_opt=`））
;   B28CA1
; 字段 18 —— charge_lv：偏移 38，长度 1，线类型 u8（蓄力等级（日志串 `charge_lv=`））
;   B28CC9
; 字段 19 —— impact_wall：偏移 39，长度 1，线类型 u8（是否命中墙体（日志串 `impact_wall=`））
;   B28CF1
; 字段 20 —— action：偏移 40，长度 1，线类型 u8（动作码（日志串 `action=`））
;   B28D19
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B28D2D
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x7C）报错
```

## E4 去向（用途锚点）

```asm
; VA: B29201 —— `vt[0x1B0]`（19 实参）
```

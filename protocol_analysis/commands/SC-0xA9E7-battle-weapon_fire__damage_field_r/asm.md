# 汇编证据 —— SC-0xA9E7-battle-weapon_fire__damage_field_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x27` @ `B277BD`）

```asm
; VA: B277BD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x27
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（发射者实体 ID（日志串 `ent_id=`））
;   B27801
; 字段 2 —— itemid：偏移 2，长度 4，线类型 u32（武器/物品 ID（日志串 `itemid=`））
;   B27841
; 字段 3 —— grenade_id：偏移 6，长度 4，线类型 u32（弹体 ID（日志串 `grenade_id=`））
;   B27865
; 字段 4 —— parent_id：偏移 10，长度 4，线类型 u32（父实体 ID（日志串 `parent_id=`））
;   B27889
; 字段 5 —— launch_x：偏移 14，长度 2，线类型 u16（发射点 X（日志串 `launch_x=`））
;   B278B1
; 字段 6 —— launch_y：偏移 16，长度 2，线类型 u16（发射点 Y（日志串 `launch_y=`））
;   B278D9
; 字段 7 —— launch_z：偏移 18，长度 2，线类型 u16（发射点 Z（日志串 `launch_z=`））
;   B27901
; 字段 8 —— target1_x：偏移 20，长度 2，线类型 u16（目标点 1 X（日志串 `target1_x=`））
;   B27929
; 字段 9 —— target1_y：偏移 22，长度 2，线类型 u16（目标点 1 Y（日志串 `target1_y=`））
;   B27951
; 字段 10 —— target1_z：偏移 24，长度 2，线类型 u16（目标点 1 Z（日志串 `target1_z=`））
;   B27979
; 字段 11 —— target2_x：偏移 26，长度 2，线类型 u16（目标点 2 X（日志串 `target2_x=`））
;   B279A1
; 字段 12 —— target2_y：偏移 28，长度 2，线类型 u16（目标点 2 Y（日志串 `target2_y=`））
;   B279C9
; 字段 13 —— target2_z：偏移 30，长度 2，线类型 u16（目标点 2 Z（日志串 `target2_z=`））
;   B279F1
; 字段 14 —— target_ent_id：偏移 32，长度 2，线类型 u16（目标实体 ID（日志串 `target_ent_id=`））
;   B27A19
; 字段 15 —— msec：偏移 34，长度 2，线类型 u16（生效毫秒（日志串 `msec=`））
;   B27A41
; 字段 16 —— shot0_impact1：偏移 36，长度 1，线类型 u8（0=射击型 / 1=命中型（日志串 `shot0_impact1=`））
;   B27A69
; 字段 17 —— fx_opt：偏移 37，长度 1，线类型 u8（特效选项（日志串 `fx_opt=`））
;   B27A91
; 字段 18 —— charge_lv：偏移 38，长度 1，线类型 u8（蓄力等级（日志串 `charge_lv=`））
;   B27AB9
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B27ACD
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x98）报错
```

## E4 去向（用途锚点）

```asm
; VA: B27F37 —— `vt[0x1E8]`（18 实参）
```

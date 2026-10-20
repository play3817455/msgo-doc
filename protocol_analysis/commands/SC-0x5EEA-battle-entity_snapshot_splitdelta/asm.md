# 汇编证据 —— SC-0x5EEA-battle-entity_snapshot_splitdelta

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9FC4` @ `0xB19403`）

```asm
; VA: 0xB19403（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB19403  push    0x9FC4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— frame_count：偏移 0，长度 4，线类型 u32（帧计数）
0xB1943E  call    sub_B02DD0     ; u32
; 块内日志格式串 "frame_count=" → 含义锚点：0xB1A4B6

; 字段 2 —— remain_msec：偏移 4，长度 4，线类型 u32（剩余毫秒）
0xB19478  call    sub_B02DD0     ; u32
; 块内日志格式串 "remain_msec=" → 含义锚点：0xB1A4E0

; 字段 3 —— ent_id[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（实体 ID 数组（元素 u16 / 槽步进 2，预留 `sub_B05E40`））
0xB194C9  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "ent_id[]=" → 含义锚点：0xB1A4FB

; 字段 4 —— dirty_bits[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（脏位数组（元素 u16））
0xB19548  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "dirty_bits[]=" → 含义锚点：0xB1A570

; 字段 5 —— pos_real_x[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（真实坐标 X（u16））
0xB195C8  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "pos_real_x[]=" → 含义锚点：0xB1A5E5

; 字段 6 —— pos_real_y[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（真实坐标 Y（u16））
0xB19648  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "pos_real_y[]=" → 含义锚点：0xB1A663

; 字段 7 —— pos_real_z[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（真实坐标 Z（u16））
0xB196C8  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "pos_real_z[]=" → 含义锚点：0xB1A6E3

; 字段 8 —— pos_diff_x[]：偏移 （浮动），长度 4+N，线类型 array<u8>（差分坐标 X（u8 / 槽步进 1，预留 `sub_B05EA0`））
0xB19748  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "pos_diff_x[]=" → 含义锚点：0xB1A763

; 字段 9 —— pos_diff_y[]：偏移 （浮动），长度 4+N，线类型 array<u8>（差分坐标 Y（u8））
0xB197BB  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "pos_diff_y[]=" → 含义锚点：0xB1A7D8

; 字段 10 —— pos_diff_z[]：偏移 （浮动），长度 4+N，线类型 array<u8>（差分坐标 Z（u8））
0xB19838  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "pos_diff_z[]=" → 含义锚点：0xB1A854

; 字段 11 —— dir[]：偏移 （浮动），长度 4+N，线类型 array<u8>（朝向（u8））
0xB198AB  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "dir[]=" → 含义锚点：0xB1A8C9

; 字段 12 —— target_real_x[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标真实坐标 X（u16））
0xB19928  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_real_x[]=" → 含义锚点：0xB1A944

; 字段 13 —— target_real_y[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标真实坐标 Y（u16））
0xB199A8  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_real_y[]=" → 含义锚点：0xB1A9C3

; 字段 14 —— target_real_z[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标真实坐标 Z（u16））
0xB19A28  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_real_z[]=" → 含义锚点：0xB1AA43

; 字段 15 —— target_diff_x[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标差分坐标 X（u16））
0xB19AA8  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_diff_x[]=" → 含义锚点：0xB1AAC3

; 字段 16 —— target_diff_y[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标差分坐标 Y（u16））
0xB19B28  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_diff_y[]=" → 含义锚点：0xB1AB43

; 字段 17 —— target_diff_z[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（目标差分坐标 Z（u16））
0xB19BA8  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "target_diff_z[]=" → 含义锚点：0xB1ABC3

; 字段 18 —— spbit_ll[]：偏移 （浮动），长度 4+N，线类型 array<u8>（状态位 ll（u8））
0xB19C35  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "spbit_ll[]=" → 含义锚点：0xB1AC43

; 字段 19 —— spbit_l[]：偏移 （浮动），长度 4+N，线类型 array<u8>（状态位 l（u8））
0xB19CAE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "spbit_l[]=" → 含义锚点：0xB1ACC7

; 字段 20 —— spbit_h[]：偏移 （浮动），长度 4+N，线类型 array<u8>（状态位 h（u8））
0xB19D2E  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "spbit_h[]=" → 含义锚点：0xB1AD47

; 字段 21 —— spbit_hh[]：偏移 （浮动），长度 4+N，线类型 array<u8>（状态位 hh（u8））
0xB19DAE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "spbit_hh[]=" → 含义锚点：0xB1ADC7

; 字段 22 —— spbit2[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（状态位 2（u16））
0xB19E2E  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "spbit2[]=" → 含义锚点：0xB1AE47

; 字段 23 —— hp_percent[]：偏移 （浮动），长度 4+N，线类型 array<u8>（HP 百分比（u8））
0xB19EC4  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "hp_percent[]=" → 含义锚点：0xB1AEC6

; 字段 24 —— hp_percent_shield[]：偏移 （浮动），长度 4+N，线类型 array<u8>（护盾 HP 百分比（u8））
0xB19F3E  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "hp_percent_shield[]=" → 含义锚点：0xB1AF47

; 字段 25 —— down_power[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（被击落力度（u16））
0xB19FBE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "down_power[]=" → 含义锚点：0xB1AFC7

; 字段 26 —— equip_index[]：偏移 （浮动），长度 4+N，线类型 array<u8>（装备索引（u8））
0xB1A054  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "equip_index[]=" → 含义锚点：0xB1B046

; 字段 27 —— score1[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（得分 1（u16））
0xB1A0CE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "score1[]=" → 含义锚点：0xB1B0C7

; 字段 28 —— water_index[]：偏移 （浮动），长度 4+N，线类型 array<u8>（水面索引（u8））
0xB1A164  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "water_index[]=" → 含义锚点：0xB1B146

; 字段 29 —— score2[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（得分 2（u16））
0xB1A1DE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "score2[]=" → 含义锚点：0xB1B1C7

; 字段 30 —— layer_index[]：偏移 （浮动），长度 4+N，线类型 array<u8>（层索引（u8））
0xB1A274  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "layer_index[]=" → 含义锚点：0xB1B246

; 字段 31 —— score3[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（得分 3（u16））
0xB1A2EE  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "score3[]=" → 含义锚点：0xB1B2C7

; 字段 32 —— rideon_ent_id[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（搭乘目标实体 ID（u16））
0xB1A36C  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "rideon_ent_id[]=" → 含义锚点：0xB1B346

; 字段 33 —— lockon_ent_id[]：偏移 （浮动），长度 4+2N，线类型 array<u16>（锁定目标实体 ID（u16））
0xB1A3EA  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "lockon_ent_id[]=" → 含义锚点：0xB1B3C3

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1A435
0xB1A435  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1B671
0xB1B671  mov     <reg>, [obj]; mov <reg>, [<reg>+0x184h]
;       call    <reg>          ; vt[0x184]（64 实参）
```

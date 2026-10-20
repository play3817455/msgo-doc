# 汇编证据 —— SC-0x49C6-battle-weapon_hit_from

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2B` @ `0xB15A7F`）

```asm
; VA: 0xB15A7F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB15A7F  push    0x2B          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（受击实体 ID）
0xB15ABA  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB15DAE

; 字段 2 —— from_ent_id：偏移 2，长度 2，线类型 u16（攻击方实体 ID）
0xB15AFA  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "from_ent_id=" → 含义锚点：0xB15DD9

; 字段 3 —— weapon_itemid：偏移 4，长度 4，线类型 u32（武器道具 ID）
0xB15B1E  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "weapon_itemid=" → 含义锚点：0xB15E03

; 字段 4 —— charge_lv：偏移 8，长度 1，线类型 u8（蓄力等级）
0xB15B42  call    sub_B06230     ; 读 u8
; 块内日志格式串 "charge_lv=" → 含义锚点：0xB15E2B

; 字段 5 —— hp_now：偏移 9，长度 4，线类型 u32（当前 HP）
0xB15B6A  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "hp_now=" → 含义锚点：0xB15E57

; 字段 6 —— hp_max：偏移 13，长度 4，线类型 u32（最大 HP）
0xB15B92  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "hp_max=" → 含义锚点：0xB15E81

; 字段 7 —— damage：偏移 17，长度 4，线类型 u32（伤害值）
0xB15BBA  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "damage=" → 含义锚点：0xB15EAB

; 字段 8 —— spbits：偏移 21，长度 4，线类型 u32（状态位）
0xB15BE2  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "spbits=" → 含义锚点：0xB15ED5

; 字段 9 —— hit_pos_x：偏移 25，长度 2，线类型 u16（命中点 X）
0xB15C0A  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "hit_pos_x=" → 含义锚点：0xB15F00

; 字段 10 —— hit_pos_y：偏移 27，长度 2，线类型 u16（命中点 Y）
0xB15C32  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "hit_pos_y=" → 含义锚点：0xB15F2B

; 字段 11 —— hit_pos_z：偏移 29，长度 2，线类型 u16（命中点 Z）
0xB15C5A  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "hit_pos_z=" → 含义锚点：0xB15F56

; 字段 12 —— hit_dir：偏移 31，长度 2，线类型 u16（受击方向）
0xB15C82  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "hit_dir=" → 含义锚点：0xB15F81

; 字段 13 —— body_region：偏移 33，长度 2，线类型 u16（受击部位）
0xB15CAA  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "body_region=" → 含义锚点：0xB15FAC

; 字段 14 —— optbits：偏移 35，长度 4，线类型 u32（选项位）
0xB15CD2  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "optbits=" → 含义锚点：0xB15FD6

; 字段 15 —— shield_hp_now：偏移 39，长度 4，线类型 u32（护盾当前 HP）
0xB15CFA  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "shield_hp_now=" → 含义锚点：0xB15FFB

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB15D35
0xB15D35  push    <模块/错误码>
0xB15D35  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB160D0
0xB160D0  mov     edx, [obj]
;       mov     edx, [edx+0x1F8h]
;       call    edx          ; vt[0x1F8]（15 实参）
```

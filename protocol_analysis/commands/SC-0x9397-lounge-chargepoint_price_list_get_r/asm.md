# 汇编证据 —— SC-0x9397-lounge-chargepoint_price_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x25` @ `B6D15B`）

```asm
; VA: B6D15B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x25
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— strg_msma：偏移 0，长度 4，线类型 u32（储值-机体价（日志串 `strg_msma=`））
;   `B6D19F`、`B6D44E`
; 字段 2 —— strg_item：偏移 4，长度 4，线类型 u32（储值-道具价（日志串 `strg_item=`））
;   `B6D1E2`、`B6D47B`
; 字段 3 —— clan_emblem：偏移 8，长度 4，线类型 u32（战队徽章价（日志串 `clan_emblem=`））
;   `B6D20C`、`B6D4A8`
; 字段 4 —— clan_npc：偏移 12，长度 4，线类型 u32（战队 NPC 价（日志串 `clan_npc=`））
;   `B6D236`、`B6D4D5`
; 字段 5 —— msma_energy：偏移 16，长度 4，线类型 u32（机体能量价（日志串 `msma_energy=`））
;   `B6D25E`、`B6D4FF`
; 字段 6 —— deckcost：偏移 20，长度 4，线类型 u32（编成费价（日志串 `deckcost=`））
;   `B6D286`、`B6D529`
; 字段 7 —— avatar_reset：偏移 24，长度 4，线类型 u32（头像重置价（日志串 `avatar_reset=`））
;   `B6D2AE`、`B6D553`
; 字段 8 —— periodpath_ticket_0_bc：偏移 28，长度 2，线类型 u16（周期通行证 0 价（日志串 `periodpath_ticket_0_bc=`））
;   `B6D2D6`、`B6D57E`
; 字段 9 —— periodpath_ticket_1_bc：偏移 30，长度 2，线类型 u16（周期通行证 1 价（日志串 `periodpath_ticket_1_bc=`））
;   `B6D2FE`、`B6D5A9`
; 字段 10 —— periodpath_ticket_2_bc：偏移 32，长度 2，线类型 u16（周期通行证 2 价（日志串 `periodpath_ticket_2_bc=`））
;   `B6D326`、`B6D5D4`
; 字段 11 —— periodpath_ticket_0_days：偏移 34，长度 1，线类型 u8（周期通行证 0 天数（日志串 `periodpath_ticket_0_days=`））
;   `B6D34E`、`B6D5FC`
; 字段 12 —— periodpath_ticket_1_days：偏移 35，长度 1，线类型 u8（周期通行证 1 天数（日志串 `periodpath_ticket_1_days=`））
;   `B6D376`、`B6D626`
; 字段 13 —— periodpath_ticket_2_days：偏移 36，长度 1，线类型 u8（周期通行证 2 天数（日志串 `periodpath_ticket_2_days=`））
;   `B6D39E`、`B6D64B`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6D3B2
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x42）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6D712 —— `vt[0xFC]`（13 实参）
```

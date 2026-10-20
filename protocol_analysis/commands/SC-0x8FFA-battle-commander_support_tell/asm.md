# 汇编证据 —— SC-0x8FFA-battle-commander_support_tell

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x27` @ `B23F9D`）

```asm
; VA: B23F9D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x27
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8（队伍编号（日志串 `team=`））
;   `B23FDB`、`B242F4`
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8（部队/阵营（日志串 `troops=`））
;   `B2401B`、`B2431E`
; 字段 3 —— support_type：偏移 2，长度 4，线类型 u32（支援类型（日志串 `support_type=`））
;   `B2403F`、`B2434A`
; 字段 4 —— ent_id：偏移 6，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   `B24063`、`B24375`
; 字段 5 —— target_x：偏移 8，长度 2，线类型 u16（目标坐标 X（日志串 `target_x=`，按有符号打印））
;   `B2408B`、`B243A0`
; 字段 6 —— target_y：偏移 10，长度 2，线类型 u16（目标坐标 Y（日志串 `target_y=`））
;   `B240B3`、`B243CB`
; 字段 7 —— target_z：偏移 12，长度 2，线类型 u16（目标坐标 Z（日志串 `target_z=`））
;   `B240DB`、`B243F6`
; 字段 8 —— spt_ms_index：偏移 14，长度 2，线类型 u16（支援机体索引（日志串 `spt_ms_index=`））
;   `B24103`、`B24421`
; 字段 9 —— spt_spot_index：偏移 16，长度 1，线类型 u8（支援投放点索引（日志串 `spt_spot_index=`））
;   `B2412B`、`B24449`
; 字段 10 —— spt_spot_dir：偏移 17，长度 2，线类型 u16（支援投放朝向（日志串 `spt_spot_dir=`））
;   `B24153`、`B24476`
; 字段 11 —— remain_cnt：偏移 19，长度 2，线类型 u16（剩余次数（日志串 `remain_cnt=`））
;   `B2417B`、`B244A1`
; 字段 12 —— remain_msec：偏移 21，长度 4，线类型 u32（剩余毫秒（日志串 `remain_msec=`））
;   `B241A3`、`B244CB`
; 字段 13 —— use_worldid：偏移 25，长度 4，线类型 u32（使用者世界 ID（日志串 `use_worldid=`））
;   `B241CB`、`B244F5`
; 字段 14 —— use_pilotid：偏移 29，长度 4，线类型 u32（使用者驾驶员 ID（日志串 `use_pilotid=`））
;   `B241F3`、`B2451F`
; 字段 15 —— setter_ms：偏移 33，长度 2，线类型 u16（设置者机体（日志串 `setter_ms=`））
;   `B2421B`、`B2454A`
; 字段 16 —— val：偏移 35，长度 4，线类型 u32（值（日志串 `val=`））
;   `B24243`、`B2456F`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B24257
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xE2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2464E —— `vt[0x2BC]`（14 实参）
```

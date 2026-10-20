# 汇编证据 —— SC-0xB9AB-lounge-msma_buildup_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x20` @ `B76388`）

```asm
; VA: B76388（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x20
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B763C6
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   B763F7|B76406
; 字段 3 —— ticket_id：偏移 12，长度 4，线类型 u32（强化券 ID（日志串 `ticket_id=`））
;   B76446
; 字段 4 —— usenum：偏移 16，长度 2，线类型 u16（使用数量（日志串 `usenum=`））
;   B7646A|B76654
; 字段 5 —— workres：偏移 18，长度 4，线类型 u32（作业结果（日志串 `workres=`））
;   B7648E
; 字段 6 —— buildup_cnt：偏移 22，长度 2，线类型 u16（强化次数（日志串 `buildup_cnt=`））
;   B764B6|B766D4
; 字段 7 —— param_idx：偏移 24，长度 2，线类型 u16（参数索引（日志串 `param_idx=`））
;   B764DE|B766FF
; 字段 8 —— up_param：偏移 26，长度 2，线类型 u16（提升参数（日志串 `up_param=`））
;   B76506
; 字段 9 —— mech_npcpict：偏移 28，长度 4，线类型 u32（机体 NPC 立绘 ID（日志串 `mech_npcpict=`））
;   B7652E
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B76542
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x10C）报错
```

## E4 去向（用途锚点）

```asm
; VA: B767CC —— `vt[0x2C0]`（10 实参）
```

# 汇编证据 —— SC-0xBDD6-battle-roomlobby_pilot_add

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC6` @ `B2A5E8`）

```asm
; VA: B2A5E8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC6
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8（阵营（日志串 `team=`））
;   0xb2a612|0xb2a621
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8（部队（日志串 `troops=`））
;   0xb2a64f|0xb2a65e
; 字段 3 —— world_id：偏移 2，长度 4，线类型 u32（世界 ID（日志串 `world_id=`））
;   0xb2a673|0xb2a682
; 字段 4 —— pilot：偏移 6，长度 159，线类型 struct(176)（玩家详情结构体（日志串 `pilot=` 打印器 `sub_B08AD0`））
;   0xb2a697|0xb2a6a6
; 字段 5 —— stat：偏移 165，长度 4，线类型 u32（状态（日志串 `stat=`））
;   0xb2a6bf|0xb2a6ce
; 字段 6 —— is_commander：偏移 169，长度 1，线类型 u8（是否指挥官（日志串 `is_commander=`））
;   0xb2a6e7|0xb2a6f6
; 字段 7 —— is_audience：偏移 170，长度 1，线类型 u8（是否观战（日志串 `is_audience=`））
;   0xb2a70f|0xb2a71e
; 字段 8 —— member_index：偏移 171，长度 1，线类型 u8（成员序号（日志串 `member_index=`））
;   0xb2a737|0xb2a746
; 字段 9 —— dtaskf_order_number：偏移 172，长度 1，线类型 u8（动态任务部队指令号（日志串 `dtaskf_order_number=`））
;   0xb2a75f|0xb2a76e
; 字段 10 —— kill_count：偏移 173，长度 4，线类型 u32（击杀数（日志串 `kill_count=`））
;   0xb2a787|0xb2a796
; 字段 11 —— death_count：偏移 177，长度 4，线类型 u32（阵亡数（日志串 `death_count=`））
;   0xb2a7af|0xb2a7be
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2A7D2
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2AAAD —— `vt[0x74]`（11 实参）
```

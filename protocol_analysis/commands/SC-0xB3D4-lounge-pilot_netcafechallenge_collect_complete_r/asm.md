# 汇编证据 —— SC-0xB3D4-lounge-pilot_netcafechallenge_collect_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `B73C25`）

```asm
; VA: B73C25（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x12
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B73C63
; 字段 2 —— cnt_completed：偏移 4，长度 4，线类型 u32（网咖挑战完成次数（日志串 `cnt_completed=`））
;   B73CA0
; 字段 3 —— item_id：偏移 8，长度 4，线类型 u32（奖励物品 ID（日志串 `item_id=`））
;   B73CC4
; 字段 4 —— item_cnt：偏移 12，长度 2，线类型 u16（奖励物品数量（日志串 `item_cnt=`））
;   B73CE8|B73EBC
; 字段 5 —— money_gp：偏移 14，长度 4，线类型 u32（奖励 GP（日志串 `money_gp=`））
;   B73D10
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73D24
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x74）报错
```

## E4 去向（用途锚点）

```asm
; VA: B73ED7 —— `vt[0x170]`（5 实参）
```

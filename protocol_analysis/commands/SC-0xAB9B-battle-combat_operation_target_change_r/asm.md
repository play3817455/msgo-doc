# 汇编证据 —— SC-0xAB9B-battle-combat_operation_target_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `B27F6C`）

```asm
; VA: B27F6C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x12
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B27FAA
; 字段 2 —— target_x：偏移 4，长度 2，线类型 u16（目标 X（日志串 `target_x=`））
;   B27FEA
; 字段 3 —— target_y：偏移 6，长度 2，线类型 u16（目标 Y（日志串 `target_y=`））
;   B2800E
; 字段 4 —— target_z：偏移 8，长度 2，线类型 u16（目标 Z（日志串 `target_z=`））
;   B28032
; 字段 5 —— use_worldid：偏移 10，长度 4，线类型 u32（目标世界 ID（日志串 `use_worldid=`））
;   B2805A
; 字段 6 —— use_pilotid：偏移 14，长度 4，线类型 u32（目标驾驶员 ID（日志串 `use_pilotid=`））
;   B28082
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B28096
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xF6）报错
```

## E4 去向（用途锚点）

```asm
; VA: B28284 —— `vt[0x2F8]`（6 实参）
```

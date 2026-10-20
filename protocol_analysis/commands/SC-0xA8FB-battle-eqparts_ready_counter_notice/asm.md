# 汇编证据 —— SC-0xA8FB-battle-eqparts_ready_counter_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE` @ `B26CC6`）

```asm
; VA: B26CC6（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xE
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B26D04
; 字段 2 —— ent_id：偏移 4，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   B26D44
; 字段 3 —— count：偏移 6，长度 4，线类型 u32（当前计数（日志串 `count=`））
;   B26D68
; 字段 4 —— maxcount：偏移 10，长度 4，线类型 u32（计数上限（日志串 `maxcount=`））
;   B26D8C
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B26DA0
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xAA）报错
```

## E4 去向（用途锚点）

```asm
; VA: B26F28 —— `vt[0x21C]`（4 实参）
```

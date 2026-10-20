# 汇编证据 —— SC-0xC64E-battle-roomlobby_pilot_del

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B2B2A2`）

```asm
; VA: B2B2A2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— world_id：偏移 0，长度 4，线类型 u32（世界 ID（日志串 `world_id=`））
;   0xb2b2cc|0xb2b2db
; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（机师 ID（日志串 `pilot_id=`））
;   0xb2b309|0xb2b318
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2B328
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x6）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2B443 —— `vt[0x7C]`（2 实参）
```

# 汇编证据 —— SC-0xC4CB-lounge-clan_rokaku_ms_deck_set_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B78477`）

```asm
; VA: B78477（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb784a1|0xb784b0
; 字段 2 —— uniq_msid：偏移 4，长度 8，线类型 u64（机体唯一序列号（日志串 `uniq_msid=`））
;   0xb784e1|0xb784f0
; 字段 3 —— decktype：偏移 12，长度 4，线类型 u32（卡组类型（日志串 `decktype=`））
;   0xb78505|0xb78514
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B78524
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1E6）报错
```

## E4 去向（用途锚点）

```asm
; VA: B78681 —— `vt[0x494]`（4 实参）
```

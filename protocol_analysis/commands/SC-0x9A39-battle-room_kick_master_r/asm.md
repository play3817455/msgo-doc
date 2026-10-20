# 汇编证据 —— SC-0x9A39-battle-room_kick_master_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B2524D`）

```asm
; VA: B2524D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B2528B`、`B2532F`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B252B4
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x2C）报错
```

## E4 去向（用途锚点）

```asm
; VA: B25388 —— `vt[0xDC]`（1 实参）
```

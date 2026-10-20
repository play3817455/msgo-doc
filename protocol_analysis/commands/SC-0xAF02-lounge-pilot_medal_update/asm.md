# 汇编证据 —— SC-0xAF02-lounge-pilot_medal_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x80` @ `B7231C`）

```asm
; VA: B7231C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x80
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— hav_medal：偏移 0，长度 128，线类型 array<u64,16>（已获得勋章位图（日志串 `hav_medal={...}`，定长 16 项 u64））
;   B7234E|B72366|B72378
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B72390
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x2B）报错
```

## E4 去向（用途锚点）

```asm
; VA: B724C0 —— `vt[0xC8]`（1 实参）
```

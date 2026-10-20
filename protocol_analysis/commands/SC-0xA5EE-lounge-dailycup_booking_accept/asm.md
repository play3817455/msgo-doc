# 汇编证据 —— SC-0xA5EE-lounge-dailycup_booking_accept

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1` @ `B704AA`）

```asm
; VA: B704AA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— is_accept：偏移 0，长度 1，线类型 u8（是否受理（日志串 `is_accept=`，字节打印器））
;   `B704E8`、`B70590`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B70514
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x232）报错
```

## E4 去向（用途锚点）

```asm
; VA: B705EC —— `vt[0x550]`（1 实参）
```

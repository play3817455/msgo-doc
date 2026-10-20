# 汇编证据 —— SC-0xA5FE-lounge-clan_introduction_set_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x228` @ `B7086C`）

```asm
; VA: B7086C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x228
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B708AD`、`B709C0`
; 字段 2 —— intro_info：偏移 4，长度 547，线类型 struct（战队介绍信息（日志串 `intro_info=`；claim == 线长 == 547））
;   `B708DE`、`B708ED`、`B709E8`
; 字段 3 —— clan_kind：偏移 551，长度 1，线类型 u8（战队种类（日志串 `clan_kind=`，字节打印器））
;   `B70911`、`B70A0D`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B70921
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1C9）报错
```

## E4 去向（用途锚点）

```asm
; VA: B70A75 —— `vt[0x454]`（3 实参）
```

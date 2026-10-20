# 汇编证据 —— SC-0xB38B-lounge-chat_invalid_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `B737FB`）

```asm
; VA: B737FB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— is_invalid：偏移 0，长度 2，线类型 u16（聊天屏蔽开关（日志串 `is_invalid=`，打印用 `fmt_i`））
;   B73839|B7392A
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73862
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x5B）报错
```

## E4 去向（用途锚点）

```asm
; VA: B73938 —— `vt[0x134]`（1 实参）
```

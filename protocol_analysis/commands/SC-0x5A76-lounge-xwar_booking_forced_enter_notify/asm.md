# 汇编证据 —— SC-0x5A76-lounge-xwar_booking_forced_enter_notify

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口（零负载，无缓冲申请）

```asm
; 处理块 `0xB633EF`..`0xB6350A` 内**没有** `mov edx,[eax+78h]` + `push IMM; call edx`
```

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何读取原语调用）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB63400
0xB63400  cmp     游标, 末尾      ; 入口闭合校验（失败直接 retn）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB634E2
0xB634E2  mov     <reg>, [obj]; mov <reg>, [<reg>+0x1F4h]
;       call    <reg>          ; vt[0x1F4]（0 实参）
```

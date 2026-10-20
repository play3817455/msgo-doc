# 汇编证据 —— SC-0x3E07-battle-commander_subcmdr_candidacy_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何读取原语调用）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB14F63
0xB14F63  cmp     cursor, end      ; 入口闭合校验（失败直接 retn）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB15045
0xB15045  mov     edx, [obj]
;       mov     edx, [edx+0x2E4h]
;       call    edx          ; vt[0x2E4]（0 实参）
```

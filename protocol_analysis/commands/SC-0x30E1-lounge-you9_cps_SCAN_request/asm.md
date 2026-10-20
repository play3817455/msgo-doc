# 汇编证据 —— SC-0x30E1-lounge-you9_cps_SCAN_request

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何读取原语调用）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5B031
0xB5B031  cmp     cursor, end      ; 入口闭合校验（失败直接 retn）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5B113
0xB5B113  mov     edx, [obj]
;       mov     edx, [edx+0x518h]
;       call    edx          ; vt[0x518]（0 实参）
```

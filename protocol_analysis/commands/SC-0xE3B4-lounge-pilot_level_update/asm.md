# 汇编证据 —— SC-0xE3B4-lounge-pilot_level_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB831ED`）

```asm
; VA: 0xB831ED（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB831ED  push    0x10          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：线类型 u32，线长 4
0xB83228  ...     ; 读点（窗口内第 1 个读事件）
0xB833D2  push    offset apilot_id     ; 日志格式串锚点

; 字段 2 —— lv_new：线类型 u16，线长 2
0xB83265  ...     ; 读点（窗口内第 2 个读事件）
0xB833FD  push    offset alv_new     ; 日志格式串锚点

; 字段 3 —— lv_old：线类型 u16，线长 2
0xB83289  ...     ; 读点（窗口内第 3 个读事件）
0xB83428  push    offset alv_old     ; 日志格式串锚点

; 字段 4 —— lv_point：线类型 u32，线长 4
0xB832AD  ...     ; 读点（窗口内第 4 个读事件）
0xB83452  push    offset alv_point     ; 日志格式串锚点

; 字段 5 —— deckcost：线类型 u16，线长 2
0xB832D5  ...     ; 读点（窗口内第 5 个读事件）
0xB8347D  push    offset adeckcost     ; 日志格式串锚点

; 字段 6 —— reason：线类型 u8，线长 1
0xB832FD  ...     ; 读点（窗口内第 6 个读事件）
0xB834A5  push    offset areason     ; 日志格式串锚点

; 字段 7 —— is_penalty：线类型 u8，线长 1
0xB83325  ...     ; 读点（窗口内第 7 个读事件）
0xB834CA  push    offset ais_penalty     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB83339
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB83554
; mov edx, [client]
; mov edx, [edx+0B4h]
; call edx          ; vt[0x0B4]（7 实参）
```

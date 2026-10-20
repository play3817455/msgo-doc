# 汇编证据 —— SC-0xEA2C-lounge-xwar_booking_info_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1c` @ `0xB84C14`）

```asm
; VA: 0xB84C14（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB84C14  push    0x1c          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— matching_type：线类型 u32，线长 4
0xB84C4F  ...     ; 读点（窗口内第 1 个读事件）
0xB84E02  push    offset amatching_type     ; 日志格式串锚点

; 字段 2 —— is_active：线类型 u32，线长 4
0xB84C8F  ...     ; 读点（窗口内第 2 个读事件）
0xB84E2C  push    offset ais_active     ; 日志格式串锚点

; 字段 3 —— room_cnt：线类型 u32，线长 4
0xB84CB3  ...     ; 读点（窗口内第 3 个读事件）
0xB84E56  push    offset aroom_cnt     ; 日志格式串锚点

; 字段 4 —— book_cntE：线类型 u32，线长 4
0xB84CD7  ...     ; 读点（窗口内第 4 个读事件）
0xB84E80  push    offset abook_cntE     ; 日志格式串锚点

; 字段 5 —— book_cntZ：线类型 u32，线长 4
0xB84CFF  ...     ; 读点（窗口内第 5 个读事件）
0xB84EAA  push    offset abook_cntZ     ; 日志格式串锚点

; 字段 6 —— remain_count：线类型 u32，线长 4
0xB84D27  ...     ; 读点（窗口内第 6 个读事件）
0xB84ED4  push    offset aremain_count     ; 日志格式串锚点

; 字段 7 —— remain_seconds：线类型 u32，线长 4
0xB84D4F  ...     ; 读点（窗口内第 7 个读事件）
0xB84EF9  push    offset aremain_seconds     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB84D63
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB84F7C
; mov edx, [client]
; mov edx, [edx+1E0h]
; call edx          ; vt[0x1E0]（7 实参）
```

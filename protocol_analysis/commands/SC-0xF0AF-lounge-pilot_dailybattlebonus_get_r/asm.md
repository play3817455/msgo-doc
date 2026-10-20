# 汇编证据 —— SC-0xF0AF-lounge-pilot_dailybattlebonus_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x505` @ `0xB85DDD`）

```asm
; VA: 0xB85DDD（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB85DDD  push    0x505          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB85E1B  ...     ; 读点（窗口内第 1 个读事件）
0xB85F41  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— on_event：线类型 u8，线长 1
0xB85E58  ...     ; 读点（窗口内第 2 个读事件）
0xB85F69  push    offset aon_event     ; 日志格式串锚点

; 字段 3 —— bonus_info：线类型 array<bonus_info,40>，线长 1280
0xB85E7E  ...     ; 读点（窗口内第 3 个读事件）
0xB85F86  push    offset abonus_info     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB85EA8
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86035
; mov edx, [client]
; mov edx, [edx+180h]
; call edx          ; vt[0x180]（3 实参）
```

# 汇编证据 —— SC-0xEC71-lounge-season_rankerbattle_set_event_flag

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB8537D`）

```asm
; VA: 0xB8537D（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB8537D  push    0x8          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— event_flag：线类型 u32，线长 4
0xB853B8  ...     ; 读点（窗口内第 1 个读事件）
0xB854A7  push    offset aevent_flag     ; 日志格式串锚点

; 字段 2 —— is_set：线类型 u32，线长 4
0xB853F8  ...     ; 读点（窗口内第 2 个读事件）
0xB854CC  push    offset ais_set     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB85408
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB8552C
; mov edx, [client]
; mov edx, [edx+5B0h]
; call edx          ; vt[0x5B0]（2 实参）
```

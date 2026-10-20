# 汇编证据 —— SC-0xE378-battle-weapon_fire__bit_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1d` @ `0xB2EC76`）

```asm
; VA: 0xB2EC76（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2EC76  push    0x1d          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB2ECB1  ...     ; 读点（窗口内第 1 个读事件）
0xB2EF7D  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— itemid：线类型 u32，线长 4
0xB2ECF1  ...     ; 读点（窗口内第 2 个读事件）
0xB2EFA7  push    offset aitemid     ; 日志格式串锚点

; 字段 3 —— bit_id：线类型 u32，线长 4
0xB2ED15  ...     ; 读点（窗口内第 3 个读事件）
0xB2EFD1  push    offset abit_id     ; 日志格式串锚点

; 字段 4 —— shot_alive：线类型 u8，线长 1
0xB2ED39  ...     ; 读点（窗口内第 4 个读事件）
0xB2EFF9  push    offset ashot_alive     ; 日志格式串锚点

; 字段 5 —— launch_x：线类型 u16，线长 2
0xB2ED61  ...     ; 读点（窗口内第 5 个读事件）
0xB2F026  push    offset alaunch_x     ; 日志格式串锚点

; 字段 6 —— launch_y：线类型 u16，线长 2
0xB2ED89  ...     ; 读点（窗口内第 6 个读事件）
0xB2F051  push    offset alaunch_y     ; 日志格式串锚点

; 字段 7 —— launch_z：线类型 u16，线长 2
0xB2EDB1  ...     ; 读点（窗口内第 7 个读事件）
0xB2F07C  push    offset alaunch_z     ; 日志格式串锚点

; 字段 8 —— target_x：线类型 u16，线长 2
0xB2EDD9  ...     ; 读点（窗口内第 8 个读事件）
0xB2F0A7  push    offset atarget_x     ; 日志格式串锚点

; 字段 9 —— target_y：线类型 u16，线长 2
0xB2EE01  ...     ; 读点（窗口内第 9 个读事件）
0xB2F0D2  push    offset atarget_y     ; 日志格式串锚点

; 字段 10 —— target_z：线类型 u16，线长 2
0xB2EE29  ...     ; 读点（窗口内第 10 个读事件）
0xB2F0FD  push    offset atarget_z     ; 日志格式串锚点

; 字段 11 —— target_ent_id：线类型 u16，线长 2
0xB2EE51  ...     ; 读点（窗口内第 11 个读事件）
0xB2F128  push    offset atarget_ent_id     ; 日志格式串锚点

; 字段 12 —— msec：线类型 u16，线长 2
0xB2EE79  ...     ; 读点（窗口内第 12 个读事件）
0xB2F153  push    offset amsec     ; 日志格式串锚点

; 字段 13 —— release0_shot1：线类型 u8，线长 1
0xB2EEA1  ...     ; 读点（窗口内第 13 个读事件）
0xB2F17B  push    offset arelease0_shot1     ; 日志格式串锚点

; 字段 14 —— fx_opt：线类型 u8，线长 1
0xB2EEC9  ...     ; 读点（窗口内第 14 个读事件）
0xB2F1A0  push    offset afx_opt     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2EEDD
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2F26E
; mov edx, [client]
; mov edx, [edx+1CCh]
; call edx          ; vt[0x1CC]（14 实参）
```

# 汇编证据 —— SC-0xEDFC-battle-weapon_fire__bit_reflect_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x15` @ `0xB2FE88`）

```asm
; VA: 0xB2FE88（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2FE88  push    0x15          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB2FEC3  ...     ; 读点（窗口内第 1 个读事件）
0xB300EF  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— itemid：线类型 u32，线长 4
0xB2FF03  ...     ; 读点（窗口内第 2 个读事件）
0xB30119  push    offset aitemid     ; 日志格式串锚点

; 字段 3 —— launch_x：线类型 u16，线长 2
0xB2FF27  ...     ; 读点（窗口内第 3 个读事件）
0xB30144  push    offset alaunch_x     ; 日志格式串锚点

; 字段 4 —— launch_y：线类型 u16，线长 2
0xB2FF4B  ...     ; 读点（窗口内第 4 个读事件）
0xB3016F  push    offset alaunch_y     ; 日志格式串锚点

; 字段 5 —— launch_z：线类型 u16，线长 2
0xB2FF73  ...     ; 读点（窗口内第 5 个读事件）
0xB3019A  push    offset alaunch_z     ; 日志格式串锚点

; 字段 6 —— target_x：线类型 u16，线长 2
0xB2FF9B  ...     ; 读点（窗口内第 6 个读事件）
0xB301C5  push    offset atarget_x     ; 日志格式串锚点

; 字段 7 —— target_y：线类型 u16，线长 2
0xB2FFC3  ...     ; 读点（窗口内第 7 个读事件）
0xB301F0  push    offset atarget_y     ; 日志格式串锚点

; 字段 8 —— target_z：线类型 u16，线长 2
0xB2FFEB  ...     ; 读点（窗口内第 8 个读事件）
0xB3021B  push    offset atarget_z     ; 日志格式串锚点

; 字段 9 —— charge_lv：线类型 u8，线长 1
0xB30013  ...     ; 读点（窗口内第 9 个读事件）
0xB30243  push    offset acharge_lv     ; 日志格式串锚点

; 字段 10 —— reflect_ent_id：线类型 u16，线长 2
0xB3003B  ...     ; 读点（窗口内第 10 个读事件）
0xB3026B  push    offset areflect_ent_id     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB3004F
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB3030C
; mov edx, [client]
; mov edx, [edx+1ECh]
; call edx          ; vt[0x1EC]（10 实参）
```

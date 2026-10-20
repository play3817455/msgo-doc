# 汇编证据 —— SC-0xE8B6-lounge-chat_world_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xd2` @ `0xB84365`）

```asm
; VA: 0xB84365（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB84365  push    0xd2          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：线类型 u32，线长 4
0xB843A3  ...     ; 读点（窗口内第 1 个读事件）
0xB844A1  push    offset apilot_id     ; 日志格式串锚点

; 字段 2 —— pilot_name：线类型 str，线长 25
0xB843E1  ...     ; 读点（窗口内第 2 个读事件）
0xB844CE  push    offset apilot_name     ; 日志格式串锚点

; 字段 3 —— msg：线类型 str，线长 181
0xB843F8  ...     ; 读点（窗口内第 3 个读事件）
0xB84501  push    offset amsg     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB84408
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB8456F
; mov edx, [client]
; mov edx, [edx+110h]
; call edx          ; vt[0x110]（3 实参）
```

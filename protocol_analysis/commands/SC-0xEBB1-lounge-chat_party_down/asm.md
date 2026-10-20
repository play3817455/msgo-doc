# 汇编证据 —— SC-0xEBB1-lounge-chat_party_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xd2` @ `0xB84FC5`）

```asm
; VA: 0xB84FC5（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB84FC5  push    0xd2          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：线类型 u32，线长 4
0xB85003  ...     ; 读点（窗口内第 1 个读事件）
0xB85101  push    offset apilot_id     ; 日志格式串锚点

; 字段 2 —— pilot_name：线类型 str，线长 25
0xB85041  ...     ; 读点（窗口内第 2 个读事件）
0xB8512E  push    offset apilot_name     ; 日志格式串锚点

; 字段 3 —— msg：线类型 str，线长 181
0xB85058  ...     ; 读点（窗口内第 3 个读事件）
0xB85161  push    offset amsg     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB85068
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB851CF
; mov edx, [client]
; mov edx, [edx+124h]
; call edx          ; vt[0x124]（3 实参）
```

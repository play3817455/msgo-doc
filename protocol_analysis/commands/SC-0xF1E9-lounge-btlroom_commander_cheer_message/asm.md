# 汇编证据 —— SC-0xF1E9-lounge-btlroom_commander_cheer_message

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19` @ `0xB866F4`）

```asm
; VA: 0xB866F4（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB866F4  push    0x19          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_name：线类型 str，线长 25
0xB86721  ...     ; 读点（窗口内第 1 个读事件）
0xB867CE  push    offset apilot_name     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8674D
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86830
; mov edx, [client]
; mov edx, [edx+1C4h]
; call edx          ; vt[0x1C4]（1 实参）
```

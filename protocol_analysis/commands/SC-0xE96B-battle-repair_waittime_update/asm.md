# 汇编证据 —— SC-0xE96B-battle-repair_waittime_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB2F79C`）

```asm
; VA: 0xB2F79C（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2F79C  push    0x2          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— repair_wait_sec：线类型 u16，线长 2
0xB2F7D7  ...     ; 读点（窗口内第 1 个读事件）
0xB2F882  push    offset arepair_wait_sec     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2F803
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2F8DC
; mov edx, [client]
; mov edx, [edx+238h]
; call edx          ; vt[0x238]（1 实参）
```

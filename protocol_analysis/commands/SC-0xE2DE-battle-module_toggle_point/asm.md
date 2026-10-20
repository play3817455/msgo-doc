# 汇编证据 —— SC-0xE2DE-battle-module_toggle_point

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB2E1C1`）

```asm
; VA: 0xB2E1C1（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2E1C1  push    0x6          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB2E1FC  ...     ; 读点（窗口内第 1 个读事件）
0xB2E310  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— point：线类型 u16，线长 2
0xB2E23C  ...     ; 读点（窗口内第 2 个读事件）
0xB2E33B  push    offset apoint     ; 日志格式串锚点

; 字段 3 —— point_max：线类型 u16，线长 2
0xB2E260  ...     ; 读点（窗口内第 3 个读事件）
0xB2E361  push    offset apoint_max     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2E270
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2E3CB
; mov edx, [client]
; mov edx, [edx+378h]
; call edx          ; vt[0x378]（3 实参）
```

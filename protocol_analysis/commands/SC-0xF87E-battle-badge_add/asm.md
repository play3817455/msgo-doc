# 汇编证据 —— SC-0xF87E-battle-badge_add

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB30A6D`）

```asm
; VA: 0xB30A6D（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB30A6D  push    0x2          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— rank：线类型 u8，线长 1
0xB30AA8  ...     ; 读点（窗口内第 1 个读事件）
0xB30B95  push    offset arank     ; 日志格式串锚点

; 字段 2 —— badge_type：线类型 u8，线长 1
0xB30AE8  ...     ; 读点（窗口内第 2 个读事件）
0xB30BBA  push    offset abadge_type     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB30AF8
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB30C1E
; mov edx, [client]
; mov edx, [edx+22Ch]
; call edx          ; vt[0x22C]（2 实参）
```

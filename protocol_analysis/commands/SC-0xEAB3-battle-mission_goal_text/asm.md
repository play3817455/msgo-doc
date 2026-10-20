# 汇编证据 —— SC-0xEAB3-battle-mission_goal_text

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x61` @ `0xB2FB66`）

```asm
; VA: 0xB2FB66（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2FB66  push    0x61          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— text：线类型 str，线长 97
0xB2FB93  ...     ; 读点（窗口内第 1 个读事件）
0xB2FC40  push    offset atext     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2FBBF
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2FCA2
; mov edx, [client]
; mov edx, [edx+334h]
; call edx          ; vt[0x334]（1 实参）
```

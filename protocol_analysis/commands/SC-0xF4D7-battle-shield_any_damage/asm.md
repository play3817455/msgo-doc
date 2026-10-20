# 汇编证据 —— SC-0xF4D7-battle-shield_any_damage

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB30884`）

```asm
; VA: 0xB30884（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB30884  push    0x6          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB308BF  ...     ; 读点（窗口内第 1 个读事件）
0xB309AF  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— damage：线类型 u32，线长 4
0xB308FF  ...     ; 读点（窗口内第 2 个读事件）
0xB309D4  push    offset adamage     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB3090F
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB30A35
; mov edx, [client]
; mov edx, [edx+384h]
; call edx          ; vt[0x384]（2 实参）
```

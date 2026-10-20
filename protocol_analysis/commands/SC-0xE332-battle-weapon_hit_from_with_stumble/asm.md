# 汇编证据 —— SC-0xE332-battle-weapon_hit_from_with_stumble

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB2E57B`）

```asm
; VA: 0xB2E57B（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2E57B  push    0x10          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB2E5B6  ...     ; 读点（窗口内第 1 个读事件）
0xB2E742  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— hit_dir：线类型 u16，线长 2
0xB2E5F6  ...     ; 读点（窗口内第 2 个读事件）
0xB2E76D  push    offset ahit_dir     ; 日志格式串锚点

; 字段 3 —— spbits：线类型 u32，线长 4
0xB2E61A  ...     ; 读点（窗口内第 3 个读事件）
0xB2E797  push    offset aspbits     ; 日志格式串锚点

; 字段 4 —— optbits：线类型 u32，线长 4
0xB2E63E  ...     ; 读点（窗口内第 4 个读事件）
0xB2E7C1  push    offset aoptbits     ; 日志格式串锚点

; 字段 5 —— stumble_power：线类型 u16，线长 2
0xB2E666  ...     ; 读点（窗口内第 5 个读事件）
0xB2E7EC  push    offset astumble_power     ; 日志格式串锚点

; 字段 6 —— stumble_msec：线类型 u16，线长 2
0xB2E68E  ...     ; 读点（窗口内第 6 个读事件）
0xB2E812  push    offset astumble_msec     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2E6A2
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2E892
; mov edx, [client]
; mov edx, [edx+200h]
; call edx          ; vt[0x200]（6 实参）
```

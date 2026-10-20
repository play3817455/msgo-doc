# 汇编证据 —— SC-0xEAEA-battle-weapon_fire_prepare__destruct

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xa` @ `0xB2F928`）

```asm
; VA: 0xB2F928（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2F928  push    0xa          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：线类型 u16，线长 2
0xB2F963  ...     ; 读点（窗口内第 1 个读事件）
0xB2FA77  push    offset aent_id     ; 日志格式串锚点

; 字段 2 —— weapon_itemid：线类型 u32，线长 4
0xB2F9A3  ...     ; 读点（窗口内第 2 个读事件）
0xB2FAA1  push    offset aweapon_itemid     ; 日志格式串锚点

; 字段 3 —— fire_id：线类型 u32，线长 4
0xB2F9C7  ...     ; 读点（窗口内第 3 个读事件）
0xB2FAC6  push    offset afire_id     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2F9D7
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2FB2E
; mov edx, [client]
; mov edx, [edx+1D0h]
; call edx          ; vt[0x1D0]（3 实参）
```

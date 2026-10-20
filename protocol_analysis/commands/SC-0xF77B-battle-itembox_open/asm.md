# 汇编证据 —— SC-0xF77B-battle-itembox_open

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xa` @ `0xB30646`）

```asm
; VA: 0xB30646（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB30646  push    0xa          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— itembox_ent_id：线类型 u16，线长 2
0xB30681  ...     ; 读点（窗口内第 1 个读事件）
0xB30795  push    offset aitembox_ent_id     ; 日志格式串锚点

; 字段 2 —— itemid：线类型 u32，线长 4
0xB306C1  ...     ; 读点（窗口内第 2 个读事件）
0xB307BF  push    offset aitemid     ; 日志格式串锚点

; 字段 3 —— trap_weaponid：线类型 u32，线长 4
0xB306E5  ...     ; 读点（窗口内第 3 个读事件）
0xB307E4  push    offset atrap_weaponid     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB306F5
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB3084C
; mov edx, [client]
; mov edx, [edx+288h]
; call edx          ; vt[0x288]（3 实参）
```

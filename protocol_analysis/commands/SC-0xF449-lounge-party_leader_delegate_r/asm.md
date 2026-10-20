# 汇编证据 —— SC-0xF449-lounge-party_leader_delegate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB86DD4`）

```asm
; VA: 0xB86DD4（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB86DD4  push    0x8          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id_old_leader：线类型 u32，线长 4
0xB86E0F  ...     ; 读点（窗口内第 1 个读事件）
0xB86EFE  push    offset apilot_id_old_leader     ; 日志格式串锚点

; 字段 2 —— pilot_id_new_leader：线类型 u32，线长 4
0xB86E4F  ...     ; 读点（窗口内第 2 个读事件）
0xB86F23  push    offset apilot_id_new_leader     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB86E5F
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86F83
; mov edx, [client]
; mov edx, [edx+208h]
; call edx          ; vt[0x208]（2 实参）
```

# 汇编证据 —— SC-0xEE0F-lounge-msma_equip_rental_modules_update_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3c` @ `0xB856EF`）

```asm
; VA: 0xB856EF（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB856EF  push    0x3c          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB8572A  ...     ; 读点（窗口内第 1 个读事件）
0xB858CD  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— uniqid_ms：线类型 u64，线长 8
0xB8576A  ...     ; 读点（窗口内第 2 个读事件）
0xB858FB  push    offset auniqid_ms     ; 日志格式串锚点

; 字段 3 —— eq_modules：线类型 u32[10]，线长 40
0xB85796  ...     ; 读点（窗口内第 3 个读事件）
0xB85916  push    offset aeq_modules     ; 日志格式串锚点

; 字段 4 —— eq_rental_modules：线类型 u32[1]，线长 4
0xB857D9  ...     ; 读点（窗口内第 4 个读事件）
0xB85975  push    offset aeq_rental_modules     ; 日志格式串锚点

; 字段 5 —— cost：线类型 u32，线长 4
0xB8581A  ...     ; 读点（窗口内第 5 个读事件）
0xB859B4  push    offset acost     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8582E
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB85A2D
; mov edx, [client]
; mov edx, [edx+27Ch]
; call edx          ; vt[0x27C]（6 实参）
```

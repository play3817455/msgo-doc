# 汇编证据 —— SC-0xF659-lounge-pilot_over_custom_level_up_estimate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xc` @ `0xB86FBB`）

```asm
; VA: 0xB86FBB（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB86FBB  push    0xc          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB86FF6  ...     ; 读点（窗口内第 1 个读事件）
0xB87109  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— price_gp：线类型 u32，线长 4
0xB87036  ...     ; 读点（窗口内第 2 个读事件）
0xB87133  push    offset aprice_gp     ; 日志格式串锚点

; 字段 3 —— price_cp：线类型 u32，线长 4
0xB8705A  ...     ; 读点（窗口内第 3 个读事件）
0xB87158  push    offset aprice_cp     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8706A
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB871BF
; mov edx, [client]
; mov edx, [edx+5B8h]
; call edx          ; vt[0x5B8]（3 实参）
```

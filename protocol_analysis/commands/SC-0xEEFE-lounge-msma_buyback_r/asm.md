# 汇编证据 —— SC-0xEEFE-lounge-msma_buyback_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xc` @ `0xB85A65`）

```asm
; VA: 0xB85A65（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB85A65  push    0xc          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB85AA0  ...     ; 读点（窗口内第 1 个读事件）
0xB85BA9  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— uniqid_ms：线类型 u64，线长 8
0xB85AE0  ...     ; 读点（窗口内第 2 个读事件）
0xB85BCE  push    offset auniqid_ms     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB85B0C
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB85C32
; mov edx, [client]
; mov edx, [edx+324h]
; call edx          ; vt[0x324]（3 实参）
```

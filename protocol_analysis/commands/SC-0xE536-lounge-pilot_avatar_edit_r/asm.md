# 汇编证据 —— SC-0xE536-lounge-pilot_avatar_edit_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x51c` @ `0xB83C90`）

```asm
; VA: 0xB83C90（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB83C90  push    0x51c          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB83CCE  ...     ; 读点（窗口内第 1 个读事件）
0xB83DFC  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— avatar：线类型 struct<avatar>，线长 18
0xB83D0B  ...     ; 读点（窗口内第 2 个读事件）
0xB83E24  push    offset aavatar     ; 日志格式串锚点

; 字段 3 —— hav_avatar：线类型 u64[160]，线长 1280
0xB83D36  ...     ; 读点（窗口内第 3 个读事件）
0xB83E41  push    offset ahav_avatar     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB83D63
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB83EFD
; mov edx, [client]
; mov edx, [edx+0CCh]
; call edx          ; vt[0x0CC]（3 实参）
```

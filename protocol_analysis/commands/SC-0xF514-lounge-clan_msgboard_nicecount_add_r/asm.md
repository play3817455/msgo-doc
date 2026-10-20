# 汇编证据 —— SC-0xF514-lounge-clan_msgboard_nicecount_add_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB86BEC`）

```asm
; VA: 0xB86BEC（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB86BEC  push    0x5          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB86C27  ...     ; 读点（窗口内第 1 个读事件）
0xB86D16  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— clan_kind：线类型 u8，线长 1
0xB86C67  ...     ; 读点（窗口内第 2 个读事件）
0xB86D39  push    offset aclan_kind     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB86C77
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86D9C
; mov edx, [client]
; mov edx, [edx+47Ch]
; call edx          ; vt[0x47C]（2 实参）
```

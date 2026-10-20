# 汇编证据 —— SC-0xE7C5-lounge-pilot_lvpt_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB841F8`）

```asm
; VA: 0xB841F8（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB841F8  push    0x4          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— lvpt_now：线类型 u32，线长 4
0xB84233  ...     ; 读点（窗口内第 1 个读事件）
0xB842D7  push    offset alvpt_now     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8425C
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB84330
; mov edx, [client]
; mov edx, [edx+0B0h]
; call edx          ; vt[0x0B0]（1 实参）
```

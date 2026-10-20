# 汇编证据 —— SC-0xF175-lounge-dailycup_bracket_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB86868`）

```asm
; VA: 0xB86868（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB86868  push    0x4          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— index：线类型 u32，线长 4
0xB868A3  ...     ; 读点（窗口内第 1 个读事件）
0xB8694D  push    offset aindex     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB868CF
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB869A6
; mov edx, [client]
; mov edx, [edx+548h]
; call edx          ; vt[0x548]（1 实参）
```

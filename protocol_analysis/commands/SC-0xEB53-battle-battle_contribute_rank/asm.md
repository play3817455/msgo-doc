# 汇编证据 —— SC-0xEB53-battle-battle_contribute_rank

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB2FCDA`）

```asm
; VA: 0xB2FCDA（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2FCDA  push    0x4          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— rank：线类型 u32，线长 4
0xB2FD15  ...     ; 读点（窗口内第 1 个读事件）
0xB2FDBF  push    offset arank     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2FD41
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2FE18
; mov edx, [client]
; mov edx, [edx+230h]
; call edx          ; vt[0x230]（1 实参）
```

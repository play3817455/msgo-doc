# 汇编证据 —— SC-0xEE0B-lounge-pilot_cmdr_fame_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB8557F`）

```asm
; VA: 0xB8557F（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB8557F  push    0x4          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— fame_now：线类型 u32，线长 4
0xB855BA  ...     ; 读点（窗口内第 1 个读事件）
0xB8565E  push    offset afame_now     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB855E3
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB856B7
; mov edx, [client]
; mov edx, [edx+0B8h]
; call edx          ; vt[0x0B8]（1 实参）
```

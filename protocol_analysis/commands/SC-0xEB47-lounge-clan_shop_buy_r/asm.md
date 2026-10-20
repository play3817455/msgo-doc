# 汇编证据 —— SC-0xEB47-lounge-clan_shop_buy_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB85207`）

```asm
; VA: 0xB85207（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB85207  push    0x4          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB85242  ...     ; 读点（窗口内第 1 个读事件）
0xB852EC  push    offset aresult     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8526E
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB85345
; mov edx, [client]
; mov edx, [edx+4A0h]
; call edx          ; vt[0x4A0]（1 实参）
```

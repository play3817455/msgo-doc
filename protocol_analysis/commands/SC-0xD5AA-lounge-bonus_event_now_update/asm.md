# 汇编证据 —— SC-0xD5AA-lounge-bonus_event_now_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x100` @ `B7D1EE`）

```asm
00B7D1D9  call    sub_B41120        ; lounge 守卫
00B7D1EE  push    100h              ; 容量 = 0x100
00B7D1F3  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7D21D  call    sub_B412E0        ; 一次推进 0x100 整块预留（非字段）
00B7D22E  call    sub_B43360        ; 字段 1 events 元素读取器（16×u32 = 64B）
00B7D240  cmp     edi, 4            ; 固定 4 元（无线上 count）
00B7D242  jb      short loc_B7D228
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7D258  cmp     ecx, [esp+2C5Ch+var_2C40]
00B7D277  jz      short loc_B7D277
```

## E4 去向（用途锚点）

```asm
00B7D386  call    edx               ; vt[0x138]，1 实参
```

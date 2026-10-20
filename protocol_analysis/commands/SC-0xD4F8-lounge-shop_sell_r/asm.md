# 汇编证据 —— SC-0xD4F8-lounge-shop_sell_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B7CAC5`）

```asm
00B7CAA5  call    sub_B41120        ; lounge 守卫
00B7CAC5  push    4                 ; 容量 = 0x4
00B7CAC8  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7CAF5  call    sub_B02DD0        ; 字段 1 result：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7CB21  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7CB23  jnz     short loc_B7CB03
```

## E4 去向（用途锚点）

```asm
00B7CBF8  call    edx               ; vt[0x3B8]，1 实参
```

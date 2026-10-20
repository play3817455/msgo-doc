# 汇编证据 —— SC-0xD6BC-lounge-msma_deckslot_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11` @ `B7EBC3`）

```asm
00B7EBAE  call    sub_B41120        ; lounge 守卫
00B7EBC3  push    11h               ; 容量 = 0x11
00B7EBC5  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7EBFE  call    sub_B02DD0        ; 1 result：u32
00B7EC3E  call    sub_B06200        ; 2 uniqid：u64
00B7EC62  call    sub_B02DF0        ; 3 decktype：u16
00B7EC86  call    sub_B02DF0        ; 4 deckslot：u16
00B7ECAE  call    sub_B06230        ; 5 is_costover：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7ECC2  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7ECC8  jz      short loc_B7ECE4
```

## E4 去向（用途锚点）

```asm
00B7EE86  call    edx               ; vt[0x24C]，6 实参
```

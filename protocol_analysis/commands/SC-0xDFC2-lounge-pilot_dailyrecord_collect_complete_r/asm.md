# 汇编证据 —— SC-0xDFC2-lounge-pilot_dailyrecord_collect_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `B82140`）

```asm
00B8212B  call    sub_B41120        ; lounge 守卫
00B82140  push    12h               ; 容量 = 0x12
00B82145  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B8217B  call    sub_B02DD0        ; 1 result：u32
00B821B8  call    sub_B02DD0        ; 2 cnt_completed：u32
00B821DC  call    sub_B02DD0        ; 3 item_id：u32
00B82200  call    sub_B02DF0        ; 4 item_cnt：u16
00B82228  call    sub_B02DD0        ; 5 money_gp：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B8223C  cmp     ebx, [esp+2C5Ch+var_2C40]
00B82242  jz      short loc_B8225B
```

## E4 去向（用途锚点）

```asm
00B823EF  call    edx               ; vt[0x164]，5 实参
```

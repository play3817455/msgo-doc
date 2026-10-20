# 汇编证据 —— SC-0xE014-battle-battleship_ride_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x20` @ `B2D9C1`）

```asm
00B2D9AF  call    sub_B05DA0        ; battle 守卫
00B2D9C4  push    20h ; char        ; 容量 = 0x20
00B2D9C6  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2D9FF  call    sub_B02DD0        ; 1 result：u32
00B2DA3F  call    sub_B02DD0        ; 2 from_world_id：u32
00B2DA63  call    sub_B02DD0        ; 3 from_pilot_id：u32
00B2DA87  call    sub_B02DF0        ; 4 from_ent_id：u16
00B2DAAF  call    sub_B02DF0        ; 5 to_ent_id：u16
00B2DAD7  call    sub_B02DD0        ; 6 hp_now：u32
00B2DAFF  call    sub_B02DD0        ; 7 hp_max：u32
00B2DB27  call    sub_B02DD0        ; 8 shield_hp_now：u32
00B2DB4F  call    sub_B02DD0        ; 9 shield_hp_max：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2DB63  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2DB69  jz      short loc_B2DB85
```

## E4 去向（用途锚点）

```asm
00B2DDE2  call    eax               ; vt[0x304]，9 实参
```

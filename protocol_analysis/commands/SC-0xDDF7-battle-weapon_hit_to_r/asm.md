# 汇编证据 —— SC-0xDDF7-battle-weapon_hit_to_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B2D00D`）

```asm
00B2CFF8  call    sub_B05DA0        ; battle 守卫
00B2D00D  push    10h               ; 容量 = 0x10
00B2D012  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2D048  call    sub_B02DD0        ; 1 weapon_itemid：u32
00B2D088  call    sub_B02DF0        ; 2 ent_id：u16
00B2D0AC  call    sub_B02DD0        ; 3 optbit：u32
00B2D0D0  call    sub_B02DF0        ; 4 hit_pos_x：u16
00B2D0F8  call    sub_B02DF0        ; 5 hit_pos_y：u16
00B2D120  call    sub_B02DF0        ; 6 hit_pos_z：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2D134  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2D13A  jz      short loc_B2D156
```

## E4 去向（用途锚点）

```asm
00B2D324  call    eax               ; vt[0x1F0]，6 实参
```

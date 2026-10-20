# 汇编证据 —— SC-0xD725-battle-weapon_fire__wrestle_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x15` @ `B2C0F3`）

```asm
00B2C0DE  call    sub_B05DA0        ; battle 守卫
00B2C0F3  push    15h               ; 容量 = 0x15
00B2C0F8  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2C12E  call    sub_B02DF0        ; 1 ent_id：u16
00B2C16B  call    sub_B02DD0        ; 2 itemid：u32
00B2C18F  call    sub_B02DF0        ; 3 dir_h：u16
00B2C1B3  call    sub_B02DF0        ; 4 dir_v：u16
00B2C1DB  call    sub_B02DF0        ; 5 msec：u16
00B2C203  call    sub_B02DD0        ; 6 wrestle_id：u32
00B2C22B  call    sub_B06230        ; 7 charge_lv：u8
00B2C253  call    sub_B06230        ; 8 action：u8
00B2C27B  call    sub_B02DF0        ; 9 chase_ent_id：u16
00B2C2A3  call    sub_B06230        ; 10 is_dp_damage_cut：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2C2B7  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2C2BD  jz      short loc_B2C2D6
```

## E4 去向（用途锚点）

```asm
00B2C56A  call    edx               ; vt[0x1A8]，10 实参
```

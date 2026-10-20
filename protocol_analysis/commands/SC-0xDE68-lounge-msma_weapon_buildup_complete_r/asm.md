# 汇编证据 —— SC-0xDE68-lounge-msma_weapon_buildup_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x24` @ `B81851`）

```asm
00B8183F  call    sub_B41120        ; lounge 守卫
00B81854  push    24h ; char        ; 容量 = 0x24
00B81856  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B8188F  call    sub_B02DD0        ; 1 result：u32
00B818CF  call    sub_B06200        ; 2 uniqid_ms：u64
00B8190F  call    sub_B02DD0        ; 3 item_id：u32
00B81933  call    sub_B02DD0        ; 4 ticket_id：u32
00B81957  call    sub_B02DF0        ; 5 usenum：u16
00B8197F  call    sub_B02DF0        ; 6 param_target：u16
00B819A7  call    sub_B02DD0        ; 7 workres：u32
00B819CF  call    sub_B02DF0        ; 8 buildup_cnt：u16
00B819F7  call    sub_B02DF0        ; 9 up_param：u16
00B81A1F  call    sub_B02DD0        ; 10 mech_npcpict：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B81A33  cmp     eax, [esp+2C5Ch+var_2C40]
00B81A55  jz      short loc_B81A55
```

## E4 去向（用途锚点）

```asm
00B81CEE  call    edx               ; vt[0x2D4]，11 实参
```

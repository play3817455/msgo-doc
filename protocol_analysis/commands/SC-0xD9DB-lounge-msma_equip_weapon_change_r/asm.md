# 汇编证据 —— SC-0xD9DB-lounge-msma_equip_weapon_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12` @ `B7F663`）

```asm
00B7F64E  call    sub_B41120        ; lounge 守卫
00B7F663  push    12h               ; 容量 = 0x12
00B7F668  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7F69E  call    sub_B02DD0        ; 1 result：u32
00B7F6DE  call    sub_B06200        ; 2 uniqid_ms：u64
00B7F702  call    sub_B02DF0        ; 3 eq_slot：u16
00B7F726  call    sub_B02DD0        ; 4 item_id：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7F73A  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7F740  jz      short loc_B7F75C
```

## E4 去向（用途锚点）

```asm
00B7F8CA  call    edx               ; vt[0x254]，5 实参
```

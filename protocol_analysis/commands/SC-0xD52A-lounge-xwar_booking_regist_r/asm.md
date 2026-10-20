# 汇编证据 —— SC-0xD52A-lounge-xwar_booking_regist_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19` @ `B7D3BE`）

```asm
00B7D3A9  call    sub_B41120        ; lounge 守卫
00B7D3BE  push    19h               ; 容量 = 0x19
00B7D3C0  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7D3F9  call    sub_B02DD0        ; 1 result：u32
00B7D439  call    sub_B02DD0        ; 2 matching_type：u32
00B7D45D  call    sub_B06230        ; 3 is_newbie：u8
00B7D481  call    sub_B02DD0        ; 4 matching_request_flag：u32
00B7D4A9  call    sub_B02DD0        ; 5 matching_battlerule_flag：u32
00B7D4D1  call    sub_B02DD0        ; 6 matching_extrule_flag：u32
00B7D4F9  call    sub_B06230        ; 7 is_party_wait：u8
00B7D521  call    sub_B02DF0        ; 8 party_wait_sec：u16
00B7D549  call    sub_B06230        ; 9 is_party_readyNG：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7D55D  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7D57F  jz      short loc_B7D57F
```

## E4 去向（用途锚点）

```asm
00B7D7E3  call    eax               ; vt[0x1E4]，9 实参
00B7D79B  push    edx               ; is_party_readyNG
00B7D7A3  push    edx               ; party_wait_sec
00B7D7AD  push    edx               ; is_party_wait
00B7D7BA  push    edx               ; matching_extrule_flag
00B7D7C1  push    edx               ; matching_battlerule_flag
00B7D7C8  push    edx               ; matching_request_flag
00B7D7D3  push    edx               ; is_newbie
00B7D7DD  push    edx               ; matching_type
00B7D7E0  push    edx               ; result
```

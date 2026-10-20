# 汇编证据 —— SC-0xE13A-lounge-pilot_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x501` @ `B82604`）

```asm
00B825EF  call    sub_B41120        ; lounge 守卫
00B82604  push    501h              ; 容量 = 0x501
00B82609  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序，节选）

```asm
00B82642  call    sub_B02DD0        ; 1 result：u32
00B82670  call    sub_B41350        ; 预留 0x1A8=424B（非字段）
00B82686  call    sub_B42BB0        ; 2 pilots_eff：struct（398B）
00B8269B  cmp     edi, 1            ; 固定 1 元
00B826B8  call    sub_B41350        ; 预留（非字段）
00B826C9  call    sub_B42BB0        ; 3 pilots_zeon：struct（398B）
00B8270C  call    sub_B02DD0        ; 4 del_remain_sec_eff：u32
00B8274C  call    sub_B02DD0        ; 5 del_remain_sec_zeon：u32
00B8278C  call    sub_B02DD0        ; 6 pilot_rename_remaintime_eff：u32
00B827CC  call    sub_B02DD0        ; 7 pilot_rename_remaintime_zeon：u32
00B82809  call    sub_B02DD0        ; 8 charge_point：u32
00B82838  call    sub_B02DD0        ; 9 bmgpack_num：u32
00B8284C  cmp     ebx, 10h          ; 上限 16
00B82880  call    sub_B458A0        ; 10 bmgpack_list 元素（23B/元素）
00B828BD  call    sub_B06230        ; 11 is_tutorial_end：u8
00B828DF  call    sub_B02DD0        ; 12 pilot_rename_price：u32
00B82905  call    sub_B02DD0        ; 13 pilot_rename_time_efsf：u32
00B8292D  call    sub_B02DD0        ; 14 pilot_rename_forbidtime_efsf：u32
00B82955  call    sub_B02DD0        ; 15 pilot_rename_time_zeon：u32
00B8297D  call    sub_B02DD0        ; 16 pilot_rename_forbidtime_zeon：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B82991  cmp     ecx, [esp+2C5Ch+var_2C40]
00B82997  jz      short loc_B829B0
```

## E4 去向（用途锚点，低槽）

```asm
00B82DD3  call    eax               ; vt[0x84]，16 实参
```

# 汇编证据 —— SC-0xDC47-lounge-pilot_record_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x74E` @ `B80AD9`）

```asm
00B80AC4  call    sub_B41120        ; lounge 守卫
00B80AD9  push    74Eh              ; 容量 = 0x74E
00B80ADE  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B80B17  call    sub_B02DD0        ; 1 result：u32
00B80B54  call    sub_B02DD0        ; 2 pilot_id：u32
00B80B78  call    sub_B02DD0        ; 3 world_id：u32
00B80B9C  call    sub_B440B0        ; 4 precord：struct（242B，claim 0xFC）
00B80BC6  call    sub_B44610        ; 5 pbadge 元素（152B ×3）
00B80BDB  cmp     edi, 3            ; 固定 3 元
00B80C09  call    sub_B06200        ; 6 hav_medal 元素：u64
00B80C1B  cmp     edi, 10h          ; 固定 16 元（无线上 count）
00B80C49  call    sub_B43E00        ; 7 msdeck 元素（324B ×2，槽 324；体内读 8×(4×u32)+4×(10×u32)+4×u32+4×u32+4×u8）
00B80C5E  cmp     edi, 2            ; 固定 2 元
00B80C8A  call    sub_B44750        ; 8 lvjudge_hist：struct（369B，claim 0x174）
00B80CC9  call    sub_B02DF0        ; 9 plvhist：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B80CF3  cmp     ecx, [esp+2C5Ch+var_2C40]
00B80CF9  jz      short loc_B80D12
```

## E4 去向（用途锚点）

```asm
00B81009  call    edx               ; vt[0x154]，9 实参
```

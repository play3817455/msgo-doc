# 汇编证据 —— SC-0xDCF2-battle-roomlobby_pilot_msdeck

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x24` @ `B2CC11`）

```asm
00B2CBFC  call    sub_B05DA0        ; battle 守卫
00B2CC11  push    24h ; char        ; 容量 = 0x24
00B2CC13  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2CC4C  call    sub_B02DD0        ; 1 world_id：u32
00B2CC89  call    sub_B02DD0        ; 2 pilot_id：u32
00B2CC9F  call    sub_B02DD0        ; 3 deck_msid_num：u32
00B2CCC8  cmp     ebx, 4            ; 上限 4
00B2CCDA  call    sub_B41850        ; 预留 4B/槽（非字段）
00B2CCFA  call    sub_B02DD0        ; 4 deck_msid 元素：u32
00B2CD2B  call    sub_B02DD0        ; 5 deck_mscolor_num：u32
00B2CD57  call    sub_B05EA0        ; 预留 1B/槽（非字段）
00B2CD70  call    sub_B06230        ; 6 deck_mscolor 元素：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2CD98  cmp     ecx, [esp+1B3Ch+var_1B24]
00B2CD9E  jz      short loc_B2CDB7
```

## E4 去向（用途锚点）

```asm
00B2CFB0  call    eax               ; vt[0x80]，6 实参
```

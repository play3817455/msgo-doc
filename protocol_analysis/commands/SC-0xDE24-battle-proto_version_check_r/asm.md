# 汇编证据 —— SC-0xDE24-battle-proto_version_check_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B2D597`）

```asm
00B2D582  call    sub_B05DA0        ; battle 守卫
00B2D597  push    0Ch               ; 容量 = 0xC
00B2D59C  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2D5D2  call    sub_B02DD0        ; 1 version：u32
00B2D60F  call    sub_B02DD0        ; 2 crc：u32
00B2D633  call    sub_B02DD0        ; 3 gentime：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2D643  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2D649  jz      short loc_B2D662
```

## E4 去向（用途锚点）

```asm
00B2D78D  call    eax               ; vt[0x6C]，3 实参
```

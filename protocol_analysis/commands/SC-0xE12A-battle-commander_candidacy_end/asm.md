# 汇编证据 —— SC-0xE12A-battle-commander_candidacy_end

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B2DE1A`）

```asm
00B2DE05  call    sub_B05DA0        ; battle 守卫
00B2DE1A  push    0Ch               ; 容量 = 0xC
00B2DE1C  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2DE55  call    sub_B02DD0        ; 1 result：u32
00B2DE95  call    sub_B02DD0        ; 2 cmdr_world_id：u32
00B2DEB9  call    sub_B02DD0        ; 3 cmdr_pilot_id：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2DEC9  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2DECF  jz      short loc_B2DEEB
```

## E4 去向（用途锚点）

```asm
00B2E01E  call    eax               ; vt[0x2A0]，3 实参
```

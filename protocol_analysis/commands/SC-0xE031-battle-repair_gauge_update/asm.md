# 汇编证据 —— SC-0xE031-battle-repair_gauge_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B2D7D9`）

```asm
00B2D7C4  call    sub_B05DA0        ; battle 守卫
00B2D7D9  push    4                 ; 容量 = 0x4
00B2D7DB  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2D814  call    sub_B02DF0        ; 1 gauge_old：u16
00B2D854  call    sub_B02DF0        ; 2 gauge_now：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2D864  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2D86A  jz      short loc_B2D886
```

## E4 去向（用途锚点）

```asm
00B2D98C  call    eax               ; vt[0x234]，2 实参
```

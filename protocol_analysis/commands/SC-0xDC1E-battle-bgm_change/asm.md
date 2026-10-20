# 汇编证据 —— SC-0xDC1E-battle-bgm_change

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19` @ `B2C847`）

```asm
00B2C832  call    sub_B05DA0        ; battle 守卫
00B2C847  push    19h               ; 容量 = 0x19
00B2C84C  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2C873  call    sub_B41740        ; 预留 0x14=20B 结构体槽（非字段）
00B2C882  call    sub_B07E00        ; 1 bgm_desc：struct（14B）
00B2C8C2  call    sub_B02DD0        ; 2 fade_msec：u32
00B2C8E6  call    sub_B06230        ; 3 reset：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2C8F6  cmp     ecx, [esp+1B3Ch+var_1B24]
00B2C8FC  jz      short loc_B2C918
```

## E4 去向（用途锚点）

```asm
00B2CA66  call    eax               ; vt[0x31C]，2 实参
```

# 汇编证据 —— SC-0xDE24-lounge-proto_version_check_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B81D23`）

```asm
00B81D0E  call    sub_B41120        ; lounge 守卫
00B81D23  push    0Ch               ; 容量 = 0xC
00B81D25  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B81D5E  call    sub_B02DD0        ; 1 version：u32
00B81D9B  call    sub_B02DD0        ; 2 crc：u32
00B81DBF  call    sub_B02DD0        ; 3 gentime：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B81DCF  cmp     ebx, [esp+2C5Ch+var_2C40]
00B81DD5  jz      short loc_B81DEE
```

## E4 去向（用途锚点）

```asm
00B81F19  call    eax               ; vt[0x68]，3 实参
```

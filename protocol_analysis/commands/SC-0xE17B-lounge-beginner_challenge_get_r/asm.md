# 汇编证据 —— SC-0xE17B-lounge-beginner_challenge_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1CC` @ `B82FF2`）

```asm
00B82FDD  call    sub_B41120        ; lounge 守卫
00B82FF2  push    1CCh              ; 容量 = 0x1CC
00B82FF7  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B83030  call    sub_B02DD0        ; 1 result：u32
00B83061  call    sub_B41AF0        ; 预留 0x1C8=456B（非字段）
00B83070  call    sub_B42440        ; 2 info：struct（454B）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B83080  cmp     ebx, [esp+2C5Ch+var_2C40]
00B83086  jz      short loc_B830A2
```

## E4 去向（用途锚点）

```asm
00B831A2  call    eax               ; vt[0x5DC]，2 实参
```

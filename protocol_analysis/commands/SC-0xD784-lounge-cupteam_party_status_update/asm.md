# 汇编证据 —— SC-0xD784-lounge-cupteam_party_status_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4C` @ `B7F22D`）

```asm
00B7F220  call    sub_B41120        ; lounge 守卫
00B7F235  push    4Ch ; char        ; 容量 = 0x4C
00B7F237  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7F270  call    sub_B02DD0        ; 1 cupteam_rate：u32
00B7F2B0  call    sub_B02DD0        ; 2 last_bracket_id：u32
00B7F2D4  call    sub_B46D20        ; 3 phase：struct（13B，claim 0x10）
00B7F2F8  call    sub_B46D80        ; 4 bracket：struct（46B，claim 0x34）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7F30C  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7F312  jz      short loc_B7F32E
```

## E4 去向（用途锚点）

```asm
00B7F48E  call    edx               ; vt[0x4F8]，4 实参
```

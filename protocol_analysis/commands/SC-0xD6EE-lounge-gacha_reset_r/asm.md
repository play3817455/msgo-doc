# 汇编证据 —— SC-0xD6EE-lounge-gacha_reset_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7EEBE`）

```asm
00B7EEA9  call    sub_B41120        ; lounge 守卫
00B7EEBE  push    8                 ; 容量 = 0x8
00B7EEC0  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7EEF9  call    sub_B02DD0        ; 1 result：u32
00B7EF39  call    sub_B02DD0        ; 2 gacha_id：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7EF49  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7EF4F  jz      short loc_B7EF6B
```

## E4 去向（用途锚点）

```asm
00B7F06D  call    edx               ; vt[0x3EC]，2 实参
```

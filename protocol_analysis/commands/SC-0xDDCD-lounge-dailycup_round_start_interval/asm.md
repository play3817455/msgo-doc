# 汇编证据 —— SC-0xDDCD-lounge-dailycup_round_start_interval

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `B81646`）

```asm
00B81631  call    sub_B41120        ; lounge 守卫
00B81646  push    6                 ; 容量 = 0x6
00B81648  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B81681  call    sub_B02DF0        ; 1 node_id：u16
00B816C1  call    sub_B02DD0        ; 2 wait_sec：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B816D1  cmp     ebx, [esp+2C5Ch+var_2C40]
00B816D7  jz      short loc_B816F3
```

## E4 去向（用途锚点）

```asm
00B817F7  call    eax               ; vt[0x558]，2 实参
```

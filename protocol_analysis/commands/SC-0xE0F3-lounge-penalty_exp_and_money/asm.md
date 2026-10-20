# 汇编证据 —— SC-0xE0F3-lounge-penalty_exp_and_money

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B82E0B`）

```asm
00B82DF6  call    sub_B41120        ; lounge 守卫
00B82E0B  push    8                 ; 容量 = 0x8
00B82E0D  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B82E46  call    sub_B02DD0        ; 1 penalty_exp：u32
00B82E86  call    sub_B02DD0        ; 2 penalty_money：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B82E96  cmp     ebx, [esp+2C5Ch+var_2C40]
00B82E9C  jz      short loc_B82EB8
```

## E4 去向（用途锚点）

```asm
00B82FBA  call    eax               ; vt[0x530]，2 实参
```

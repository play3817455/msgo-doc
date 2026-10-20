# 汇编证据 —— SC-0xD691-battle-commander_subcmdr_candidacy_start

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `B2C5A2`）

```asm
00B2C58D  call    sub_B05DA0        ; battle 守卫
00B2C5A2  push    2                 ; 容量 = 0x2
00B2C5A4  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2C5DD  call    sub_B02DF0        ; 字段 1 remain_sec：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2C609  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2C60B  jnz     short loc_B2C5EB
```

## E4 去向（用途锚点）

```asm
00B2C6E2  call    eax               ; vt[0x2E0]，1 实参
```

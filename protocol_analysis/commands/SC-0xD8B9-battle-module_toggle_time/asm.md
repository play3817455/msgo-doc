# 汇编证据 —— SC-0xD8B9-battle-module_toggle_time

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B2BEB6`）

```asm
00B2BEA1  call    sub_B05DA0        ; battle 守卫
00B2BEB6  push    8                 ; 容量 = 0x8
00B2BEB8  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2BEF1  call    sub_B02DF0        ; 1 ent_id：u16
00B2BF31  call    sub_B02DD0        ; 2 msec：u32
00B2BF55  call    sub_B02DF0        ; 3 rate：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2BF65  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2BF6B  jz      short loc_B2BF87
```

## E4 去向（用途锚点）

```asm
00B2C0BE  call    eax               ; vt[0x37C]，3 实参
```

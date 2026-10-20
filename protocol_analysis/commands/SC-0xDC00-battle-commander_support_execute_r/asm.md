# 汇编证据 —— SC-0xDC00-battle-commander_support_execute_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B2CA9E`）

```asm
00B2CA89  call    sub_B05DA0        ; battle 守卫
00B2CA9E  push    4                 ; 容量 = 0x4
00B2CAA0  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2CAD9  call    sub_B02DD0        ; 字段 1 result：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2CB05  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2CB0B  jnz     short loc_B2CAE7
```

## E4 去向（用途锚点）

```asm
00B2CBDC  call    eax               ; vt[0x2B8]，1 实参
```

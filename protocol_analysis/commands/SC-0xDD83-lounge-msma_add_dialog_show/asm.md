# 汇编证据 —— SC-0xDD83-lounge-msma_add_dialog_show

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `B8145D`）

```asm
00B81448  call    sub_B41120        ; lounge 守卫
00B8145D  push    6                 ; 容量 = 0x6
00B8145F  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B81498  call    sub_B02DD0        ; 1 msma_id：u32
00B814D8  call    sub_B02DF0        ; 2 stack：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B814E8  cmp     ebx, [esp+2C5Ch+var_2C40]
00B814EE  jz      short loc_B8150A
```

## E4 去向（用途锚点）

```asm
00B8160E  call    eax               ; vt[0x23C]，2 实参
```

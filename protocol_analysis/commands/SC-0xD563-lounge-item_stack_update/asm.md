# 汇编证据 —— SC-0xD563-lounge-item_stack_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA` @ `B7D81B`）

```asm
00B7D806  call    sub_B41120        ; lounge 守卫
00B7D81B  push    0Ah               ; 容量 = 0xA
00B7D81D  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7D856  call    sub_B06200        ; 字段 1 uniqid：u64
00B7D896  call    sub_B02DF0        ; 字段 2 stack：u16
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7D8A6  cmp     ecx, [esp+2C5Ch+var_2C40]
00B7D8C8  jz      short loc_B7D8C8
```

## E4 去向（用途锚点）

```asm
00B7D9D0  call    edx               ; vt[0x33C]，3 实参
```

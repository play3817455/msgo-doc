# 汇编证据 —— SC-0xDEE3-lounge-block_list_remove_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B81F51`）

```asm
00B81F3C  call    sub_B41120        ; lounge 守卫
00B81F51  push    8                 ; 容量 = 0x8
00B81F53  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B81F8C  call    sub_B02DD0        ; 1 result：u32
00B81FCC  call    sub_B02DD0        ; 2 send_sysmes：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B81FDC  cmp     ebx, [esp+2C5Ch+var_2C40]
00B81FE2  jz      short loc_B81FFE
```

## E4 去向（用途锚点）

```asm
00B82100  call    edx               ; vt[0x380]，2 实参
```

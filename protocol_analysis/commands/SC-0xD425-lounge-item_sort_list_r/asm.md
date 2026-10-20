# 汇编证据 —— SC-0xD425-lounge-item_sort_list_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA` @ `B7C866`）

```asm
00B7C851  call    sub_B41120        ; lounge 守卫
00B7C866  push    0Ah               ; 容量 = 0xA
00B7C868  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7C8A1  call    sub_B02DF0        ; 字段 1 inv_place：u16（游标 +2）
00B7C8E1  call    sub_B02DD0        ; 字段 2 sort_tm_sec：u32（游标 +4）
00B7C905  call    sub_B02DD0        ; 字段 3 sort_tm_usec：u32（游标 +4）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7C915  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7C917  jz      short loc_B7C937
```

## E4 去向（用途锚点）

```asm
00B7CA6C  call    eax               ; vt[0x340]，3 实参
```

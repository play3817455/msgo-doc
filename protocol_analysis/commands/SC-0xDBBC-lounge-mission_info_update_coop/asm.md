# 汇编证据 —— SC-0xDBBC-lounge-mission_info_update_coop

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x61` @ `B80735`）

```asm
00B8071E  call    sub_B41120        ; lounge 守卫
00B80733  push    61h ; char        ; 容量 = 0x61
00B80735  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B8075F  call    sub_B41300        ; 一次推进 0x20 整块预留（非字段）
00B80776  call    sub_B06200        ; 1 is_unlock 元素：u64
00B80788  cmp     edi, 4            ; 固定 4 元（无线上 count）
00B807A5  call    sub_B41300        ; 预留（非字段）
00B807B6  call    sub_B06200        ; 2 is_known 元素：u64
00B807E5  call    sub_B41300        ; 预留（非字段）
00B807F6  call    sub_B06200        ; 3 is_clear 元素：u64
00B80834  call    sub_B06230        ; 4 coop_entry_is_freeze：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B8085D  cmp     eax, [esp+2C5Ch+var_2C40]
00B80863  jz      short loc_B8087A
```

## E4 去向（用途锚点）

```asm
00B80AA4  call    eax               ; vt[0x140]，4 实参
```

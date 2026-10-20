# 汇编证据 —— SC-0xDBDB-lounge-btlroom_coop_roomlist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA8C4` @ `B804E5`）

```asm
00B804D0  call    sub_B41120        ; lounge 守卫
00B804E5  push    0A8C4h            ; 容量 = 0xA8C4
00B804EA  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B80515  call    sub_B02DD0        ; 1 roomlist_num：u32
00B80541  cmp     ebx, 12Ch         ; 上限 300
00B80547  ja      short loc_B80521  ; 越界 → 错误出口
00B80553  call    sub_B41650        ; 按 count 预留 144B/槽（非字段）
00B8057A  call    sub_B44880        ; 2 roomlist 元素（135B/元素）
00B80586  add     [esp+2C5Ch+var_2C3C], 90h   ; 元素步进 144
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B805AB  cmp     ecx, [esp+2C5Ch+var_2C40]
00B805B1  jz      short loc_B805CD
```

## E4 去向（用途锚点）

```asm
00B806FE  call    eax               ; vt[0x1C8]，2 实参（数组指针 + 计数）
```

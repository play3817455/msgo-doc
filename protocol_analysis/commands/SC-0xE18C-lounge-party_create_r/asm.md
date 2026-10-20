# 汇编证据 —— SC-0xE18C-lounge-party_create_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x46` @ `B83589`）

```asm
00B83577  call    sub_B41120        ; lounge 守卫
00B8358C  push    46h ; char        ; 容量 = 0x46
00B8358E  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B835C7  call    sub_B02DD0        ; 1 result：u32
00B83607  call    sub_B06230        ; 2 is_recruiting：u8
00B83619  push    3Dh               ; 串槽预算 61
00B8362C  call    sub_B02BA0        ; 3 comment：NUL 串
00B8366C  call    sub_B02DD0        ; 4 party_type：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B8367C  cmp     ebx, [esp+2C5Ch+var_2C40]
00B83682  jz      short loc_B8369E
```

## E4 去向（用途锚点）

```asm
00B8380F  call    eax               ; vt[0x1F8]，4 实参
```

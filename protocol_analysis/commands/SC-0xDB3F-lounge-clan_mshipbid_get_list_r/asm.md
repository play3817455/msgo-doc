# 汇编证据 —— SC-0xDB3F-lounge-clan_mshipbid_get_list_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA59` @ `B8019A`）

```asm
00B80185  call    sub_B41120        ; lounge 守卫
00B8019A  push    0A59h             ; 容量 = 0xA59
00B8019F  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B801D8  call    sub_B02DD0        ; 1 result：u32
00B8020A  call    sub_B02DD0        ; 2 lpcard_num：u32
00B80236  cmp     ebx, 14h          ; 上限 20
00B80239  ja      short loc_B80216  ; 越界 → 错误出口
00B80245  call    sub_B415D0        ; 按 count 预留 132B/槽（非字段）
00B8026A  call    sub_B43100        ; 3 lpcard 元素（113B/元素）
00B80276  add     [esp+2C5Ch+var_2C3C], 84h   ; 元素步进 132
00B802AF  call    sub_B06230        ; 4 clan_kind：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B802C3  cmp     ecx, [esp+2C5Ch+var_2C40]
00B802C9  jz      short loc_B802E5
```

## E4 去向（用途锚点）

```asm
00B80477  call    edx               ; vt[0x434]，4 实参
```

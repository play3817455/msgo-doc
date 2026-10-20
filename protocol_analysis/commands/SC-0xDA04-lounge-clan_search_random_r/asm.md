# 汇编证据 —— SC-0xDA04-lounge-clan_search_random_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4B5` @ `B7FD78`）

```asm
00B7FD63  call    sub_B41120        ; lounge 守卫
00B7FD78  push    4B5h              ; 容量 = 0x4B5
00B7FD7D  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7FDA8  call    sub_B02DD0        ; 1 res_num：u32
00B7FDD4  cmp     ebx, 0Ah          ; 上限 10
00B7FDD7  ja      short loc_B7FDB4  ; 越界 → 错误出口
00B7FDE3  call    sub_B417A0        ; 按 count 预留 120B/槽（非字段）
00B7FE0A  call    sub_B45BA0        ; 2 search_res 元素（114B/元素）
00B7FE16  add     [esp+2C5Ch+var_2C3C], 78h   ; 元素步进 120
00B7FE4C  call    sub_B06230        ; 3 clan_kind：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7FE60  cmp     ecx, [esp+2C5Ch+var_2C40]
00B7FE66  jz      short loc_B7FE82
```

## E4 去向（用途锚点）

```asm
00B7FFDD  call    eax               ; vt[0x464]，3 实参
```

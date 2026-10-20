# 汇编证据 —— SC-0xD6E5-lounge-season_rankerbattle_team_info_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x320C` @ `B7E8B2`）

```asm
00B7E89D  call    sub_B41120        ; lounge 守卫
00B7E8B2  push    320Ch             ; 容量 = 0x320C
00B7E8B7  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7E8F0  call    sub_B02DD0        ; 1 result：u32
00B7E930  call    sub_B02DD0        ; 2 troops：u32
00B7E946  call    sub_B02DD0        ; 3 pilots_num：u32
00B7E972  cmp     ebx, 0C8h         ; 上限 200
00B7E978  ja      short loc_B7E952  ; 越界 → 错误出口
00B7E984  call    sub_B41AC0        ; 按 count 预留 64B/槽（非字段）
00B7E9AA  call    sub_B472C0        ; 4 pilots 元素（复合读取器，55B/元素）
00B7E9B6  add     [esp+2C5Ch+var_2C3C], 40h   ; 元素步进 64
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7E9D8  cmp     ecx, [esp+2C5Ch+var_2C40]
00B7E9DE  jz      short loc_B7E9FA
```

## E4 去向（用途锚点）

```asm
00B7EB8B  call    eax               ; vt[0x5D8]，4 实参
```

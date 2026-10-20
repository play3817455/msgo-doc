# 汇编证据 —— SC-0xD467-lounge-clan_search_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE19` @ `B7CC30`）

```asm
00B7CC1B  call    sub_B41120        ; lounge 守卫
00B7CC30  push    0E19h             ; 容量 = 0xE19
00B7CC35  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7CC6E  call    sub_B02DD0        ; 字段 1 result：u32
00B7CCA0  call    sub_B02DD0        ; 字段 2 res_num：u32
00B7CCCC  cmp     ebx, 1Eh          ; 上限 30
00B7CCCF  ja      short loc_B7CCAC  ; 越界 → 错误出口
00B7CCDB  call    sub_B417A0        ; 按 res_num 预留 120B/槽（非字段）
00B7CCFC  call    sub_B45BA0        ; 字段 3 search_res 元素（复合读取器，114B/元素）
00B7CD08  add     [esp+2C5Ch+var_2C48], 78h   ; 元素步进 120
00B7CD3E  call    sub_B06230        ; 字段 4 clan_kind：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7CD52  cmp     ecx, [esp+2C5Ch+var_2C40]
00B7CD58  jz      short loc_B7CD74
```

## E4 去向（用途锚点）

```asm
00B7CEFB  call    edx               ; vt[0x460]，4 实参
```

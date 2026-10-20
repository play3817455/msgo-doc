# 汇编证据 —— SC-0xD505-lounge-msma_equip_bonus_modules_lot_redraw_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `B7CF33`）

```asm
00B7CF1E  call    sub_B41120        ; lounge 守卫
00B7CF33  push    18h               ; 容量 = 0x18
00B7CF35  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7CF6E  call    sub_B02DD0        ; 字段 1 result：u32
00B7CFAE  call    sub_B06200        ; 字段 2 uniqid_ms：u64
00B7CFC3  call    sub_B41460        ; 一次推进 0xC（=3×4）整块预留（非字段）
00B7CFD6  call    sub_B02DD0        ; 字段 3 eq_bonus_modules_lot 元素：u32 ×3
00B7CFE8  cmp     edi, 3            ; 固定 3 元（无线上 count）
00B7CFEB  jb      short loc_B7CFD0
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7D003  cmp     eax, [esp+2C5Ch+var_2C40]
00B7D009  jz      short loc_B7D025
```

## E4 去向（用途锚点）

```asm
00B7D19B  call    edx               ; vt[0x274]，4 实参
```

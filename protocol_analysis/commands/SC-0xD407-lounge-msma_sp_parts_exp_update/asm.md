# 汇编证据 —— SC-0xD407-lounge-msma_sp_parts_exp_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B7C4E7`）

```asm
00B7C4D2  call    sub_B41120        ; lounge 守卫
00B7C4E7  push    0Ch               ; 容量 = 0xC
00B7C4E9  call    edx               ; vt[0x78]（解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
00B7C522  call    sub_B06200        ; 字段 1 uniqid_ms：u64（游标 +8）
00B7C562  call    sub_B02DD0        ; 字段 2 exp：u32（游标 +4）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7C572  cmp     eax, [esp+2C5Ch+var_2C40]
00B7C578  jz      short loc_B7C594
```

## E4 去向（用途锚点）

```asm
00B7C69A  call    edx               ; vt[0x2F0]，3 实参（uniqid_ms lo/hi + exp）
```

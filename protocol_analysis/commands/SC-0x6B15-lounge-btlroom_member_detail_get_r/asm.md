# 汇编证据 —— SC-0x6B15-lounge-btlroom_member_detail_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD58` @ `0xb6560f`）

```asm
; VA: 0xb6560f（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb6560f  push    0xD58          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb65648
; 字段 2 —— roominfo：偏移 4，长度 135，线类型 struct<roominfo>；读取点 VA 0xb65688
; 字段 3 —— members_count：偏移 139，长度 4，线类型 u32；读取点 VA 0xb6569e
; 字段 4 —— members：偏移 143，长度 ?，线类型 array<struct<member>,N>；读取点 VA 0xb656fa
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb65724
0xb65724  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb658cc（4 实参）
;       `vt[0x1CC]`
```

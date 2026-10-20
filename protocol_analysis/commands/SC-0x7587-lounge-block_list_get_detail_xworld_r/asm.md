# 汇编证据 —— SC-0x7587-lounge-block_list_get_detail_xworld_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x352C` @ `0xb67802`）

```asm
; VA: 0xb67802（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb67802  push    0x352C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb6783b
; 字段 2 —— block_details_count：偏移 4，长度 4，线类型 u32；读取点 VA 0xb6786d
; 字段 3 —— block_details：偏移 8，长度 ?，线类型 array<struct<block_detail>,N>；读取点 VA 0xb678ca
; 字段 4 —— block_widlist_count：偏移 -，长度 4，线类型 u32；读取点 VA 0xb67901
; 字段 5 —— block_widlist：偏移 -，长度 ?，线类型 array<u32,N>；读取点 VA 0xb6794a
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb67976
0xb67976  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb67b70（5 实参）
;       `vt[0x378]`
```

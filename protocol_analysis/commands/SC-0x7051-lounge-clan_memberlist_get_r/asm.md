# 汇编证据 —— SC-0x7051-lounge-clan_memberlist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19D1` @ `0xb65f05`）

```asm
; VA: 0xb65f05（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb65f05  push    0x19D1          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb65f43
; 字段 2 —— lpcard_count：偏移 4，长度 4，线类型 u32；读取点 VA 0xb65f75
; 字段 3 —— lpcard：偏移 8，长度 ?，线类型 array<struct<lpcard>,N>；读取点 VA 0xb65fcd
; 字段 4 —— clan_kind：偏移 -，长度 1，线类型 u8；读取点 VA 0xb66012
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb66026
0xb66026  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb661d7（4 实参）
;       `vt[0x418]`
```

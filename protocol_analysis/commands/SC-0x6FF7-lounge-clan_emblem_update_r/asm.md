# 汇编证据 —— SC-0x6FF7-lounge-clan_emblem_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `0xb65a7c`）

```asm
; VA: 0xb65a7c（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb65a7c  push    0x7          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb65ab5
; 字段 2 —— emb_base：偏移 4，长度 1，线类型 u8；读取点 VA 0xb65af5
; 字段 3 —— emb_parts1：偏移 5，长度 1，线类型 u8；读取点 VA 0xb65b19
; 字段 4 —— emb_parts2：偏移 6，长度 1，线类型 u8；读取点 VA 0xb65b3d
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb65b65
0xb65b65  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb65cda（4 实参）
;       `vt[0x440]`
```

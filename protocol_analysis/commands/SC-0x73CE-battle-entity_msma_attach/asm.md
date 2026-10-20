# 汇编证据 —— SC-0x73CE-battle-entity_msma_attach

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `0xb1f6ba`）

```asm
; VA: 0xb1f6ba（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1f6ba  push    0xB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16；读取点 VA 0xb1f6f5
; 字段 2 —— attach_parent_ent_id：偏移 2，长度 2，线类型 u16；读取点 VA 0xb1f732
; 字段 3 —— attach_socket：偏移 4，长度 1，线类型 u8；读取点 VA 0xb1f756
; 字段 4 —— attach_pos_x：偏移 5，长度 2，线类型 u16；读取点 VA 0xb1f77a
; 字段 5 —— attach_pos_y：偏移 7，长度 2，线类型 u16；读取点 VA 0xb1f7a2
; 字段 6 —— attach_pos_z：偏移 9，长度 2，线类型 u16；读取点 VA 0xb1f7ca
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1f7de
0xb1f7de  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1f9cb（6 实参）
;       `vt[0x168]`
```

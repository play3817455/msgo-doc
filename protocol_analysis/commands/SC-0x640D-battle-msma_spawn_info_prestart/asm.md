# 汇编证据 —— SC-0x640D-battle-msma_spawn_info_prestart

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x179` @ `0xb1b873`）

```asm
; VA: 0xb1b873（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1b873  push    0x179          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— remain_sec：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1b8ac
; 字段 2 —— mstype_count：偏移 4，长度 4，线类型 u32；读取点 VA 0xb1b8db
; 字段 3 —— mstype：偏移 8，长度 ?，线类型 array<u8,N>；读取点 VA 0xb1b930
; 字段 4 —— post_index_count：偏移 -，长度 4，线类型 u32；读取点 VA 0xb1b95c
; 字段 5 —— post_index：偏移 -，长度 ?，线类型 array<u16,N>；读取点 VA 0xb1b9aa
; 字段 6 —— spt_spot_index_count：偏移 -，长度 4，线类型 u32；读取点 VA 0xb1b9db
; 字段 7 —— spt_spot_index：偏移 -，长度 ?，线类型 array<u16,N>；读取点 VA 0xb1ba2a
; 字段 8 —— stghold_entid_count：偏移 -，长度 4，线类型 u32；读取点 VA 0xb1ba5b
; 字段 9 —— stghold_entid：偏移 -，长度 ?，线类型 array<u16,N>；读取点 VA 0xb1baa2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1bac9
0xb1bac9  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1bdd0（8 实参）
;       `vt[0x140]`
```

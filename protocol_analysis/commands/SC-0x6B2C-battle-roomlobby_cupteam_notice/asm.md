# 汇编证据 —— SC-0x6B2C-battle-roomlobby_cupteam_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD` @ `0xb1d418`）

```asm
; VA: 0xb1d418（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1d418  push    0xD          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1d451
; 字段 2 —— cupteam_id：偏移 1，长度 4，线类型 u32；读取点 VA 0xb1d48e
; 字段 3 —— cupteam_rate：偏移 5，长度 4，线类型 u32；读取点 VA 0xb1d4b2
; 字段 4 —— tournament_vs_type：偏移 9，长度 4，线类型 u32；读取点 VA 0xb1d4d6
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1d4e6
0xb1d4e6  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1d66b（4 实参）
;       `vt[0xA0]`
```

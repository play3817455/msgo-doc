# 汇编证据 —— SC-0x6B71-battle-roomlobby_vote_state

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xb1d23d`）

```asm
; VA: 0xb1d23d（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1d23d  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— state：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1d276
; 字段 2 —— sec：偏移 4，长度 4，线类型 u32；读取点 VA 0xb1d2b3
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1d2bf
0xb1d2bf  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1d3e1（2 实参）
;       `vt[0xCC]`
```

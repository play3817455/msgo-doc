# 汇编证据 —— SC-0x6A8D-battle-roomlobby_xwar_countdown

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xb1d0bc`）

```asm
; VA: 0xb1d0bc（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1d0bc  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— sec：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1d0f5
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1d11a
0xb1d11a  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1d1f2（1 实参）
;       `vt[0x94]`
```

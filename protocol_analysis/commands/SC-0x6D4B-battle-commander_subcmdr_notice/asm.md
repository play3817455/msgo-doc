# 汇编证据 —— SC-0x6D4B-battle-commander_subcmdr_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A0` @ `0xb1df3f`）

```asm
; VA: 0xb1df3f（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1df3f  push    0x1A0          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— worldids_count：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1df6a
; 字段 2 —— worldids：偏移 4，长度 ?，线类型 array<u32,N>；读取点 VA 0xb1dfca
; 字段 3 —— pilotids_count：偏移 -，长度 4，线类型 u32；读取点 VA 0xb1dffe
; 字段 4 —— pilotids：偏移 -，长度 ?，线类型 array<u32,N>；读取点 VA 0xb1e05a
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1e084
0xb1e084  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1e24c（4 实参）
;       `vt[0x2E8]`
```

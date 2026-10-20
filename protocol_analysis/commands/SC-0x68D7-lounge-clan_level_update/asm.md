# 汇编证据 —— SC-0x68D7-lounge-clan_level_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xb65289`）

```asm
; VA: 0xb65289（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb65289  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— lv：偏移 0，长度 1，线类型 u8；读取点 VA 0xb652c2
; 字段 2 —— deckcost：偏移 1，长度 4，线类型 u32；读取点 VA 0xb65302
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb6530e
0xb6530e  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb65437（2 实参）
;       `vt[0x45C]`
```

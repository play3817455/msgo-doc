# 汇编证据 —— SC-0x645D-battle-module_val_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xb1c7b0`）

```asm
; VA: 0xb1c7b0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1c7b0  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16；读取点 VA 0xb1c7e9
; 字段 2 —— val：偏移 2，长度 2，线类型 u16；读取点 VA 0xb1c829
; 字段 3 —— val2：偏移 4，长度 2，线类型 u16；读取点 VA 0xb1c84d
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1c859
0xb1c859  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1c9b8（3 实参）
;       `vt[0x374]`
```

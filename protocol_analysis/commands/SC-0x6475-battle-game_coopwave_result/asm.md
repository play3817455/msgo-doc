# 汇编证据 —— SC-0x6475-battle-game_coopwave_result

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2C` @ `0xb1c642`）

```asm
; VA: 0xb1c642（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1c642  push    0x2C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— wave_res：偏移 0，长度 34，线类型 struct<wave_res>；读取点 VA 0xb1c67b
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1c6a0
0xb1c6a0  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1c776（1 实参）
;       `vt[0xF8]`
```

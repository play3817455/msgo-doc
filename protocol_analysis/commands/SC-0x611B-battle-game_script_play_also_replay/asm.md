# 汇编证据 —— SC-0x611B-battle-game_script_play_also_replay

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x42` @ `0xb1c261`）

```asm
; VA: 0xb1c261（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1c261  push    0x42          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— src：偏移 0，长度 ?，线类型 bytes；读取点 VA 0xb1c295
; 字段 2 —— script_thread：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1c2d2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1c2de
0xb1c2de  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1c40d（2 实参）
;       `vt[0x110]`
```

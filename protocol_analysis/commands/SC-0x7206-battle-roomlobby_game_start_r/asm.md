# 汇编证据 —— SC-0x7206-battle-roomlobby_game_start_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xb1e80c`）

```asm
; VA: 0xb1e80c（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1e80c  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1e847
; 字段 2 —— elapsed_sec：偏移 4，长度 4，线类型 u32；读取点 VA 0xb1e884
; 字段 3 —— limit_sec：偏移 8，长度 4，线类型 u32；读取点 VA 0xb1e8a8
; 字段 4 —— kill_count：偏移 12，长度 4，线类型 u32；读取点 VA 0xb1e8cc
; 字段 5 —— death_count：偏移 16，长度 4，线类型 u32；读取点 VA 0xb1e8f4
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1e908
0xb1e908  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1eab9（5 实参）
;       `vt[0xA8]`
```

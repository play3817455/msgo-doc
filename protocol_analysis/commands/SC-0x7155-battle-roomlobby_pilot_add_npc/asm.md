# 汇编证据 —— SC-0x7155-battle-roomlobby_pilot_add_npc

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5B` @ `0xb1e283`）

```asm
; VA: 0xb1e283（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1e283  push    0x5B          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8；读取点 VA 0xb1e2bc
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8；读取点 VA 0xb1e2f9
; 字段 3 —— pilot_id：偏移 2，长度 4，线类型 u32；读取点 VA 0xb1e31d
; 字段 4 —— level：偏移 6，长度 2，线类型 u16；读取点 VA 0xb1e341
; 字段 5 —— cutin_id：偏移 8，长度 4，线类型 u32；读取点 VA 0xb1e369
; 字段 6 —— name：偏移 12，长度 ?，线类型 bytes；读取点 VA 0xb1e392
; 字段 7 —— gender：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e3cf
; 字段 8 —— platoon：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e3f3
; 字段 9 —— platoon_slot：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e417
; 字段 10 —— is_platoon_leader：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e43f
; 字段 11 —— dtaskf_order_number：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e467
; 字段 12 —— is_disable_scoreboard：偏移 -，长度 1，线类型 u8；读取点 VA 0xb1e48f
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1e49f
0xb1e49f  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1e7c1（12 实参）
;       `vt[0x78](客户端对象)`
```

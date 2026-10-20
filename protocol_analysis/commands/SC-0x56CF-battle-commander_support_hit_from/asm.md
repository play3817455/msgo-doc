# 汇编证据 —— SC-0x56CF-battle-commander_support_hit_from

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB184F0`）

```asm
; VA: 0xB184F0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB184F0  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— support_type：偏移 0，长度 4，线类型 u32（支援类型）
0xB1852B  call    sub_B02DD0     ; u32
; 块内日志格式串 "support_type=" → 含义锚点：0xB186B6

; 字段 2 —— ent_id：偏移 4，长度 2，线类型 u16（实体 ID）
0xB1856B  call    sub_B02DF0     ; u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB186E1

; 字段 3 —— hp_now：偏移 6，长度 4，线类型 u32（当前 HP）
0xB1858F  call    sub_B02DD0     ; u32
; 块内日志格式串 "hp_now=" → 含义锚点：0xB1870B

; 字段 4 —— hp_max：偏移 10，长度 4，线类型 u32（最大 HP）
0xB185B3  call    sub_B02DD0     ; u32
; 块内日志格式串 "hp_max=" → 含义锚点：0xB18735

; 字段 5 —— spbits：偏移 14，长度 4，线类型 u32（状态位（special bits））
0xB185DB  call    sub_B02DD0     ; u32
; 块内日志格式串 "spbits=" → 含义锚点：0xB1875F

; 字段 6 —— hit_dir：偏移 18，长度 2，线类型 u16（受击方向）
0xB18603  call    sub_B02DF0     ; u16
; 块内日志格式串 "hit_dir=" → 含义锚点：0xB18785

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB18617
0xB18617  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB18617  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB18803
0xB18803  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2D0h]
;       call    <reg>          ; vt[0x2D0]（6 实参）
```

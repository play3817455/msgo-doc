# 汇编证据 —— SC-0x5F32-battle-bullet_supply_per_weapon_slot

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB1915C`）

```asm
; VA: 0xB1915C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1915C  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— supplyer_end_id：偏移 0，长度 2，线类型 u16（补给方实体 ID）
0xB19197  call    sub_B02DF0     ; u16
; 块内日志格式串 "supplyer_end_id=" → 含义锚点：0xB192EF

; 字段 2 —— supply_amount_per_weapon_slot_count：偏移 2，长度 4，线类型 u32（武器槽补给量条数（上限 3，`cmp ebx,3`@`0xB191F5`））
0xB191C9  call    sub_B02DD0     ; u32
; 块内日志格式串 "supply_amount_per_weapon_slot_count=" → 含义锚点：0xB1930A

; 字段 3 —— supply_amount_per_weapon_slot[]：偏移 6，长度 2N，线类型 array<u16>（各武器槽补给量（元素 2B / 槽步进 2B，预留 `sub_B05E40`））
0xB19204  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "supply_amount_per_weapon_slot[]=" → 含义锚点：0xB1930A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1924F
0xB1924F  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB1924F  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB193CE
0xB193CE  mov     <reg>, [obj]; mov <reg>, [<reg>+0x27Ch]
;       call    <reg>          ; vt[0x27C]（3 实参）
```

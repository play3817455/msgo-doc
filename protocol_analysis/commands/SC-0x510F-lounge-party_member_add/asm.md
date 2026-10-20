# 汇编证据 —— SC-0x510F-lounge-party_member_add

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xBB` @ `0xB6010E`）

```asm
; VA: 0xB6010E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB6010E  push    0xBB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot：偏移 0，长度 159，线类型 struct<pilot>（成员飞行员信息（claim 176 = 预留 `sub_B05F00` 槽步进 `0xB0`；线长 159，读取器 `sub_B06980`））
0xB6013D  call    复合读取器（元素/结构体，见 notes.md）     ; struct<pilot>
; 块内日志格式串 "pilot=" → 含义锚点：0xB602D5

; 字段 2 —— stat：偏移 159，长度 1，线类型 u8（状态）
0xB6018C  call    sub_B06230     ; u8
; 块内日志格式串 "stat=" → 含义锚点：0xB602FF

; 字段 3 —— mission_id：偏移 160，长度 4，线类型 u32（任务 ID）
0xB601B0  call    sub_B02DD0     ; u32
; 块内日志格式串 "mission_id=" → 含义锚点：0xB6032B

; 字段 4 —— is_party_leader：偏移 164，长度 1，线类型 u8（是否队长）
0xB601D4  call    sub_B06230     ; u8
; 块内日志格式串 "is_party_leader=" → 含义锚点：0xB60353

; 字段 5 —— comeback_limittime：偏移 165，长度 4，线类型 u32（回归时限）
0xB601FC  call    sub_B02DD0     ; u32
; 块内日志格式串 "comeback_limittime=" → 含义锚点：0xB6037F

; 字段 6 —— is_booking：偏移 169，长度 1，线类型 u8（是否预约）
0xB60224  call    sub_B06230     ; u8
; 块内日志格式串 "is_booking=" → 含义锚点：0xB603A2

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB60238
0xB60238  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB60238  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB60421
0xB60421  mov     <reg>, [obj]; mov <reg>, [<reg>+0x20Ch]
;       call    <reg>          ; vt[0x20C]（6 实参）
```

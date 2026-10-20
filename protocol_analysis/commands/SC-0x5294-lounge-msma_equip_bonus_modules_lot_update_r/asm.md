# 汇编证据 —— SC-0x5294-lounge-msma_equip_bonus_modules_lot_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB609DD`）

```asm
; VA: 0xB609DD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB609DD  push    0x10          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB60A18  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB60B4A

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB60A58  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB60B78

; 字段 3 —— eq_bonus_modules：偏移 12，长度 4，线类型 u32[1]（装备追加模块（**无线上计数**的定长数组，循环上界字面量 1：`cmp edi,1`@`0xB60A90`））
0xB60A7E  call    sub_B02DD0     ; u32[1]
; 块内日志格式串 "eq_bonus_modules=" → 含义锚点：0xB60B93

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB60AAB
0xB60AAB  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB60AAB  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB60C11
0xB60C11  mov     <reg>, [obj]; mov <reg>, [<reg>+0x278h]
;       call    <reg>          ; vt[0x278]（4 实参）
```

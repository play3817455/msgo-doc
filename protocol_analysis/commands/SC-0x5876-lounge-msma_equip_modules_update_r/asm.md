# 汇编证据 —— SC-0x5876-lounge-msma_equip_modules_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x38` @ `0xB629DA`）

```asm
; VA: 0xB629DA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB629DA  push    0x38          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB62A15  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB62B85

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB62A55  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB62BB3

; 字段 3 —— eq_modules：偏移 12，长度 40，线类型 u32[10]（装备模块（**无线上计数**的定长数组 10×u32；预留 `sub_B418C0` 槽步进 `0x28`=40，循环上界字面量 `cmp edi,0Ah`@`0xB62A8D`））
0xB62A6A  call    sub_B02DD0     ; u32[10]
; 块内日志格式串 "eq_modules=" → 含义锚点：0xB62BCE

; 字段 4 —— cost：偏移 52，长度 4，线类型 u32（消耗）
0xB62ABC  call    sub_B02DD0     ; u32
; 块内日志格式串 "cost=" → 含义锚点：0xB62C38

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB62AE8
0xB62AE8  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB62AE8  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB62CAC
0xB62CAC  mov     <reg>, [obj]; mov <reg>, [<reg>+0x264h]
;       call    <reg>          ; vt[0x264]（5 实参）
```

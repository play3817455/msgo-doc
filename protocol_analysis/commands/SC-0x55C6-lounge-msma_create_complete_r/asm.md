# 汇编证据 —— SC-0x55C6-lounge-msma_create_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB620BF`）

```asm
; VA: 0xB620BF（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB620BF  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB620FA  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB6224D

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB6213A  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB62277

; 字段 3 —— workres：偏移 12，长度 4，线类型 u32（制作结果值）
0xB6217A  call    sub_B02DD0     ; u32
; 块内日志格式串 "workres=" → 含义锚点：0xB622A1

; 字段 4 —— mech_npcpict：偏移 16，长度 4，线类型 u32（机体 NPC 头像 ID）
0xB6219E  call    sub_B02DD0     ; u32
; 块内日志格式串 "mech_npcpict=" → 含义锚点：0xB622C6

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB621AE
0xB621AE  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB621AE  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB62338
0xB62338  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2ACh]
;       call    <reg>          ; vt[0x2AC]（5 实参）
```

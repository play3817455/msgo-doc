# 汇编证据 —— SC-0x5A2C-lounge-deckcost_extend_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB62ECA`）

```asm
; VA: 0xB62ECA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB62ECA  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB62F05  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB63018

; 字段 2 —— deckcost：偏移 4，长度 2，线类型 u16（编成费用）
0xB62F45  call    sub_B02DF0     ; u16
; 块内日志格式串 "deckcost=" → 含义锚点：0xB63043

; 字段 3 —— remain：偏移 6，长度 2，线类型 u16（剩余次数）
0xB62F69  call    sub_B02DF0     ; u16
; 块内日志格式串 "remain=" → 含义锚点：0xB63069

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB62F79
0xB62F79  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB62F79  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB630D2
0xB630D2  mov     <reg>, [obj]; mov <reg>, [<reg>+0x4C0h]
;       call    <reg>          ; vt[0x4C0]（3 实参）
```

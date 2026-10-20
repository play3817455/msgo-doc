# 汇编证据 —— SC-0x5885-lounge-party_member_kick_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB627F3`）

```asm
; VA: 0xB627F3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB627F3  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB6282E  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB6291D

; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（被踢飞行员 ID）
0xB6286E  call    sub_B02DD0     ; u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB62942

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB6287E
0xB6287E  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB6287E  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB629A2
0xB629A2  mov     <reg>, [obj]; mov <reg>, [<reg>+0x214h]
;       call    <reg>          ; vt[0x214]（2 实参）
```

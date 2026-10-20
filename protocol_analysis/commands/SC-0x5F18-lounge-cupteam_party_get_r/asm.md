# 汇编证据 —— SC-0x5F18-lounge-cupteam_party_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB642DA`）

```asm
; VA: 0xB642DA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB642DA  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB64315  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB64428

; 字段 2 —— channel_id：偏移 4，长度 4，线类型 u32（频道 ID）
0xB64355  call    sub_B02DD0     ; u32
; 块内日志格式串 "channel_id=" → 含义锚点：0xB64452

; 字段 3 —— party_id：偏移 8，长度 4，线类型 u32（队伍 ID）
0xB64379  call    sub_B02DD0     ; u32
; 块内日志格式串 "party_id=" → 含义锚点：0xB64477

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB64389
0xB64389  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB64389  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB644DE
0xB644DE  mov     <reg>, [obj]; mov <reg>, [<reg>+0x4F4h]
;       call    <reg>          ; vt[0x4F4]（3 实参）
```

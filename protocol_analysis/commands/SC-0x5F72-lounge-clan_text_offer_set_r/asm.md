# 汇编证据 —— SC-0x5F72-lounge-clan_text_offer_set_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x59` @ `0xB63FD9`）

```asm
; VA: 0xB63FD9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB63FD9  push    0x59          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB64014  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB64171

; 字段 2 —— is_active：偏移 4，长度 4，线类型 u32（是否启用（线宽 **u32**））
0xB64054  call    sub_B02DD0     ; u32
; 块内日志格式串 "is_active=" → 含义锚点：0xB6419B

; 字段 3 —— subj：偏移 8，长度 49，线类型 str（公告主题（槽位预算 `0x31`=49））
0xB64075  call    sub_B02BA0     ; str
; 块内日志格式串 "subj=" → 含义锚点：0xB641C8

; 字段 4 —— body：偏移 57，长度 31，线类型 str（公告正文（槽位预算 `0x1F`=31））
0xB64096  call    sub_B02BA0     ; str
; 块内日志格式串 "body=" → 含义锚点：0xB64200

; 字段 5 —— clan_kind：偏移 88，长度 1，线类型 u8（战队种类）
0xB640BE  call    sub_B06230     ; u8
; 块内日志格式串 "clan_kind=" → 含义锚点：0xB6422E

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB640D2
0xB640D2  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB640D2  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB642A2
0xB642A2  mov     <reg>, [obj]; mov <reg>, [<reg>+0x450h]
;       call    <reg>          ; vt[0x450]（5 实参）
```

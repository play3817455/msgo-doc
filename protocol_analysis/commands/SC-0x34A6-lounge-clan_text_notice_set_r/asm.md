# 汇编证据 —— SC-0x34A6-lounge-clan_text_notice_set_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1B6` @ `0xB5B6A6`）

```asm
; VA: 0xB5B6A6（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5B6A6  push    0x1B6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5B6E4  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5B819

; 字段 2 —— body：偏移 4，长度 433，线类型 str（战队公告正文（槽位预算 `0x1B1`=433））
0xB5B72A  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "body=" → 含义锚点：0xB5B846

; 字段 3 —— clan_kind：偏移 437，长度 1，线类型 u8（战队种类）
0xB5B76A  call    sub_B06230     ; 读 u8
; 块内日志格式串 "clan_kind=" → 含义锚点：0xB5B874

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5B7A1
0xB5B7A1  push    <模块/错误码>
0xB5B7A1  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5B8DC
0xB5B8DC  mov     edx, [obj]
;       mov     edx, [edx+0x44Ch]
;       call    edx          ; vt[0x44C]（3 实参）
```

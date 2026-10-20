# 汇编证据 —— SC-0x3671-lounge-mail_get_present_body_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x316` @ `0xB5C0D9`）

```asm
; VA: 0xB5C0D9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5C0D9  push    0x316          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5C117  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5C2B1

; 字段 2 —— mailid：偏移 4，长度 8，线类型 u64（邮件 ID（u64，作 2 个 32 位实参传递））
0xB5C157  call    sub_B06200     ; 读 u64
; 块内日志格式串 "mailid=" → 含义锚点：0xB5C2DB

; 字段 3 —— attach_type：偏移 12，长度 4，线类型 u32（附件类型）
0xB5C197  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "attach_type=" → 含义锚点：0xB5C305

; 字段 4 —— attach_id：偏移 16，长度 4，线类型 u32（附件 ID）
0xB5C1BB  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "attach_id=" → 含义锚点：0xB5C32F

; 字段 5 —— amount：偏移 20，长度 4，线类型 u32（数量）
0xB5C1DF  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "amount=" → 含义锚点：0xB5C359

; 字段 6 —— body：偏移 24，长度 766，线类型 str（邮件正文（槽位预算 `0x2FE`=766））
0xB5C1FE  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "body=" → 含义锚点：0xB5C381

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5C239
0xB5C239  push    <模块/错误码>
0xB5C239  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5C40A
0xB5C40A  mov     edx, [obj]
;       mov     edx, [edx+0x394h]
;       call    edx          ; vt[0x394]（7 实参）
```

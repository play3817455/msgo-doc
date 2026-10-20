# 汇编证据 —— SC-0x8C6E-lounge-mail_get_body_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x312` @ `B6B5B7`）

```asm
; VA: B6B5B7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6B5B7  push    0x312          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6B5F5  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6B767 → 含义锚点

; 字段 2 —— from_pilotid：偏移 4，长度 4，线类型 u32（发件飞行员 ID（日志串 `from_pilotid=`））
B6B635  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6B791 → 含义锚点

; 字段 3 —— from_clan_id：偏移 8，长度 4，线类型 u32（发件战队 ID（日志串 `from_clan_id=`））
B6B659  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6B7BB → 含义锚点

; 字段 4 —— mailid：偏移 12，长度 8，线类型 u64（邮件 ID（日志串 `mailid=`））
B6B67D  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B6B7E5 → 含义锚点

; 字段 5 —— body：偏移 20，长度 766，线类型 str（邮件正文（日志串 `body="`））
B6B6B4  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B6B80D → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6B6C8
B6B6C8  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6B886 —— `vt[0x390]`（6 实参）
B6B886  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x390h]
;       call    <reg>
```

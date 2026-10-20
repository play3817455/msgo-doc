# 汇编证据 —— SC-0x5281-lounge-mail_get_box_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A9C` @ `0xB60C49`）

```asm
; VA: 0xB60C49（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB60C49  push    0x1A9C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB60C87  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB60E0A

; 字段 2 —— box_type：偏移 4，长度 4，线类型 u32（邮件箱类型）
0xB60CC7  call    sub_B02DD0     ; u32
; 块内日志格式串 "box_type=" → 含义锚点：0xB60E34

; 字段 3 —— mail_count：偏移 8，长度 4，线类型 u32（邮件条数（上限 `0x32`=50，`cmp ebx,32h`@`0xB60D09`））
0xB60CDD  call    sub_B02DD0     ; u32
; 块内日志格式串 "mail_count=" → 含义锚点：0xB60E4F

; 字段 4 —— mails[]：偏移 12，长度 130，线类型 array<mail>（邮件数组（元素线长 130 / 槽步进 `0x88`=136，预留 `sub_B41610`））
0xB60D18  call    复合读取器（元素/结构体，见 notes.md）     ; array<mail>
; 块内日志格式串 "mails[]=" → 含义锚点：0xB60E4F

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB60D6B
0xB60D6B  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB60D6B  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB60F1E
0xB60F1E  mov     <reg>, [obj]; mov <reg>, [<reg>+0x38Ch]
;       call    <reg>          ; vt[0x38C]（4 实参）
```

# 汇编证据 —— SC-0x4DE7-lounge-clan_msgboard_msglist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xDAD9` @ `0xB5EF5F`）

```asm
; VA: 0xB5EF5F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5EF5F  push    0xDAD9          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5EF9D  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5F2BD

; 字段 2 —— sv_time：偏移 4，长度 4，线类型 u32（服务器时间）
0xB5EFDD  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "sv_time=" → 含义锚点：0xB5F2E7

; 字段 3 —— comment_social_count：偏移 8，长度 4，线类型 u32（社交评论数（上限 50，`cmp ebx,32h`@`0xB5F01F`））
0xB5EFF3  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "comment_social_count=" → 含义锚点：0xB5F302

; 字段 4 —— comment_social[]：偏移 12，长度 267，线类型 array<comment>（社交评论数组（元素线长 267 / 槽步进 `0x118`=280，`sub_B41810`））
0xB5F04B  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<comment>
; 块内日志格式串 "comment_social[]=" → 含义锚点：0xB5F302

; 字段 5 —— comment_event_count：偏移 14012，长度 4，线类型 u32（活动评论数（上限 50））
0xB5F082  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "comment_event_count=" → 含义锚点：0xB5F37E

; 字段 6 —— comment_event[]：偏移 14016，长度 267，线类型 array<comment>（活动评论数组）
0xB5F0CC  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<comment>
; 块内日志格式串 "comment_event[]=" → 含义锚点：0xB5F37E

; 字段 7 —— comment_question_count：偏移 28016，长度 4，线类型 u32（提问评论数（上限 50））
0xB5F103  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "comment_question_count=" → 含义锚点：0xB5F400

; 字段 8 —— comment_question[]：偏移 28020，长度 267，线类型 array<comment>（提问评论数组）
0xB5F14A  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<comment>
; 块内日志格式串 "comment_question[]=" → 含义锚点：0xB5F400

; 字段 9 —— comment_system_count：偏移 42020，长度 4，线类型 u32（系统评论数（上限 50））
0xB5F181  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "comment_system_count=" → 含义锚点：0xB5F47E

; 字段 10 —— comment_system[]：偏移 42024，长度 267，线类型 array<comment>（系统评论数组）
0xB5F1C8  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<comment>
; 块内日志格式串 "comment_system[]=" → 含义锚点：0xB5F47E

; 字段 11 —— clan_kind：偏移 56024，长度 1，线类型 u8（战队种类）
0xB5F1FB  call    sub_B06230     ; 读 u8
; 块内日志格式串 "clan_kind=" → 含义锚点：0xB5F506

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5F245
0xB5F245  push    <模块/错误码>
0xB5F245  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5F59F
0xB5F59F  mov     edx, [obj]
;       mov     edx, [edx+0x470h]
;       call    edx          ; vt[0x470]（10 实参）
```

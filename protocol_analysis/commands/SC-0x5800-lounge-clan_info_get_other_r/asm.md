# 汇编证据 —— SC-0x5800-lounge-clan_info_get_other_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x529` @ `0xB62370`）

```asm
; VA: 0xB62370（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB62370  push    0x529          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB623AE  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB625D5

; 字段 2 —— cinfo：偏移 4，长度 639，线类型 struct<cinfo>（战队信息（线长 639 = 读取器 `sub_B45940` 整函数展开；缓冲槽 648 = 预留 `sub_B41780` 槽步进 `0x288`））
0xB623EE  call    复合读取器（元素/结构体，见 notes.md）     ; struct<cinfo>
; 块内日志格式串 "cinfo=" → 含义锚点：0xB625FD

; 字段 3 —— leader_count：偏移 643，长度 4，线类型 u32（队长数（上限 **1**，`cmp ebx,1`@`0xB62430`））
0xB62404  call    sub_B02DD0     ; u32
; 块内日志格式串 "leader_count=" → 含义锚点：0xB6261A

; 字段 4 —— leader[]：偏移 647，长度 113，线类型 array<clan_member_card>（队长数组（元素线长 113 / 槽步进 `0x84`=132，读取器 `sub_B43100` = lpcard 同构卡片））
0xB6243F  call    复合读取器（元素/结构体，见 notes.md）     ; array<clan_member_card>
; 块内日志格式串 "leader[]=" → 含义锚点：0xB6261A

; 字段 5 —— subleader_count：偏移 （浮动），长度 4，线类型 u32（副队长数（上限 **4**，`cmp …,4`@`0xB624A3`））
0xB62493  call    sub_B02DD0     ; u32
; 块内日志格式串 "subleader_count=" → 含义锚点：0xB62692

; 字段 6 —— subleader[]：偏移 （浮动），长度 113，线类型 array<clan_member_card>（副队长数组（元素线长 113 / 槽步进 `0x84`=132，读取器 `sub_B43100` = lpcard 同构卡片））
0xB624BC  call    复合读取器（元素/结构体，见 notes.md）     ; array<clan_member_card>
; 块内日志格式串 "subleader[]=" → 含义锚点：0xB62692

; 字段 7 —— clan_kind：偏移 （浮动），长度 1，线类型 u8（战队种类）
0xB62522  call    sub_B06230     ; u8
; 块内日志格式串 "clan_kind=" → 含义锚点：0xB62716

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB62536
0xB62536  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB62536  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB62796
0xB62796  mov     <reg>, [obj]; mov <reg>, [<reg>+0x414h]
;       call    <reg>          ; vt[0x414]（7 实参）
```

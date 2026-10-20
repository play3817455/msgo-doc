# 汇编证据 —— SC-0x8E92-lounge-clan_info_get_self_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x54A` @ `B6BD04`）

```asm
; VA: B6BD04（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6BD04  push    0x54A          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6BD42  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6BFE2 → 含义锚点

; 字段 2 —— reason：偏移 4，长度 1，线类型 u8（原因（日志串 `reason=`））
B6BD82  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6C00A → 含义锚点

; 字段 3 —— cinfo：偏移 5，长度 639，线类型 struct<cinfo>（战队信息主体（日志串 `cinfo=`，打印器 `sub_B4E240`））
B6BDA6  call    sub_B41780 + sub_B45940     ; 读取 struct<cinfo>
; 块内日志格式串 @B6C034 → 含义锚点

; 字段 4 —— offer_body：偏移 644，长度 31，线类型 str（战队报价/宣言正文（日志串 `offer_body="`））
B6BDCB  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B6C063 → 含义锚点

; 字段 5 —— leader_count：偏移 675，长度 4，线类型 u32（队长列表计数（日志串 `leader={`；上限 1：`cmp ebx,1; ja` @`0xB6BE11`））
B6BDFD  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6C089 → 含义锚点

; 字段 6 —— leader：偏移 ，长度 ，线类型 array<member_info,N1>（队长列表）
B6BE41  call    sub_B43100     ; 读取 array<member_info,N1>
; 块内日志格式串 @B6C089 → 含义锚点

; 字段 7 —— subleader_count：偏移 ，长度 4，线类型 u32（副队长列表计数（日志串 `subleader={`；上限 4：`cmp [esp+…],4; ja` @`0xB6BE88`））
B6BE78  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6C0FE → 含义锚点

; 字段 8 —— subleader：偏移 ，长度 ，线类型 array<member_info,N2>（副队长列表）
B6BEC0  call    sub_B43100     ; 读取 array<member_info,N2>
; 块内日志格式串 @B6C0FE → 含义锚点

; 字段 9 —— clan_kind：偏移 ，长度 1，线类型 u8（战队种类（日志串 `clan_kind=`，打印器 `sub_B0C1F0`））
B6BF07  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6C18B → 含义锚点

; 字段 10 —— clan_forbidden：偏移 ，长度 1，线类型 u8（战队禁则位（日志串 `clan_forbidden=`））
B6BF2F  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6C1B0 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6BF43
B6BF43  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6C21C —— `vt[0x410]`（10 实参）
B6C21C  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x410h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B41780（cinfo 结构体预留）：add dword ptr [ecx],288h ⇒ claim 648（0xB41780..0xB41793）
; sub_B45940（cinfo 读取器，整函数逐字节展开）：
;    4 + 1 + 4 + 4 + 31×1 + 1 + 4 + 1 + 1 + 1 + 2 + 2 + 7×4 + 1 + 433×1 + 4 + 1 + 4 + 4×28×1 = 639
;    （字面量循环：31 @0xB459BF、433 @0xB45B05、内层 28×外层 4 @0xB45B74/0xB45B7F）
;    结构体跨度 0x288=648，含 9 字节填充（0x05..0x07、0x37、0x20A..0x20B、0x211..0x213）
;    ⇒ 线长 639 ≠ claim 648
; sub_B415D0（阵列预留，槽步进 0x84=132）：add dword ptr [edx],84h @0xB415F0
; sub_B43100（leader/subleader 元素读取器，整函数逐字节展开）：
;    4 + 25×1 + 4 + 1 + 1 + 1 + 2 + 18(sub_B068B0) + 4 + 31×1 + 1 + 1 + 1 + 4 + 4 + 1 + 1 + 4 + 4 + 1 = 113
;    （字面量循环 25 @0xB4313D、31 @0xB431FC；结构体跨度到 0x80，槽步进 132）
```

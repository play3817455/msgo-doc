# 汇编证据 —— SC-0x7ED3-lounge-clan_search_sortfilter_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2F01` @ `B69023`）

```asm
; VA: B69023（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69023  push    0x2F01          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B69061  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69207 → 含义锚点

; 字段 2 —— clan_kind：偏移 4，长度 1，线类型 u8（战队种类（日志串 `clan_kind=`））
B690A1  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6922F → 含义锚点

; 字段 3 —— sort_info：偏移 5，长度 18，线类型 struct<sort_info>（排序条件结构（日志串 `sort_info=`，打印器 `sub_B4F180`））
B690C5  call    sub_B411C0 + sub_B461E0     ; 读取 struct<sort_info>
; 块内日志格式串 @B69259 → 含义锚点

; 字段 4 —— search_res_count：偏移 23，长度 4，线类型 u32（搜索结果条数（日志串 `search_res={`；上限 100：`cmp ebx,64h; ja` @`0xB69107`））
B690DB  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69276 → 含义锚点

; 字段 5 —— search_res：偏移 27，长度 ，线类型 array<srch_res,N>（搜索结果数组）
B6913A  call    sub_B45BA0     ; 读取 array<srch_res,N>
; 块内日志格式串 @B69276 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B69168
B69168  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B69327 —— `vt[0x468]`（5 实参）
B69327  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x468h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B411C0（结构体预留）：mov edx,[ecx]; mov [eax],edx; add dword ptr [ecx],18h ⇒ claim 24（0xB411C0..0xB411D0）
; sub_B461E0（sort_info 读取器，整函数）：2 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 2 + 2 + 1 + 4 + 1 = 18（0xB461E0..0xB462D4）
; sub_B417A0（阵列预留，槽步进 0x78=120，按 count 循环）：add dword ptr [edx],78h @0xB417C0
; sub_B45BA0（search_res 元素读取器，整函数）：4 + 1 + 1 + 1 + 31×1 + 1 + 31×1 + 25×1 + 4 + 4 + 1 + 1 + 4 + 1 + 4 = 114
;    （三段字面量循环：cmp edi,1Fh @0xB45C2A、cmp edi,1Fh @0xB45C6A、cmp edi,19h @0xB45C8B）
```

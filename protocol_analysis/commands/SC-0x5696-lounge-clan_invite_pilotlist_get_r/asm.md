# 汇编证据 —— SC-0x5696-lounge-clan_invite_pilotlist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1789` @ `0xB61D15`）

```asm
; VA: 0xB61D15（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB61D15  push    0x1789          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB61D53  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB61F22

; 字段 2 —— invite_count：偏移 4，长度 4，线类型 u32（邀请列表条数（上限 `0x64`=100，`cmp ebx,64h`@`0xB61DB1`））
0xB61D85  call    sub_B02DD0     ; u32
; 块内日志格式串 "invite_count=" → 含义锚点：0xB61F3D

; 字段 3 —— invite_list[]：偏移 8，长度 55，线类型 array<invite>（邀请飞行员数组（元素线长 55 / 槽步进 `0x3C`=60，预留 `sub_B41230`））
0xB61DC0  call    复合读取器（元素/结构体，见 notes.md）     ; array<invite>
; 块内日志格式串 "invite_list[]=" → 含义锚点：0xB61F3D

; 字段 4 —— page_now：偏移 （浮动），长度 4，线类型 u32（当前页（偏移随数组长度浮动））
0xB61E1F  call    sub_B02DD0     ; u32
; 块内日志格式串 "page_now=" → 含义锚点：0xB61FBE

; 字段 5 —— page_max：偏移 （浮动），长度 4，线类型 u32（最大页（偏移随数组长度浮动））
0xB61E47  call    sub_B02DD0     ; u32
; 块内日志格式串 "page_max=" → 含义锚点：0xB61FE8

; 字段 6 —— sort_info：偏移 （浮动），长度 9，线类型 struct<sort_info>（排序信息（claim 9 = 预留 `sub_B41210` 槽步进 9；线长 9，读取器 `sub_B46080`））
0xB61E6F  call    复合读取器（元素/结构体，见 notes.md）     ; struct<sort_info>
; 块内日志格式串 "sort_info=" → 含义锚点：0xB6200B

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB61E83
0xB61E83  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB61E83  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB62087
0xB62087  mov     <reg>, [obj]; mov <reg>, [<reg>+0x480h]
;       call    <reg>          ; vt[0x480]（6 实参）
```

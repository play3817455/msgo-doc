# 汇编证据 —— SC-0x8D4F-lounge-get_special_a_info_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3C` @ `B6B8DD`）

```asm
; VA: B6B8DD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6B8DD  push    0x3C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6B918  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6BA53 → 含义锚点

; 字段 2 —— info：偏移 4，长度 40，线类型 struct<special_a_info>（特殊 A 信息（日志串 `info=`，打印器 `sub_B4F710`））
B6B958  call    sub_B418C0 + sub_B464A0     ; 读取 struct<special_a_info>
; 块内日志格式串 @B6BA7B → 含义锚点

; 字段 3 —— next：偏移 44，长度 12，线类型 struct<special_a_next>（下一阶段特殊 A 信息（日志串 `next=`，打印器 `sub_B506E0`））
B6B97C  call    sub_B41460 + sub_B46CD0     ; 读取 struct<special_a_next>
; 块内日志格式串 @B6BAA5 → 含义锚点

; 字段 4 —— type：偏移 56，长度 4，线类型 u32（信息种类（日志串 `type=`））
B6B9A0  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6BACC → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6B9B4
B6B9B4  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6BB20 —— `vt[0x524]`（4 实参）
B6BB20  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x524h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B418C0（结构体预留）：add dword ptr [ecx],28h ⇒ 40（0xB418C0..0xB418D0）
; sub_B464A0（info 读取器，整函数）：4 + 4 + 2 + 7×2 + 2 + 7×2 = 40（0xB464A0..0xB46559）
;    （两组字面量 7 元 u16：cmp edx,7 @0xB4650A、@0xB46541）
; sub_B41460（结构体预留）：add dword ptr [ecx],0Ch ⇒ 12（0xB41460..0xB41470）
; sub_B46CD0（next 读取器，整函数）：3×u32 = 12（0xB46CD0..0xB46D19）
```

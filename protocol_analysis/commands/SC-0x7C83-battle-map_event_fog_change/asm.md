# 汇编证据 —— SC-0x7C83-battle-map_event_fog_change

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x13` @ `B204EE`）

```asm
; VA: B204EE（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B204EE  push    0x13          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— nearz：偏移 0，长度 4，线类型 u32（雾近端 Z（日志串 `nearz=`））
B20529  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B206DC → 含义锚点

; 字段 2 —— farz：偏移 4，长度 4，线类型 u32（雾远端 Z（日志串 `farz=`））
B20569  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B20706 → 含义锚点

; 字段 3 —— color_r：偏移 8，长度 1，线类型 u8（雾颜色 R（日志串 `color_r=`，打印器 `sub_ADCBF0`））
B2058D  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B2072E → 含义锚点

; 字段 4 —— color_g：偏移 9，长度 1，线类型 u8（雾颜色 G（日志串 `color_g=`））
B205B1  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20758 → 含义锚点

; 字段 5 —— color_b：偏移 10，长度 1，线类型 u8（雾颜色 B（日志串 `color_b=`））
B205D9  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20782 → 含义锚点

; 字段 6 —— time：偏移 11，长度 4，线类型 u32（变化时长（日志串 `time=`））
B20601  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B207AE → 含义锚点

; 字段 7 —— elapsed_time：偏移 15，长度 4，线类型 u32（已流逝时间（日志串 `elapsed_time=`））
B20629  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B207D3 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2063D
B2063D  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B20836 —— `vt[0x350]`（7 实参）
B20836  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x350h]
;       call    <reg>
```

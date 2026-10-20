# 汇编证据 —— SC-0x81F1-lounge-pilot_dailyrecord_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x45` @ `B69A9B`）

```asm
; VA: B69A9B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69A9B  push    0x45          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pdaily：偏移 0，长度 39，线类型 array<pdaily,3>（每日战绩列表（固定 3 元素；日志串 `pdaily={`，元素打印器 `sub_B0A1A0`））
B69AD8  call    sub_B07540 ×3     ; 读取 array<pdaily,3>
; 块内日志格式串 @B69C64 → 含义锚点

; 字段 2 —— is_all_clear：偏移 39，长度 1，线类型 u8（是否全部完成（日志串 `is_all_clear=`））
B69B16  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B69CD0 → 含义锚点

; 字段 3 —— cnt_completed：偏移 40，长度 4，线类型 u32（已完成数量（日志串 `cnt_completed=`））
B69B53  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69CFC → 含义锚点

; 字段 4 —— year：偏移 44，长度 2，线类型 u16（年（日志串 `year=`））
B69B77  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B69D27 → 含义锚点

; 字段 5 —— month：偏移 46，长度 1，线类型 u8（月（日志串 `month=`））
B69B9B  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B69D4F → 含义锚点

; 字段 6 —— day：偏移 47，长度 1，线类型 u8（日（日志串 `day=`））
B69BC3  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B69D74 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B69BD7
B69BD7  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B69DCF —— `vt[0x15C]`（6 实参）
B69DCF  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x15Ch]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B06160（定长 3 元阵列预留）：add dword ptr [ecx],3Ch ⇒ 60 = 3×20（0xB06160..0xB06170）
; sub_B07540（pdaily 元素读取器，整函数）：4 + 4 + 4 + 1 = 13（0xB07540..0xB0759B）
; 循环上界字面量 3：cmp edi,3 @0xB69AEA；循环步进 add ebx,14h @0xB69AE7
; 元素打印器 sub_B0A1A0（打印 pdaily 各元素）
```

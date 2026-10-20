# 汇编证据 —— SC-0x7B30-lounge-pilot_rental_module_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B686CC`）

```asm
; VA: B686CC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B686CC  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B68707  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68811 → 含义锚点

; 字段 2 —— module_id：偏移 4，长度 4，线类型 u32（租用模块 ID（日志串 `module_id=`））
B68744  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6883B → 含义锚点

; 字段 3 —— count：偏移 8，长度 4，线类型 u32（数量（日志串 `count=`））
B68768  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68860 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68778
B68778  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B688B4 —— `vt[0xE8]`（3 实参）
B688B4  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0xE8h]
;       call    <reg>
```

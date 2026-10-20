# 汇编证据 —— SC-0x838B-lounge-msma_buildup_reset_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A` @ `B6A343`）

```asm
; VA: B6A343（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6A343  push    0x1A          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6A37E  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6A4B2 → 含义锚点

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
B6A3BE  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B6A4E0 → 含义锚点

; 字段 3 —— up_param：偏移 12，长度 14，线类型 u16[7]（改造参数（固定 7×u16；日志串 `up_param={`））
B6A3E6  call    sub_B02DF0 ×7     ; 读取 u16[7]
; 块内日志格式串 @B6A4FB → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6A413
B6A413  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6A591 —— `vt[0x2C4]`（4 实参）
B6A591  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x2C4h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B41590（定长 7 元 u16 阵列预留）：add dword ptr [ecx],0Eh ⇒ 14 = 7×2（0xB41590..0xB415A0）
; 循环上界字面量 7：cmp edi,7 @0xB6A3F8；循环步进 add ebx,2 @0xB6A3F5
```

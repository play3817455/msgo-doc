# 汇编证据 —— SC-0x8AF0-lounge-deckcost_extend_info_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B6B123`）

```asm
; VA: B6B123（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6B123  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— deckcost：偏移 0，长度 2，线类型 u16（卡组费用上限（日志串 `deckcost=`））
B6B15E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B6B24E → 含义锚点

; 字段 2 —— remain：偏移 2，长度 2，线类型 u16（剩余时间（日志串 `remain=`））
B6B19E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B6B274 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6B1AE
B6B1AE  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6B2C9 —— `vt[0x4C4]`（2 实参）
B6B2C9  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x4C4h]
;       call    <reg>
```

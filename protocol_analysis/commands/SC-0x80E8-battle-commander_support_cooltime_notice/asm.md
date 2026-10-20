# 汇编证据 —— SC-0x80E8-battle-commander_support_cooltime_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B21414`）

```asm
; VA: B21414（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B21414  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— support_type：偏移 0，长度 4，线类型 u32（支援种类（日志串 `support_type=`））
B2144F  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21562 → 含义锚点

; 字段 2 —— remain_msec：偏移 4，长度 4，线类型 u32（剩余冷却毫秒（日志串 `remain_msec=`））
B2148F  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B2158C → 含义锚点

; 字段 3 —— target_change_msec：偏移 8，长度 4，线类型 u32（目标切换冷却毫秒（日志串 `target_change_msec=`））
B214B3  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B215B1 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B214C3
B214C3  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B21605 —— `vt[0x2D4]`（3 实参）
B21605  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x2D4h]
;       call    <reg>
```

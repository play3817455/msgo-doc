# 汇编证据 —— SC-0x81FB-lounge-msma_weapon_unlock_complete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11` @ `B6A091`）

```asm
; VA: B6A091（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6A091  push    0x11          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6A0CC  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6A21F → 含义锚点

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
B6A10C  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B6A249 → 含义锚点

; 字段 3 —— item_id：偏移 12，长度 4，线类型 u32（武器道具 ID（日志串 `item_id=`））
B6A14C  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6A273 → 含义锚点

; 字段 4 —— db_index：偏移 16，长度 1，线类型 u8（DB 索引（日志串 `db_index=`））
B6A170  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6A296 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6A180
B6A180  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6A2F1 —— `vt[0x2E4]`（5 实参）
B6A2F1  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x2E4h]
;       call    <reg>
```

# 汇编证据 —— SC-0x8F3E-lounge-msma_equipset_del_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE` @ `B6C485`）

```asm
; VA: B6C485（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6C485  push    0xE          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6C4C0  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6C5D3 → 含义锚点

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
B6C500  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B6C601 → 含义锚点

; 字段 3 —— slot：偏移 12，长度 2，线类型 u16（装备槽序号（日志串 `slot=`））
B6C524  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B6C627 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6C534
B6C534  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6C67C —— `vt[0x318]`（4 实参）
B6C67C  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x318h]
;       call    <reg>
```

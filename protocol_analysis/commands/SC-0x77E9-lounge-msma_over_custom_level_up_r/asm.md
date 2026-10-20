# 汇编证据 —— SC-0x77E9-lounge-msma_over_custom_level_up_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B67BE0`）

```asm
; VA: B67BE0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B67BE0  push    0x10          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B67C1B  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B67D2E → 含义锚点

; 字段 2 —— uniq_msid：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniq_msid=`））
B67C5B  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B67D5C → 含义锚点

; 字段 3 —— level：偏移 12，长度 4，线类型 u32（改造等级（日志串 `level=`））
B67C7F  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B67D81 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B67C8F
B67C8F  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B67DD5 —— `vt[0x5B4]`（4 实参）
B67DD5  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x5B4h]
;       call    <reg>
```

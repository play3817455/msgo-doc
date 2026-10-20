# 汇编证据 —— SC-0x7899-lounge-msma_over_custom_buildup_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B68057`）

```asm
; VA: B68057（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B68057  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— uniq_msid：偏移 0，长度 8，线类型 u64（机体唯一 ID（日志串 `uniq_msid=`））
B68092  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B681A5 → 含义锚点

; 字段 2 —— param_idx：偏移 8，长度 2，线类型 u16（改造参数序号（日志串 `param_idx=`））
B680D2  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B681D0 → 含义锚点

; 字段 3 —— up_param：偏移 10，长度 2，线类型 u16（改造参数值（日志串 `up_param=`））
B680F6  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B681F6 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68106
B68106  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6824F —— `vt[0x5CC]`（4 实参）
B6824F  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x5CCh]
;       call    <reg>
```

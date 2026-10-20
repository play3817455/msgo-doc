# 汇编证据 —— SC-0x7998-lounge-msma_over_custom_use_capsule_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `B6841E`）

```asm
; VA: B6841E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6841E  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B68459  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B685AC → 含义锚点

; 字段 2 —— uniq_msid：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniq_msid=`））
B68499  call    sub_B06200     ; 读取 u64
; 块内日志格式串 @B685D6 → 含义锚点

; 字段 3 —— item_id：偏移 12，长度 4，线类型 u32（消耗道具 ID（日志串 `item_id=`））
B684D9  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68600 → 含义锚点

; 字段 4 —— exp：偏移 16，长度 4，线类型 u32（获得改造经验（日志串 `exp=`））
B684FD  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68625 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6850D
B6850D  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6867D —— `vt[0x5C0]`（5 实参）
B6867D  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x5C0h]
;       call    <reg>
```

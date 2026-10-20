# 汇编证据 —— SC-0x817D-lounge-quest_clear_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x609` @ `B69537`）

```asm
; VA: B69537（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69537  push    0x609          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B69575  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6967F → 含义锚点

; 字段 2 —— quest_id：偏移 4，长度 4，线类型 u32（任务 ID（日志串 `quest_id=`））
B695B5  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B696A9 → 含义锚点

; 字段 3 —— pay_comment：偏移 8，长度 1537，线类型 str（付酬备注（日志串 `pay_comment="`））
B695D0  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B696D1 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B695FC
B695FC  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6972E —— `vt[0x3CC]`（3 实参）
B6972E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x3CCh]
;       call    <reg>
```

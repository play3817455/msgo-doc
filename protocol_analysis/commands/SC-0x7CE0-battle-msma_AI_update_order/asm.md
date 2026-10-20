# 汇编证据 —— SC-0x7CE0-battle-msma_AI_update_order

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `B20B44`）

```asm
; VA: B20B44（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B20B44  push    0x7          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
B20B7F  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B20C93 → 含义锚点

; 字段 2 —— kind：偏移 2，长度 1，线类型 u8（指令种类（日志串 `kind=`））
B20BBF  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20CBB → 含义锚点

; 字段 3 —— param：偏移 3，长度 4，线类型 u32（指令参数（日志串 `param=`））
B20BE3  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B20CE2 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B20BF3
B20BF3  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B20D36 —— `vt[0x264]`（3 实参）
B20D36  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x264h]
;       call    <reg>
```

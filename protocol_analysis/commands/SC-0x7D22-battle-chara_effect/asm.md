# 汇编证据 —— SC-0x7D22-battle-chara_effect

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B20903`）

```asm
; VA: B20903（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B20903  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
B2093E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B20A52 → 含义锚点

; 字段 2 —— effect_id：偏移 2，长度 2，线类型 u16（演出效果 ID（日志串 `effect_id=`））
B2097E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B20A7D → 含义锚点

; 字段 3 —— is_start：偏移 4，长度 1，线类型 u8（开始/结束标志（日志串 `is_start=`））
B209A2  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20AA0 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B209B2
B209B2  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B20AF7 —— `vt[0x388]`（3 实参）
B20AF7  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x388h]
;       call    <reg>
```

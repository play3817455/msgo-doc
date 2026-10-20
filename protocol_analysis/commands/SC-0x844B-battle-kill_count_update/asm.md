# 汇编证据 —— SC-0x844B-battle-kill_count_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x17` @ `B21B9F`）

```asm
; VA: B21B9F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B21B9F  push    0x17          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— reason：偏移 0，长度 4，线类型 u32（击杀原因（日志串 `reason=`））
B21BDA  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21D8D → 含义锚点

; 字段 2 —— ent_id_dead：偏移 4，长度 2，线类型 u16（被击杀实体 ID（日志串 `ent_id_dead=`））
B21C1A  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B21DB8 → 含义锚点

; 字段 3 —— world_id_kill：偏移 6，长度 4，线类型 u32（击杀方世界 ID（日志串 `world_id_kill=`））
B21C3E  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21DE2 → 含义锚点

; 字段 4 —— pilot_id_kill：偏移 10，长度 4，线类型 u32（击杀方飞行员 ID（日志串 `pilot_id_kill=`））
B21C62  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21E0C → 含义锚点

; 字段 5 —— kill_streak：偏移 14，长度 4，线类型 u32（连杀数（日志串 `kill_streak=`））
B21C8A  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21E36 → 含义锚点

; 字段 6 —— weapon_itemid：偏移 18，长度 4，线类型 u32（武器道具 ID（日志串 `weapon_itemid=`））
B21CB2  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21E60 → 含义锚点

; 字段 7 —— is_extend_style_change_limit：偏移 22，长度 1，线类型 u8（是否放宽风格切换限制（日志串 `is_extend_style_change_limit=`））
B21CDA  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B21E83 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B21CEE
B21CEE  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B21EE1 —— `vt[0x220]`（7 实参）
B21EE1  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x220h]
;       call    <reg>
```

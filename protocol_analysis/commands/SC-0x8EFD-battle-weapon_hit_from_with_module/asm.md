# 汇编证据 —— SC-0x8EFD-battle-weapon_hit_from_with_module

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `B23893`）

```asm
; VA: B23893（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B23893  push    0x7          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（受击实体 ID（日志串 `ent_id=`））
B238CE  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B239E2 → 含义锚点

; 字段 2 —— module_hp：偏移 2，长度 4，线类型 u32（模块 HP（日志串 `module_hp=`））
B2390E  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B23A0C → 含义锚点

; 字段 3 —— is_force：偏移 6，长度 1，线类型 u8（是否强制（日志串 `is_force=`））
B23932  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B23A2F → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B23942
B23942  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B23A86 —— `vt[0x208]`（3 实参）
B23A86  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x208h]
;       call    <reg>
```

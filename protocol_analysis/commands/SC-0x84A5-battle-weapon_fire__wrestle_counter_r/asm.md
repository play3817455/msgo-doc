# 汇编证据 —— SC-0x84A5-battle-weapon_fire__wrestle_counter_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B21968`）

```asm
; VA: B21968（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B21968  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
B219A3  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B21AAE → 含义锚点

; 字段 2 —— itemid：偏移 2，长度 4，线类型 u32（武器道具 ID（日志串 `itemid=`））
B219E0  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B21AD8 → 含义锚点

; 字段 3 —— target_ent_id：偏移 6，长度 2，线类型 u16（目标实体 ID（日志串 `target_ent_id=`））
B21A04  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B21AFE → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B21A14
B21A14  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B21B53 —— `vt[0x1AC]`（3 实参）
B21B53  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x1ACh]
;       call    <reg>
```

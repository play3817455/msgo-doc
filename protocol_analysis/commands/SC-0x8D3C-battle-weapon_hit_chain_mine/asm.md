# 汇编证据 —— SC-0x8D3C-battle-weapon_hit_chain_mine

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE` @ `B22C69`）

```asm
; VA: B22C69（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B22C69  push    0xE          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— weapon_itemid：偏移 0，长度 4，线类型 u32（武器道具 ID（日志串 `weapon_itemid=`））
B22CA4  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22E2F → 含义锚点

; 字段 2 —— to_ent_id：偏移 4，长度 2，线类型 u16（目标实体 ID（日志串 `to_ent_id=`））
B22CE4  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22E5A → 含义锚点

; 字段 3 —— from_ent_id：偏移 6，长度 2，线类型 u16（来源实体 ID（日志串 `from_ent_id=`））
B22D08  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22E85 → 含义锚点

; 字段 4 —— hit_pos_x：偏移 8，长度 2，线类型 u16（命中点 X（日志串 `hit_pos_x=`））
B22D2C  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22EB0 → 含义锚点

; 字段 5 —— hit_pos_y：偏移 10，长度 2，线类型 u16（命中点 Y（日志串 `hit_pos_y=`））
B22D54  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22EDB → 含义锚点

; 字段 6 —— hit_pos_z：偏移 12，长度 2，线类型 u16（命中点 Z（日志串 `hit_pos_z=`））
B22D7C  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22F01 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B22D90
B22D90  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B22F5E —— `vt[0x1F4]`（6 实参）
B22F5E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x1F4h]
;       call    <reg>
```

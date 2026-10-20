# 汇编证据 —— SC-0x894B-battle-weapon_fire__destruct

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `B224D3`）

```asm
; VA: B224D3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B224D3  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
B2250E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B225FE → 含义锚点

; 字段 2 —— weapon_itemid：偏移 2，长度 4，线类型 u32（武器道具 ID（日志串 `weapon_itemid=`））
B2254E  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22623 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2255E
B2255E  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B22677 —— `vt[0x1D4]`（2 实参）
B22677  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x1D4h]
;       call    <reg>
```

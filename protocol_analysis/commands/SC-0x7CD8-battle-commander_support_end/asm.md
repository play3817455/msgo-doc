# 汇编证据 —— SC-0x7CD8-battle-commander_support_end

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `B20D83`）

```asm
; VA: B20D83（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B20D83  push    0xB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8（阵营（日志串 `team=`，打印器 `sub_B0C1F0`））
B20DBE  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20F47 → 含义锚点

; 字段 2 —— troops：偏移 1，长度 1，线类型 u8（部队编号（日志串 `troops=`））
B20DFE  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B20F71 → 含义锚点

; 字段 3 —— support_type：偏移 2，长度 4，线类型 u32（支援种类（日志串 `support_type=`））
B20E22  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B20F9D → 含义锚点

; 字段 4 —— ent_id：偏移 6，长度 2，线类型 u16（支援实体 ID（日志串 `ent_id=`））
B20E46  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B20FC8 → 含义锚点

; 字段 5 —— spt_ms_index：偏移 8，长度 2，线类型 u16（支援机体序号（日志串 `spt_ms_index=`））
B20E6E  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B20FF3 → 含义锚点

; 字段 6 —— spt_spot_index：偏移 10，长度 1，线类型 u8（支援点位序号（日志串 `spt_spot_index=`））
B20E96  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B21016 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B20EAA
B20EAA  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B21075 —— `vt[0x2C0]`（6 实参）
B21075  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x2C0h]
;       call    <reg>
```

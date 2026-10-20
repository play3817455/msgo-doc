# 汇编证据 —— SC-0x37C1-battle-weapon_fire__for_myself_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `0xB14486`）

```asm
; VA: 0xB14486（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB14486  push    0xB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 4，线类型 u32（实体 ID）
0xB144C1  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "ent_id=" → 含义锚点：0xB14624

; 字段 2 —— target_x：偏移 4，长度 2，线类型 u16（目标 X）
0xB14501  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "target_x=" → 含义锚点：0xB1464F

; 字段 3 —— target_y：偏移 6，长度 2，线类型 u16（目标 Y）
0xB14525  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "target_y=" → 含义锚点：0xB1467A

; 字段 4 —— target_z：偏移 8，长度 2，线类型 u16（目标 Z）
0xB14549  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "target_z=" → 含义锚点：0xB146A5

; 字段 5 —— begin1_end0：偏移 10，长度 1，线类型 u8（开始/结束标志）
0xB14571  call    sub_B06230     ; 读 u8
; 块内日志格式串 "begin1_end0=" → 含义锚点：0xB146C8

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB145AC
0xB145AC  push    <模块/错误码>
0xB145AC  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB14743
0xB14743  mov     edx, [obj]
;       mov     edx, [edx+0x1D8h]
;       call    edx          ; vt[0x1D8]（5 实参）
```

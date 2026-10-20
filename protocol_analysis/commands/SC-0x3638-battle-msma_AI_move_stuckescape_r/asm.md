# 汇编证据 —— SC-0x3638-battle-msma_AI_move_stuckescape_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA` @ `0xB1418E`）

```asm
; VA: 0xB1418E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1418E  push    0xA          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID）
0xB141C9  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "AI_ent_id=" → 含义锚点：0xB1432D

; 字段 2 —— to_x：偏移 2，长度 2，线类型 u16（目标 X）
0xB14209  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "to_x=" → 含义锚点：0xB14358

; 字段 3 —— to_y：偏移 4，长度 2，线类型 u16（目标 Y）
0xB1422D  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "to_y=" → 含义锚点：0xB14383

; 字段 4 —— to_z：偏移 6，长度 2，线类型 u16（目标 Z）
0xB14251  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "to_z=" → 含义锚点：0xB143AE

; 字段 5 —— msec：偏移 8，长度 2，线类型 u16（持续毫秒）
0xB14279  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "msec=" → 含义锚点：0xB143D4

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB142B4
0xB142B4  push    <模块/错误码>
0xB142B4  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1444E
0xB1444E  mov     edx, [obj]
;       mov     edx, [edx+0x26Ch]
;       call    edx          ; vt[0x26C]（5 实参）
```

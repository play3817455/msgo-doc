# 汇编证据 —— SC-0x4C36-battle-rideable_msma_get_down_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A` @ `0xB162FB`）

```asm
; VA: 0xB162FB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB162FB  push    0x1A          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB16336  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB16511

; 字段 2 —— access_type：偏移 4，长度 2，线类型 u16（乘降类型）
0xB16376  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "access_type=" → 含义锚点：0xB1653C

; 字段 3 —— from_ent_id：偏移 6，长度 2，线类型 u16（来源实体 ID）
0xB1639A  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "from_ent_id=" → 含义锚点：0xB16567

; 字段 4 —— to_world_id：偏移 8，长度 4，线类型 u32（目标世界 ID）
0xB163BE  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "to_world_id=" → 含义锚点：0xB16591

; 字段 5 —— to_pilot_id：偏移 12，长度 4，线类型 u32（目标飞行员 ID）
0xB163E6  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "to_pilot_id=" → 含义锚点：0xB165BB

; 字段 6 —— to_ent_id：偏移 16，长度 2，线类型 u16（目标实体 ID）
0xB1640E  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "to_ent_id=" → 含义锚点：0xB165E6

; 字段 7 —— hp_now：偏移 18，长度 4，线类型 u32（当前 HP）
0xB16436  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "hp_now=" → 含义锚点：0xB16610

; 字段 8 —— hp_max：偏移 22，长度 4，线类型 u32（最大 HP）
0xB1645E  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "hp_max=" → 含义锚点：0xB16635

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16499
0xB16499  push    <模块/错误码>
0xB16499  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB166C2
0xB166C2  mov     edx, [obj]
;       mov     edx, [edx+0x318h]
;       call    edx          ; vt[0x318]（8 实参）
```

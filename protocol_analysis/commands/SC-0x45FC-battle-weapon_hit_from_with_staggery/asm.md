# 汇编证据 —— SC-0x45FC-battle-weapon_hit_from_with_staggery

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB15730`）

```asm
; VA: 0xB15730（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB15730  push    0x10          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB1576B  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB158F7

; 字段 2 —— hit_dir：偏移 2，长度 2，线类型 u16（受击方向）
0xB157AB  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "hit_dir=" → 含义锚点：0xB15922

; 字段 3 —— spbits：偏移 4，长度 4，线类型 u32（状态位（special bits））
0xB157CF  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "spbits=" → 含义锚点：0xB1594C

; 字段 4 —— optbits：偏移 8，长度 4，线类型 u32（选项位）
0xB157F3  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "optbits=" → 含义锚点：0xB15976

; 字段 5 —— staggery_power：偏移 12，长度 2，线类型 u16（硬直力度）
0xB1581B  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "staggery_power=" → 含义锚点：0xB159A1

; 字段 6 —— staggery_msec：偏移 14，长度 2，线类型 u16（硬直毫秒）
0xB15843  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "staggery_msec=" → 含义锚点：0xB159C7

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1587E
0xB1587E  push    <模块/错误码>
0xB1587E  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB15A47
0xB15A47  mov     edx, [obj]
;       mov     edx, [edx+0x204h]
;       call    edx          ; vt[0x204]（6 实参）
```

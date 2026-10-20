# 汇编证据 —— SC-0x4C7D-battle-entity_msma_unattended_state

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB16119`）

```asm
; VA: 0xB16119（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB16119  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB16154  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB1623B

; 字段 2 —— state_bit：偏移 2，长度 2，线类型 u16（状态位）
0xB16191  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "state_bit=" → 含义锚点：0xB16261

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB161C2
0xB161C2  push    <模块/错误码>
0xB161C2  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB162C3
0xB162C3  mov     edx, [obj]
;       mov     edx, [edx+0x17Ch]
;       call    edx          ; vt[0x17C]（2 实参）
```

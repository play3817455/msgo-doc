# 汇编证据 —— SC-0x39B3-battle-msma_AI_update_move_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB149D3`）

```asm
; VA: 0xB149D3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB149D3  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID）
0xB14A0E  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "AI_ent_id=" → 含义锚点：0xB14B4A

; 字段 2 —— end_x：偏移 2，长度 2，线类型 u16（终点 X）
0xB14A4E  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "end_x=" → 含义锚点：0xB14B75

; 字段 3 —— end_y：偏移 4，长度 2，线类型 u16（终点 Y）
0xB14A72  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "end_y=" → 含义锚点：0xB14BA0

; 字段 4 —— end_z：偏移 6，长度 2，线类型 u16（终点 Z）
0xB14A96  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "end_z=" → 含义锚点：0xB14BC6

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB14AD1
0xB14AD1  push    <模块/错误码>
0xB14AD1  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB14C38
0xB14C38  mov     edx, [obj]
;       mov     edx, [edx+0x258h]
;       call    edx          ; vt[0x258]（4 实参）
```

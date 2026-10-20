# 汇编证据 —— SC-0x3C70-battle-mission_safety_area_return_to_area

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB14C70`）

```asm
; VA: 0xB14C70（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB14C70  push    0x2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB14CAB  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB14D56

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB14CE2
0xB14CE2  push    <模块/错误码>
0xB14CE2  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB14DB0
0xB14DB0  mov     edx, [obj]
;       mov     edx, [edx+0x398h]
;       call    edx          ; vt[0x398]（1 实参）
```

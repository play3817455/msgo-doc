# 汇编证据 —— SC-0x3BBE-battle-room_chat_editing_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `0xB1479F`）

```asm
; VA: 0xB1479F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1479F  push    0x9          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— world_id：偏移 0，长度 4，线类型 u32（世界 ID）
0xB147DA  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "world_id=" → 含义锚点：0xB148E4

; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（飞行员 ID）
0xB14817  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB1490E

; 字段 3 —— is_editing：偏移 8，长度 1，线类型 u8（是否正在编辑）
0xB1483B  call    sub_B06230     ; 读 u8
; 块内日志格式串 "is_editing=" → 含义锚点：0xB14931

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1486C
0xB1486C  push    <模块/错误码>
0xB1486C  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1499B
0xB1499B  mov     edx, [obj]
;       mov     edx, [edx+0xD8h]
;       call    edx          ; vt[0xD8]（3 实参）
```

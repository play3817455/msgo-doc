# 汇编证据 —— SC-0x339C-battle-roomlobby_game_ready_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB13CFB`）

```asm
; VA: 0xB13CFB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB13CFB  push    0x10          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB13D36  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB13E68

; 字段 2 —— world_id：偏移 4，长度 4，线类型 u32（世界 ID）
0xB13D73  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "world_id=" → 含义锚点：0xB13E92

; 字段 3 —— pilot_id：偏移 8，长度 4，线类型 u32（飞行员 ID）
0xB13D97  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB13EBC

; 字段 4 —— stat：偏移 12，长度 4，线类型 u32（状态）
0xB13DBB  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "stat=" → 含义锚点：0xB13EE1

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB13DF0
0xB13DF0  push    <模块/错误码>
0xB13DF0  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB13F4F
0xB13F4F  mov     edx, [obj]
;       mov     edx, [edx+0xA4h]
;       call    edx          ; vt[0xA4]（4 实参）
```

# 汇编证据 —— SC-0x45E4-lounge-msma_weapon_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11` @ `0xB5DEEB`）

```asm
; VA: 0xB5DEEB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5DEEB  push    0x11          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5DF26  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5E079

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB5DF66  call    sub_B06200     ; 读 u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB5E0A3

; 字段 3 —— item_id：偏移 12，长度 4，线类型 u32（道具 ID）
0xB5DFA6  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "item_id=" → 含义锚点：0xB5E0CD

; 字段 4 —— db_index：偏移 16，长度 1，线类型 u8（DB 索引）
0xB5DFCA  call    sub_B06230     ; 读 u8
; 块内日志格式串 "db_index=" → 含义锚点：0xB5E0F0

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5E001
0xB5E001  push    <模块/错误码>
0xB5E001  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5E165
0xB5E165  mov     edx, [obj]
;       mov     edx, [edx+0x2DCh]
;       call    edx          ; vt[0x2DC]（4 实参）
```

# 汇编证据 —— SC-0x3B34-lounge-pilot_newpilotchallenge_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x505` @ `0xB5CFA0`）

```asm
; VA: 0xB5CFA0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5CFA0  push    0x505          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5CFDE  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5D109

; 字段 2 —— on_clear：偏移 4，长度 1，线类型 u8（是否达成通关）
0xB5D01B  call    sub_B06230     ; 读 u8
; 块内日志格式串 "on_clear=" → 含义锚点：0xB5D131

; 字段 3 —— bonus_info[40]：偏移 5，长度 29，线类型 array<bonus_info>（奖励信息（固定 40 元素，元素线长 29 / 槽步进 `0x20`=32，`sub_B41420`））
0xB5D046  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<bonus_info>
; 块内日志格式串 "bonus_info[40]=" → 含义锚点：0xB5D14E

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5D091
0xB5D091  push    <模块/错误码>
0xB5D091  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5D1F7
0xB5D1F7  mov     edx, [obj]
;       mov     edx, [edx+0x184h]
;       call    edx          ; vt[0x184]（3 实参）
```

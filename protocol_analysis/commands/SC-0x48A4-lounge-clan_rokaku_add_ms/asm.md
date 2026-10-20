# 汇编证据 —— SC-0x48A4-lounge-clan_rokaku_add_ms

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11108` @ `0xB5E74A`）

```asm
; VA: 0xB5E74A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5E74A  push    0x11108          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ms_count：偏移 0，长度 4，线类型 u32（机体条数（上限 `0xA8`=168，`cmp ebx,0A8h`@`0xB5E7A6`））
0xB5E77A  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "ms_count=" → 含义锚点：0xB5E8DE

; 字段 2 —— ms[]：偏移 4，长度 401，线类型 array<ms>（机体数组（元素线长 401 / 槽步进 `0x1A0`=416，`sub_B41880`））
0xB5E7DA  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<ms>
; 块内日志格式串 "ms[]=" → 含义锚点：0xB5E8DE

; 字段 3 —— is_firstonetime：偏移 69892，长度 4，线类型 u32（是否首次）
0xB5E81F  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "is_firstonetime=" → 含义锚点：0xB5E960

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5E872
0xB5E872  push    <模块/错误码>
0xB5E872  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5E9C7
0xB5E9C7  mov     edx, [obj]
;       mov     edx, [edx+0x488h]
;       call    edx          ; vt[0x488]（3 实参）
```

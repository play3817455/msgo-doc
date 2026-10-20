# 汇编证据 —— SC-0x35F8-lounge-restrict_exchange_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x64` @ `0xB5BEB7`）

```asm
; VA: 0xB5BEB7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5BEB7  push    0x64          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— exchanges：偏移 0，长度 100，线类型 u16[50]（交换限制表（固定 50×u16，无线上计数；`cmp edi,32h`@`0xB5BF08`））
0xB5BEF6  call    复合读取器（元素/结构体，见 notes.md）     ; 读 u16[50]
; 块内日志格式串 "exchanges=" → 含义锚点：0xB5BFB6

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5BF4A
0xB5BF4A  push    <模块/错误码>
0xB5BF4A  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5C05A
0xB5C05A  mov     edx, [obj]
;       mov     edx, [edx+0x4D8h]
;       call    edx          ; vt[0x4D8]（1 实参）
```

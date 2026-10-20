# 汇编证据 —— SC-0x483F-battle-dynamic_taskforce_order_result

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `0xB152C9`）

```asm
; VA: 0xB152C9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB152C9  push    0xB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB15304  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB15467

; 字段 2 —— order_index：偏移 4，长度 1，线类型 u8（指令序号）
0xB15344  call    sub_B06230     ; 读 u8
; 块内日志格式串 "order_index=" → 含义锚点：0xB1548F

; 字段 3 —— order_number：偏移 5，长度 1，线类型 u8（指令编号）
0xB15368  call    sub_B06230     ; 读 u8
; 块内日志格式串 "order_number=" → 含义锚点：0xB154B9

; 字段 4 —— order_kind：偏移 6，长度 1，线类型 u8（指令种类）
0xB1538C  call    sub_B06230     ; 读 u8
; 块内日志格式串 "order_kind=" → 含义锚点：0xB154E3

; 字段 5 —— order_param：偏移 7，长度 4，线类型 u32（指令参数）
0xB153B4  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "order_param=" → 含义锚点：0xB1550A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB153EF
0xB153EF  push    <模块/错误码>
0xB153EF  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB15582
0xB15582  mov     edx, [obj]
;       mov     edx, [edx+0x300h]
;       call    edx          ; vt[0x300]（5 实参）
```

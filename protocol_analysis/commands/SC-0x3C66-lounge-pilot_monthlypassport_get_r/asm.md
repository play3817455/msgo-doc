# 汇编证据 —— SC-0x3C66-lounge-pilot_monthlypassport_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB5D3CC`）

```asm
; VA: 0xB5D3CC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5D3CC  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5D407  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5D4F6

; 字段 2 —— remaining_days：偏移 4，长度 1，线类型 u8（剩余天数）
0xB5D447  call    sub_B06230     ; 读 u8
; 块内日志格式串 "remaining_days=" → 含义锚点：0xB5D519

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5D47E
0xB5D47E  push    <模块/错误码>
0xB5D47E  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5D57C
0xB5D57C  mov     edx, [obj]
;       mov     edx, [edx+0x18Ch]
;       call    edx          ; vt[0x18C]（2 实参）
```

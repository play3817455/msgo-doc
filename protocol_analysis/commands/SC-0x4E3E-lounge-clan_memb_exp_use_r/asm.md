# 汇编证据 —— SC-0x4E3E-lounge-clan_memb_exp_use_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB5F5D7`）

```asm
; VA: 0xB5F5D7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5F5D7  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5F612  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5F701

; 字段 2 —— exp：偏移 4，长度 4，线类型 u32（经验值）
0xB5F652  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "exp=" → 含义锚点：0xB5F726

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5F689
0xB5F689  push    <模块/错误码>
0xB5F689  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5F786
0xB5F786  mov     edx, [obj]
;       mov     edx, [edx+0x49Ch]
;       call    edx          ; vt[0x49C]（2 实参）
```

# 汇编证据 —— SC-0x4DA5-lounge-chargepoint_charge_url_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x404` @ `0xB5ED70`）

```asm
; VA: 0xB5ED70（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5ED70  push    0x404          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5EDAE  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5EE8B

; 字段 2 —— url：偏移 4，长度 1024，线类型 str（充值 URL（槽位预算 `0x400`=1024））
0xB5EDE2  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "url=" → 含义锚点：0xB5EEB3

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5EE13
0xB5EE13  push    <模块/错误码>
0xB5EE13  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5EF1C
0xB5EF1C  mov     edx, [obj]
;       mov     edx, [edx+0x100h]
;       call    edx          ; vt[0x100]（2 实参）
```

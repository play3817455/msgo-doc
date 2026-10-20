# 汇编证据 —— SC-0x4B2F-lounge-pilot_rating_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB5EA23`）

```asm
; VA: 0xB5EA23（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5EA23  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— rate_vslocal：偏移 0，长度 2，线类型 u16（本地对战评级）
0xB5EA5E  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "rate_vslocal=" → 含义锚点：0xB5EB45

; 字段 2 —— rate_vslocal_4ev：偏移 2，长度 2，线类型 u16（本地对战评级（4ev））
0xB5EA9B  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "rate_vslocal_4ev=" → 含义锚点：0xB5EB6B

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5EACC
0xB5EACC  push    <模块/错误码>
0xB5EACC  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5EBCD
0xB5EBCD  mov     edx, [obj]
;       mov     edx, [edx+0xBCh]
;       call    edx          ; vt[0xBC]（2 实参）
```

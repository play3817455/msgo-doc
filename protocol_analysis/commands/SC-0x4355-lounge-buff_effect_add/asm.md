# 汇编证据 —— SC-0x4355-lounge-buff_effect_add

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB5D8AB`）

```asm
; VA: 0xB5D8AB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5D8AB  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— buff_id：偏移 0，长度 4，线类型 u32（增益效果 ID）
0xB5D8E6  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "buff_id=" → 含义锚点：0xB5D9F9

; 字段 2 —— remain_sec：偏移 4，长度 4，线类型 u32（剩余秒数）
0xB5D926  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "remain_sec=" → 含义锚点：0xB5DA23

; 字段 3 —— remain_max：偏移 8，长度 4，线类型 u32（剩余上限）
0xB5D94A  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "remain_max=" → 含义锚点：0xB5DA48

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5D981
0xB5D981  push    <模块/错误码>
0xB5D981  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5DAAF
0xB5DAAF  mov     edx, [obj]
;       mov     edx, [edx+0x194h]
;       call    edx          ; vt[0x194]（3 实参）
```

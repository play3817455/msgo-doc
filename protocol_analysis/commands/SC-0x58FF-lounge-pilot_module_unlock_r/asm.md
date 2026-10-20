# 汇编证据 —— SC-0x58FF-lounge-pilot_module_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB62CE1`）

```asm
; VA: 0xB62CE1（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB62CE1  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB62D1C  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB62E02

; 字段 2 —— module_id：偏移 4，长度 4，线类型 u32（模块 ID）
0xB62D59  call    sub_B02DD0     ; u32
; 块内日志格式串 "module_id=" → 含义锚点：0xB62E27

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB62D69
0xB62D69  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB62D69  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB62E87
0xB62E87  mov     <reg>, [obj]; mov <reg>, [<reg>+0xE0h]
;       call    <reg>          ; vt[0xE0]（2 实参）
```

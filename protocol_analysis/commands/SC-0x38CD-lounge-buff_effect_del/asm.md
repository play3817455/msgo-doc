# 汇编证据 —— SC-0x38CD-lounge-buff_effect_del

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB5CE2D`）

```asm
; VA: 0xB5CE2D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5CE2D  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— buff_id：偏移 0，长度 4，线类型 u32（增益效果 ID）
0xB5CE68  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "buff_id=" → 含义锚点：0xB5CF12

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5CE9F
0xB5CE9F  push    <模块/错误码>
0xB5CE9F  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5CF6B
0xB5CF6B  mov     edx, [obj]
;       mov     edx, [edx+0x198h]
;       call    edx          ; vt[0x198]（1 实参）
```

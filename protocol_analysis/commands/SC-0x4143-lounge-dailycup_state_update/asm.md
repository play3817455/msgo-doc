# 汇编证据 —— SC-0x4143-lounge-dailycup_state_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB5D735`）

```asm
; VA: 0xB5D735（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5D735  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— state：偏移 0，长度 4，线类型 u32（每日杯状态）
0xB5D770  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "state=" → 含义锚点：0xB5D81A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5D7A7
0xB5D7A7  push    <模块/错误码>
0xB5D7A7  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5D873
0xB5D873  mov     edx, [obj]
;       mov     edx, [edx+0x544h]
;       call    edx          ; vt[0x544]（1 实参）
```

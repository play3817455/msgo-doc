# 汇编证据 —— SC-0x673D-lounge-pilot_comeback_process_stat

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xb64e4c`）

```asm
; VA: 0xb64e4c（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb64e4c  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— comeback_stat：偏移 0，长度 4，线类型 u32；读取点 VA 0xb64e85
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb64eaa
0xb64eaa  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb64f82（1 实参）
;       `vt[0x98]`
```

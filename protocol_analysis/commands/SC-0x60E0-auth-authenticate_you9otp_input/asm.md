# 汇编证据 —— SC-0x60E0-auth-authenticate_you9otp_input

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x15` @ `0xb044eb`）

```asm
; VA: 0xb044eb（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb044eb  push    0x15          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— otp_type：偏移 0，长度 4，线类型 u32；读取点 VA 0xb04518
; 字段 2 —— otp_matrix_code：偏移 4，长度 ?，线类型 bytes；读取点 VA 0xb04535
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb04545
0xb04545  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb04652（2 实参）
;       `vt[0x74]`
```

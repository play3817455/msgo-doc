# 汇编证据 —— SC-0x6735-battle-deliver_oration

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xb1c9f2`）

```asm
; VA: 0xb1c9f2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1c9f2  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— voice_id：偏移 0，长度 4，线类型 u32；读取点 VA 0xb1ca2b
; 字段 2 —— elap_msec：偏移 4，长度 4，线类型 u32；读取点 VA 0xb1ca6b
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1ca77
0xb1ca77  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb1cb9f（2 实参）
;       `vt[0x320]`
```

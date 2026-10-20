# 汇编证据 —— SC-0x632D-lounge-btlroom_deleted

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xb64884`）

```asm
; VA: 0xb64884（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb64884  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— room_id：偏移 0，长度 4，线类型 u32；读取点 VA 0xb648bd
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb648e5
0xb648e5  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb649c0（1 实参）
;       `vt[0x1A0]`
```

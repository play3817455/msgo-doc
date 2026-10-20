# 汇编证据 —— SC-0x7626-battle-netcafe_challenge_progress_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3C` @ `0xb1fe76`）

```asm
; VA: 0xb1fe76（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xb1fe76  push    0x3C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— netcafe_challenge_info：偏移 0，长度 13，线类型 struct<netcafe_challenge_info>；读取点 VA 0xb1feb6
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xb1fee3
0xb1fee3  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
```

## E4 去向（用途锚点）

```asm
; VA: 0xb20016（1 实参）
;       `vt[0x344]`
```

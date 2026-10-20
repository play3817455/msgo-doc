# 汇编证据 —— SC-0xC803-lounge-msma_energy_charge_deck_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B79112`）

```asm
; VA: B79112（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7913c|0xb7914b
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B79177
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xF7）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7924E —— `vt[0x298]`（1 实参）
```

# 汇编证据 —— SC-0xD3AA-lounge-msma_del

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7C6D4`）

```asm
; VA: B7C6D4（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— uniqid：偏移 0，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid=`））
;   0xb7c6fe|0xb7c70d
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7C739
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xCD）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7C82E —— `vt[0x240]`（2 实参）
```

# 汇编证据 —— SC-0xAA33-lounge-msma_sp_parts_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B716C1`）

```asm
; VA: B716C1（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B716FF
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   B71730|B7173F
; 字段 3 —— sp_parts_id：偏移 12，长度 4，线类型 u32（SP 部件 ID（日志串 `sp_parts_id=`））
;   B71763
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B71773
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x126）报错
```

## E4 去向（用途锚点）

```asm
; VA: B718D0 —— `vt[0x2F8]`（4 实参）
```

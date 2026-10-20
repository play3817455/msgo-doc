# 汇编证据 —— SC-0xA003-lounge-msma_color_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B6F353`）

```asm
; VA: B6F353（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6F391`、`B6F4A4`
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   `B6F3D1`、`B6F4D2`
; 字段 3 —— color：偏移 12，长度 4，线类型 u32（机体配色（日志串 `color=`））
;   `B6F3F5`、`B6F4F7`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6F405
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xF2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6F562 —— `vt[0x28C]`（4 实参）
```

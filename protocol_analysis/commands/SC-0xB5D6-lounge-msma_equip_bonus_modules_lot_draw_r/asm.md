# 汇编证据 —— SC-0xB5D6-lounge-msma_equip_bonus_modules_lot_draw_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `B748D4`）

```asm
; VA: B748D4（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x18
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B74912
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   B74943|B74952
; 字段 3 —— eq_bonus_modules_lot：偏移 12，长度 12，线类型 array<u32,3>（抽选出的加成模块 ID（日志串 `eq_bonus_modules_lot={...}`，3 项））
;   B74967|B74978|B7498A
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B749A5
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xE3）报错
```

## E4 去向（用途锚点）

```asm
; VA: B74B3B —— `vt[0x270]`（4 实参）
```

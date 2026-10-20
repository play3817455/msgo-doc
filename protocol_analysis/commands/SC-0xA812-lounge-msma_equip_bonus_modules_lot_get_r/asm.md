# 汇编证据 —— SC-0xA812-lounge-msma_equip_bonus_modules_lot_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `B7117C`）

```asm
; VA: B7117C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x18
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B711BA`、`B712F8`
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   `B711FA`、`B71326`
; 字段 3 —— eq_bonus_modules_lot：偏移 12，长度 12，线类型 struct（装备加成模块抽选结果（日志 `eq_bonus_modules_lot={...}`；定长 12B））
;   `B7120F`、`B71226`、`B71341`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B71253
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xE1）报错
```

## E4 去向（用途锚点）

```asm
; VA: B713ED —— `vt[0x26C]`（4 实参）
```

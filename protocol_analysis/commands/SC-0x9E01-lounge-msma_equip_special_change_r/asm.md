# 汇编证据 —— SC-0x9E01-lounge-msma_equip_special_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B6EC95`）

```asm
; VA: B6EC95（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6ECD3`、`B6EDE6`
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`；读原语 `sub_B06200`））
;   `B6ED13`、`B6EE14`
; 字段 3 —— item_id：偏移 12，长度 4，线类型 u32（特殊装备道具 ID（日志串 `item_id=`））
;   `B6ED37`、`B6EE39`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6ED47
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xDB）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6EEA4 —— `vt[0x260]`（4 实参）
```

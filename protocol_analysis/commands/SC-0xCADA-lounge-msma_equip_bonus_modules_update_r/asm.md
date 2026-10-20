# 汇编证据 —— SC-0xCADA-lounge-msma_equip_bonus_modules_update_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B7A855`）

```asm
; VA: B7A855（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7a87f|0xb7a88e
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   0xb7a8bf|0xb7a8ce
; 字段 3 —— eq_bonus_modules：偏移 12，长度 4，线类型 u32（装备奖励模块（固定 1 个 `cmp edi,1`@`B7A908`；日志串 `eq_bonus_modules={`））
;   0xb7a8e3|0xb7a8f6
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7A923
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xDF）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7AA89 —— `vt[0x268]`（4 实参）
```

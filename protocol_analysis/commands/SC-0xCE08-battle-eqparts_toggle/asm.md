# 汇编证据 —— SC-0xCE08-battle-eqparts_toggle

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `B2B9B3`）

```asm
; VA: B2B9B3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   0xb2b9dd|0xb2b9ec
; 字段 2 —— group_id：偏移 2，长度 4，线类型 u32（分组 ID（日志串 `group_id=`））
;   0xb2ba1d|0xb2ba2c
; 字段 3 —— toggle：偏移 6，长度 2，线类型 u16（开关值（日志串 `toggle=`））
;   0xb2ba41|0xb2ba50
; 字段 4 —— reason：偏移 8，长度 1，线类型 u8（原因（日志串 `reason=`））
;   0xb2ba65|0xb2ba74
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2BA88
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xA4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2BC13 —— `vt[0x210]`（4 实参）
```

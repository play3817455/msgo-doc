# 汇编证据 —— SC-0xAC3D-battle-msma_change_team

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B28569`）

```asm
; VA: B28569（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8（新阵营（日志串 `team=`；顶层 1B 由 `movzx` ⇒ u8））
;   B285A7|B28766
; 字段 2 —— troops：偏移 1，长度 1，线类型 u8（部队编号（日志串 `troops=`））
;   B285E7|B2876E
; 字段 3 —— ent_id：偏移 2，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   B2860B|B28756
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2861B
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xC8）报错
```

## E4 去向（用途锚点）

```asm
; VA: B28774 —— `vt[0x274]`（3 实参）
```

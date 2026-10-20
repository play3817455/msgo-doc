# 汇编证据 —— SC-0xAA98-battle-combat_operation_end

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `B27580`）

```asm
; VA: B27580（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— support_type：偏移 0，长度 4，线类型 u32（支援类型（日志串 `support_type=`））
;   B275BE
; 字段 2 —— is_completed：偏移 4，长度 1，线类型 u8（是否完成（日志串 `is_completed=`；顶层 1B 由派发侧 `movzx` ⇒ u8））
;   B275FE|B2777B
; 字段 3 —— stg_arms_initiation_ms：偏移 5，长度 4，线类型 u32（武装展开发起毫秒（日志串 `stg_arms_initiation_ms=`））
;   B27622
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B27632
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xF2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B27788 —— `vt[0x2F0]`（3 实参）
```

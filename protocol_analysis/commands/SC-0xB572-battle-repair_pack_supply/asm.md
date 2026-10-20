# 汇编证据 —— SC-0xB572-battle-repair_pack_supply

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `B2971C`）

```asm
; VA: B2971C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x6
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— val：偏移 0，长度 4，线类型 u32（补给量（日志串 `val=`））
;   B2975A
; 字段 2 —— equip_idx：偏移 4，长度 2，线类型 u16（装备槽索引（日志串 `equip_idx=`））
;   B2979A
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B297AA
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xCC）报错
```

## E4 去向（用途锚点）

```asm
; VA: B298D0 —— `vt[0x280]`（2 实参）
```

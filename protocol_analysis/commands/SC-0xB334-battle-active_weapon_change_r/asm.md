# 汇编证据 —— SC-0xB334-battle-active_weapon_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B29233`）

```asm
; VA: B29233（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   B29271
; 字段 2 —— result：偏移 2，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B292AE
; 字段 3 —— equip_index：偏移 6，长度 1，线类型 u8（装备槽索引（日志串 `equip_index=`））
;   B292D2|B294BB
; 字段 4 —— equip_itemid：偏移 7，长度 4，线类型 u32（装备物品 ID（日志串 `equip_itemid=`））
;   B292F6|B294E1
; 字段 5 —— is_force：偏移 11，长度 1，线类型 u8（是否强制换装（日志串 `is_force=`））
;   B2931E|B294D2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B29332
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x70）报错
```

## E4 去向（用途锚点）

```asm
; VA: B294E7 —— `vt[0x19C]`（5 实参）
```

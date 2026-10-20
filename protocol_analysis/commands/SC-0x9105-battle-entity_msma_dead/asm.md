# 汇编证据 —— SC-0x9105-battle-entity_msma_dead

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C` @ `B23AF3`）

```asm
; VA: B23AF3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id_dead：偏移 0，长度 2，线类型 u16（死亡实体 ID（日志串 `ent_id_dead=`））
;   `B23B31`、`B23D54`
; 字段 2 —— world_id_kill：偏移 2，长度 4，线类型 u32（击杀者世界 ID（日志串 `world_id_kill=`））
;   `B23B6E`、`B23D7E`
; 字段 3 —— pilot_id_kill：偏移 6，长度 4，线类型 u32（击杀者驾驶员 ID（日志串 `pilot_id_kill=`））
;   `B23B92`、`B23DA8`
; 字段 4 —— decal_kill：偏移 10，长度 4，线类型 u32（击杀者贴花（日志串 `decal_kill=`））
;   `B23BB6`、`B23DD2`
; 字段 5 —— weapon_itemid：偏移 14，长度 4，线类型 u32（击杀武器道具 ID（日志串 `weapon_itemid=`））
;   `B23BDE`、`B23DFC`
; 字段 6 —— repair_wait_sec：偏移 18，长度 2，线类型 u16（复活等待秒（日志串 `repair_wait_sec=`））
;   `B23C06`、`B23E27`
; 字段 7 —— kill_streak_count：偏移 20，长度 2，线类型 u16（连杀计数（日志串 `kill_streak_count=`））
;   `B23C2E`、`B23E52`
; 字段 8 —— spbits：偏移 22，长度 4，线类型 u32（特殊位（日志串 `spbits=`））
;   `B23C56`、`B23E7C`
; 字段 9 —— is_resurrect：偏移 26，长度 1，线类型 u8（是否复活（日志串 `is_resurrect=`，字节打印器））
;   `B23C7E`、`B23EA4`
; 字段 10 —— is_extend_style_change_limit：偏移 27，长度 1，线类型 u8（是否放宽换装限制（日志串 `is_extend_style_change_limit=`））
;   `B23CA6`、`B23EC9`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B23CBA
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x58）报错
```

## E4 去向（用途锚点）

```asm
; VA: B23F68 —— `vt[0x160]`（10 实参）
```

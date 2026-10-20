# 汇编证据 —— SC-0xB514-lounge-clan_npclist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9C` @ `B7448A`）

```asm
; VA: B7448A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— id_num：偏移 0，长度 4，线类型 u32（NPC 列表 ID 条目数（上限 24））
;   B744BD|B744E9
; 字段 2 —— npclist_id：偏移 4，长度 4·n₁，线类型 array<u32,24>（NPC 列表 ID（日志串 `npclist_id={...}`））
;   B744FB|B7451B|B74527
; 字段 3 —— is_ex_num：偏移 var，长度 4，线类型 u32（扩展标志条目数（上限 24））
;   B7454F|B74563
; 字段 4 —— npclist_is_ex：偏移 var，长度 n₂，线类型 array<u8,24>（是否为扩展 NPC（日志串 `npclist_is_ex={...}`，十六进制打印））
;   B74576|B7458D
; 字段 5 —— unlock_num：偏移 var，长度 4，线类型 u32（解锁等级条目数（上限 24））
;   B745BC|B745E8
; 字段 6 —— npclist_unlock_lv：偏移 var，长度 n₃，线类型 array<u8,24>（解锁等级（日志串 `npclist_unlock_lv={...}`，十六进制打印））
;   B745F7|B7460E
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B74637
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1AD）报错
```

## E4 去向（用途锚点）

```asm
; VA: B74878 —— `vt[0x41C]`（6 实参）
```

# 汇编证据 —— SC-0xA39E-battle-msma_AI_change_movetype

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B25656`）

```asm
; VA: B25656（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x5
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
;   `B25694`、`B257A8`
; 字段 2 —— action_type：偏移 2，长度 1，线类型 u8（动作类型（日志串 `action_type=`，字节打印器））
;   `B256D4`、`B257D0`
; 字段 3 —— route_number：偏移 3，长度 2，线类型 u16（路线编号（日志串 `route_number=`））
;   `B256F8`、`B257F8`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B25708
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xC4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B25862 —— `vt[0x268]`（3 实参）
```

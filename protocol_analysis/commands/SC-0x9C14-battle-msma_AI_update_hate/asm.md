# 汇编证据 —— SC-0x9C14-battle-msma_AI_update_hate

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x32` @ `B24EAD`）

```asm
; VA: B24EAD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x32
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
;   `B24EEB`、`B250CA`
; 字段 2 —— ent_id_cnt：偏移 2，长度 4，线类型 u32（仇恨目标个数（上界 `cmp ebx,0Ah` @`B24F49` ⇒ ≤10））
;   `B24F1D`
; 字段 3 —— ent_id_ary：偏移 6，长度 2×N1，线类型 array<u16,N1>（仇恨目标实体 ID 列表（日志 `ent_id={...}`））
;   `B24F5B`、`B24F7B`、`B250E5`
; 字段 4 —— val_cnt：偏移 var，长度 4，线类型 u32（仇恨值个数（上界 `cmp …,0Ah` @`B24FBF` ⇒ ≤10））
;   `B24FAF`
; 字段 5 —— val_ary：偏移 var，长度 2×N2，线类型 array<u16,N2>（仇恨值列表（日志 `val={...}`））
;   `B24FDB`、`B24FFA`、`B25157`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2502A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xBD）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2521B —— `vt[0x254]`（5 实参）
```

## E5 补充证据

```asm
; 数组 1 预留：B24F5B  call sub_B05E40 ; 按 N1 推进，槽步进 2
; 数组 2 预留：B24FDB  call sub_B05E40 ; 按 N2 推进，槽步进 2
```

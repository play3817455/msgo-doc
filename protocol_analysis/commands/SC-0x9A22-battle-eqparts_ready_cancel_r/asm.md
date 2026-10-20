# 汇编证据 —— SC-0x9A22-battle-eqparts_ready_cancel_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B253BD`）

```asm
; VA: B253BD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B253FB`、`B25536`
; 字段 2 —— frame_count：偏移 4，长度 4，线类型 u32（帧计数（日志串 `frame_count=`））
;   `B2543B`、`B25560`
; 字段 3 —— AI_ent_id：偏移 8，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
;   `B2545F`、`B2558B`
; 字段 4 —— group_id：偏移 10，长度 2，线类型 u16（分组 ID（日志串 `group_id=`））
;   `B25483`、`B255B1`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B25497
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xA8）报错
```

## E4 去向（用途锚点）

```asm
; VA: B25621 —— `vt[0x218]`（4 实参）
```

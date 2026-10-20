# 汇编证据 —— SC-0xA959-battle-radar_captured_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `B272AC`）

```asm
; VA: B272AC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id_radar：偏移 0，长度 2，线类型 u16（占领雷达的实体 ID（日志串 `ent_id_radar=`））
;   B272EA
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B27316
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xB4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B273EF —— `vt[0x23C]`（1 实参）
```

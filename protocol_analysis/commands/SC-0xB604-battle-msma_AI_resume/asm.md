# 汇编证据 —— SC-0xB604-battle-msma_AI_resume

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `B29BFA`）

```asm
; VA: B29BFA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
;   B29C38
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B29C64
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xB9）报错
```

## E4 去向（用途锚点）

```asm
; VA: B29D3D —— `vt[0x250]`（1 实参）
```

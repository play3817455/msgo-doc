# 汇编证据 —— SC-0xB463-battle-msma_AI_install

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xAA` @ `B2951C`）

```asm
; VA: B2951C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xAA
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
;   B2955D
; 字段 2 —— AI：偏移 2，长度 168，线类型 struct（AI 参数结构体（跨度 168B；日志串 `AI=`））
;   B2958E|B2959D
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B295AD
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xB5）报错
```

## E4 去向（用途锚点）

```asm
; VA: B296D1 —— `vt[0x240]`（2 实参）
```

# 汇编证据 —— SC-0xCDE7-lounge-msma_adop_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A` @ `B7B76A`）

```asm
; VA: B7B76A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1A
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— adop_result：偏移 0，长度 2，线类型 u16（采纳结果（日志串 `adop_result=`））
;   0xb7b794|0xb7b7a3
; 字段 2 —— adop_uniq_msid：偏移 2，长度 8，线类型 u64（被采纳机体唯一 ID（日志串 `adop_uniq_msid=`））
;   0xb7b7d4|0xb7b7e3
; 字段 3 —— adop_get：偏移 10，长度 13，线类型 struct(16)（采纳获得内容（日志串 `adop_get=`；读取器 `sub_B43D90`））
;   0xb7b7f8|0xb7b807
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7B817
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x243）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7B974 —— `vt[0x578]`（4 实参）
```

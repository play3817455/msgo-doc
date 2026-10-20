# 汇编证据 —— SC-0xC0C4-lounge-deckcost_update_by_accum_point

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C` @ `B776B1`）

```asm
; VA: B776B1（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— userid：偏移 0，长度 4，线类型 u32（用户 ID（日志串 `userid=`））
;   0xb776db|0xb776ea
; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（机师 ID（日志串 `pilot_id=`））
;   0xb77718|0xb77727
; 字段 3 —— accum_point：偏移 8，长度 4，线类型 u32（累计点数（日志串 `accum_point=`））
;   0xb7773c|0xb7774b
; 字段 4 —— rank：偏移 12，长度 4，线类型 u32（名次（日志串 `rank=`））
;   0xb77760|0xb7776f
; 字段 5 —— base_accump：偏移 16，长度 4，线类型 u32（基础累计点（日志串 `base_accump=`））
;   0xb77788|0xb77797
; 字段 6 —— req_accump：偏移 20，长度 4，线类型 u32（所需累计点（日志串 `req_accump=`））
;   0xb777b0|0xb777bf
; 字段 7 —— deckcost：偏移 24，长度 4，线类型 u32（卡组 COST（日志串 `deckcost=`））
;   0xb777d8|0xb777e7
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B777FB
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x28）报错
```

## E4 去向（用途锚点）

```asm
; VA: B77A0E —— `vt[0xC0]`（7 实参）
```

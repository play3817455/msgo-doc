# 汇编证据 —— SC-0xC664-lounge-ranking_elite_pilot_get_page_light_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3B72` @ `B78BF5`）

```asm
; VA: B78BF5（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x3B72
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb78c1f|0xb78c2e
; 字段 2 —— order：偏移 4，长度 10，线类型 struct(10)（排序条件（日志串 `order=`；`sub_B46420` = 10B））
;   0xb78c5f|0xb78c6e
; 字段 3 —— ranking_num：偏移 14，长度 4，线类型 u32（名次条目数（上限 200））
;   0xb78c84|0xb78cb0
; 字段 4 —— ranking：偏移 18，长度 73n，线类型 array<rank_pilot_light,200>（精英机师排行榜（轻量版 日志串 `ranking={`））
;   0xb78cc2|0xb78cdf
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B78D0D
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x253）报错
```

## E4 去向（用途锚点）

```asm
; VA: B78EB9 —— `vt[0x598]`（4 实参）
```

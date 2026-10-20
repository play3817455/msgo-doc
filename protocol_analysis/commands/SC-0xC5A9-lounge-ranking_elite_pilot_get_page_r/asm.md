# 汇编证据 —— SC-0xC5A9-lounge-ranking_elite_pilot_get_page_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4E8B` @ `B786BE`）

```asm
; VA: B786BE（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4E8B
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb786e8|0xb786f7
; 字段 2 —— is_revoke：偏移 4，长度 4，线类型 u32（是否撤销（日志串 `is_revoke=`））
;   0xb78728|0xb78737
; 字段 3 —— order：偏移 8，长度 10，线类型 struct(10)（排序条件（日志串 `order=`；读取器 `sub_B46420` = 5×u16 = 10B））
;   0xb7874c|0xb7875b
; 字段 4 —— rankself：偏移 18，长度 8，线类型 u64（自身名次值（日志串 `rankself=`））
;   0xb78770|0xb7877f
; 字段 5 —— page_now：偏移 26，长度 4，线类型 u32（当前页（日志串 `page_now=`））
;   0xb78798|0xb787a7
; 字段 6 —— page_max：偏移 30，长度 4，线类型 u32（总页数（日志串 `page_max=`））
;   0xb787c0|0xb787cf
; 字段 7 —— ranking_num：偏移 34，长度 4，线类型 u32（名次条目数（上限 100））
;   0xb787e9|0xb78815
; 字段 8 —— ranking：偏移 38，长度 188n，线类型 array<rank_pilot,100>（精英机师排行榜（日志串 `ranking={`））
;   0xb78824|0xb7884a
; 字段 9 —— term_str：偏移 var，长度 Ls+1，线类型 bytes(≤65)（赛季/期间字符串（NUL 结尾 日志串 `term_str=`））
;   0xb78890
; 字段 10 —— term_rankerbattle：偏移 var，长度 4，线类型 u32（排位赛期间号（日志串 `term_rankerbattle=`））
;   0xb788a9|0xb788b8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B788CC
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x24D）报错
```

## E4 去向（用途锚点）

```asm
; VA: B78BAD —— `vt[0x588]`（10 实参）
```

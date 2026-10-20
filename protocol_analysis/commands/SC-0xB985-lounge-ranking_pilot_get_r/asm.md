# 汇编证据 —— SC-0xB985-lounge-ranking_pilot_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2A63` @ `B75BE4`）

```asm
; VA: B75BE4（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2A63
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B75C25
; 字段 2 —— is_revoke：偏移 4，长度 4，线类型 u32（是否撤销（日志串 `is_revoke=`））
;   B75C65
; 字段 3 —— order：偏移 8，长度 10，线类型 struct（排序方式（跨度 10B = 线长 10B；日志串 `order=`））
;   B75C7A|B75C89
; 字段 4 —— rankself：偏移 18，长度 40，线类型 struct（我的排名信息（跨度 40B = 线长 40B；日志串 `rankself=`））
;   B75C9E|B75CAD
; 字段 5 —— page_now：偏移 58，长度 4，线类型 u32（当前页（日志串 `page_now=`））
;   B75CD5
; 字段 6 —— page_max：偏移 62，长度 4，线类型 u32（最大页（日志串 `page_max=`））
;   B75CFD
; 字段 7 —— ranking_num：偏移 66，长度 4，线类型 u32（排行条目数（上限 100））
;   B75D17|B75D43
; 字段 8 —— ranking：偏移 70，长度 95·n₁，线类型 array<struct,104>（驾驶员排行列表（元素线长 95 / 槽步进 104；日志串 `ranking={...}`））
;   B75D52|B75D7A|B75D86
; 字段 9 —— toppilot_num：偏移 var，长度 4，线类型 u32（榜首条目数（上限 3））
;   B75DAE|B75DBE
; 字段 10 —— toppilots：偏移 var，长度 95·n₂，线类型 array<struct,104>（榜首驾驶员列表（元素线长 95 / 槽步进 104；日志串 `toppilots={...}`））
;   B75DD7|B75DFA|B75E06
; 字段 11 —— term_str：偏移 var，长度 变长(槽 65)，线类型 bytes(NUL 串)（赛季/期间名称串（日志串 `term_str="..."`））
;   B75E32|B75E2A
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B75E46
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1F2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7616B —— `vt[0x4AC]`（11 实参）
```

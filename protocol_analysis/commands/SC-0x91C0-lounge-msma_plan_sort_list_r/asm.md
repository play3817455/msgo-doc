# 汇编证据 —— SC-0x91C0-lounge-msma_plan_sort_list_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B6CA9C`）

```asm
; VA: B6CA9C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— sort_tm_sec：偏移 0，长度 4，线类型 u32（排序时间戳-秒（日志串 `sort_tm_sec=`））
;   `B6CADA`、`B6CC15`
; 字段 2 —— sort_tm_usec：偏移 4，长度 4，线类型 u32（排序时间戳-微秒（日志串 `sort_tm_usec=`））
;   `B6CB1A`、`B6CC3F`
; 字段 3 —— msma_sort_type：偏移 8，长度 4，线类型 u32（机体排序类型（日志串 `msma_sort_type=`））
;   `B6CB3E`、`B6CC69`
; 字段 4 —— msma_sort_order：偏移 12，长度 4，线类型 u32（机体排序方向（日志串 `msma_sort_order=`））
;   `B6CB62`、`B6CC8E`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6CB76
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xFD）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6CCFC —— `vt[0x2A0]`（4 实参）
```

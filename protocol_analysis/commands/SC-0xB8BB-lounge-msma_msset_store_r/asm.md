# 汇编证据 —— SC-0xB8BB-lounge-msma_msset_store_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x64` @ `B7545B`）

```asm
; VA: B7545B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x64
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B75499
; 字段 2 —— ms_set：偏移 4，长度 95，线类型 struct（机体套装存储数据（线长 95B；缓冲槽 96B；日志串 `ms_set=`））
;   B754CA|B754D9
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B754E9
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x12A）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7560B —— `vt[0x300]`（2 实参）
```

# 汇编证据 —— SC-0xBD77-lounge-msma_msset_del_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B76DBA`）

```asm
; VA: B76DBA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb76de4|0xb76df3
; 字段 2 —— deck_type：偏移 4，长度 2，线类型 u16（卡组类型（日志串 `deck_type=`））
;   0xb76e24|0xb76e33
; 字段 3 —— slot：偏移 6，长度 2，线类型 u16（槽位号（日志串 `slot=`））
;   0xb76e48|0xb76e57
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B76E67
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x12C）报错
```

## E4 去向（用途锚点）

```asm
; VA: B76FC0 —— `vt[0x304]`（3 实参）
```

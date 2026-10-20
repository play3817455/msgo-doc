# 汇编证据 —— SC-0xB718-lounge-storage_msma_extend_buy_ticket_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B74FA0`）

```asm
; VA: B74FA0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B74FDE
; 字段 2 —— slot_num：偏移 4，长度 4，线类型 u32（扩展后的机库槽位数（日志串 `slot_num=`））
;   B7501E
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7502E
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1F9）报错
```

## E4 去向（用途锚点）

```asm
; VA: B75152 —— `vt[0x4B8]`（2 实参）
```

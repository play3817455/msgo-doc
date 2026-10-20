# 汇编证据 —— SC-0xCFD2-lounge-result_add_inventory_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7BD86`）

```asm
; VA: B7BD86（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7bdb0|0xb7bdbf
; 字段 2 —— remain_count：偏移 4，长度 4，线类型 u32（剩余数量（日志串 `remain_count=`））
;   0xb7bdf0|0xb7bdff
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7BE0F
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1A4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7BF33 —— `vt[0x408]`（2 实参）
```

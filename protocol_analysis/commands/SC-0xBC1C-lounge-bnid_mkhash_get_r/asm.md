# 汇编证据 —— SC-0xBC1C-lounge-bnid_mkhash_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x404` @ `B7682D`）

```asm
; VA: B7682D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x404
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb76857|0xb76866
; 字段 2 —— mkhash：偏移 4，长度 L+1，线类型 bytes(≤1024)（BNID 机器哈希串（NUL 结尾 日志串 `mkhash="`））
;   0xb7689a
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B768C3
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x46）报错
```

## E4 去向（用途锚点）

```asm
; VA: B769D4 —— `vt[0x104]`（2 实参）
```

# 汇编证据 —— SC-0xAEAA-lounge-bnid_mkhash_get_for_tournament_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x404` @ `B724F2`）

```asm
; VA: B724F2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x404
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B72533
; 字段 2 —— mkhash：偏移 4，长度 变长(槽 1024)，线类型 bytes(NUL 串)（锦标赛用赛事哈希串（日志串 `mkhash="..."`））
;   B72567|B7255C
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B72590
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x48）报错
```

## E4 去向（用途锚点）

```asm
; VA: B726A1 —— `vt[0x108]`（2 实参）
```

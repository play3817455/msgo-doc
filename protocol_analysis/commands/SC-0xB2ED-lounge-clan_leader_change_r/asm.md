# 汇编证据 —— SC-0xB2ED-lounge-clan_leader_change_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `B73372`）

```asm
; VA: B73372（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B733B0
; 字段 2 —— pilot_id_new：偏移 4，长度 4，线类型 u32（新会长驾驶员 ID（日志串 `pilot_id_new=`））
;   B733F0
; 字段 3 —— clan_kind：偏移 8，长度 1，线类型 u8（公会类别（日志串 `clan_kind=`））
;   B73414|B7355E
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73424
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1C3）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7357A —— `vt[0x448]`（3 实参）
```

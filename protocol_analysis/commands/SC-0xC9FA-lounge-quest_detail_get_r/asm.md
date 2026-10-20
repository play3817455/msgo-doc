# 汇编证据 —— SC-0xC9FA-lounge-quest_detail_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x609` @ `B7A42E`）

```asm
; VA: B7A42E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x609
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7a458|0xb7a467
; 字段 2 —— quest_id：偏移 4，长度 4，线类型 u32（任务 ID（日志串 `quest_id=`））
;   0xb7a498|0xb7a4a7
; 字段 3 —— desc：偏移 8，长度 L+1，线类型 bytes(≤1537)（任务说明（NUL 结尾 日志串 `desc="`））
;   0xb7a4c2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7A4EE
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x184）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7A633 —— `vt[0x3C8]`（3 实参）
```

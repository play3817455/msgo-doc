# 汇编证据 —— SC-0xBF1F-lounge-pilot_rename_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2E` @ `B76FF7`）

```asm
; VA: B76FF7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2E
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb77021|0xb77030
; 字段 2 —— troops：偏移 4，长度 4，线类型 u32（部队（日志串 `troops=`））
;   0xb7705e|0xb7706d
; 字段 3 —— slot：偏移 8，长度 4，线类型 u32（槽位（日志串 `slot=`））
;   0xb77082|0xb77091
; 字段 4 —— pilot_id：偏移 12，长度 4，线类型 u32（机师 ID（日志串 `pilot_id=`））
;   0xb770a6|0xb770b5
; 字段 5 —— pilot_name：偏移 16，长度 L+1，线类型 bytes(≤25)（机师名（NUL 结尾 日志串 `pilot_name="`））
;   0xb770de
; 字段 6 —— request_status：偏移 var，长度 1，线类型 u8（改名申请状态（日志串 `request_status=`））
;   0xb7710c|0xb7711b
; 字段 7 —— pilot_rename_remaintime：偏移 var，长度 4，线类型 u32（改名剩余时间（日志串 `pilot_rename_remaintime=`））
;   0xb77130|0xb7713f
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7714F
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x12）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7736F —— `vt[0x8C]`（7 实参）
```

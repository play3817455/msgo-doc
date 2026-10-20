# 汇编证据 —— SC-0xC779-lounge-pilot_personal_emblem_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4C` @ `B79285`）

```asm
; VA: B79285（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb792af|0xb792be
; 字段 2 —— emblem_id：偏移 4，长度 4，线类型 u32（徽章 ID（日志串 `emblem_id=`））
;   0xb792ec|0xb792fb
; 字段 3 —— use_gp：偏移 8，长度 4，线类型 u32（消耗 GP（日志串 `use_gp=`））
;   0xb79310|0xb7931f
; 字段 4 —— hav_emblem：偏移 12，长度 64，线类型 array<u64,8>（已持有徽章列表（日志串 `hav_emblem={`））
;   0xb79334|0xb79346
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B79370
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x34）报错
```

## E4 去向（用途锚点）

```asm
; VA: B79533 —— `vt[0xDC]`（4 实参）
```

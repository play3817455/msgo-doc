# 汇编证据 —— SC-0xCCDF-lounge-xwar_booking_option_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x22C` @ `B7B024`）

```asm
; VA: B7B024（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x22C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7b04e|0xb7b05d
; 字段 2 —— matching_type：偏移 4，长度 4，线类型 u32（匹配类型（日志串 `matching_type=`））
;   0xb7b08e|0xb7b09d
; 字段 3 —— matching_request_flag：偏移 8，长度 4，线类型 u32（匹配申请标志（日志串 `matching_request_flag=`））
;   0xb7b0b2|0xb7b0c1
; 字段 4 —— matching_battlerule_flag：偏移 12，长度 4，线类型 u32（匹配战斗规则标志（日志串 `matching_battlerule_flag=`））
;   0xb7b0d6|0xb7b0e5
; 字段 5 —— matching_extrule_flag：偏移 16，长度 4，线类型 u32（匹配扩展规则标志（日志串 `matching_extrule_flag=`））
;   0xb7b0fe|0xb7b10d
; 字段 6 —— ext_subrule：偏移 20，长度 20，线类型 struct(20)（扩展子规则（日志串 `ext_subrule=`；读取器 `sub_B456F0` = 2×u16 + 8×u16 = 20B））
;   0xb7b126|0xb7b135
; 字段 7 —— xwar_ext_rule：偏移 40，长度 514，线类型 struct(516)（XWar 扩展规则（日志串 `xwar_ext_rule=`；读取器 `sub_B08160` = u16 + 128×u32 = 514B））
;   0xb7b14e|0xb7b15d
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7B171
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xA4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7B386 —— `vt[0x1DC]`（7 实参）
```

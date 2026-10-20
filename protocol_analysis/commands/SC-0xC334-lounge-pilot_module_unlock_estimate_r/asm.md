# 汇编证据 —— SC-0xC334-lounge-pilot_module_unlock_estimate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B77A45`）

```asm
; VA: B77A45（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb77a6f|0xb77a7e
; 字段 2 —— price_gp：偏移 4，长度 4，线类型 u32（GP 价格（日志串 `price_gp=`））
;   0xb77aac|0xb77abb
; 字段 3 —— price_cp：偏移 8，长度 4，线类型 u32（CP 价格（日志串 `price_cp=`））
;   0xb77ad0|0xb77adf
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B77AEF
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x38）报错
```

## E4 去向（用途锚点）

```asm
; VA: B77C3E —— `vt[0xE4]`（3 实参）
```

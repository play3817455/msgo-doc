# 汇编证据 —— SC-0xB2C1-lounge-season_class_level_max_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B731F1`）

```asm
; VA: B731F1（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— sc_lv_max：偏移 0，长度 4，线类型 u32（赛季等级上限（日志串 `sc_lv_max=`））
;   B7322F
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7325B
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x251）报错
```

## E4 去向（用途锚点）

```asm
; VA: B73332 —— `vt[0x594]`（1 实参）
```

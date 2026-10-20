# 汇编证据 —— SC-0xB4B6-lounge-pilotcard_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1B0` @ `B73F1D`）

```asm
; VA: B73F1D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1B0
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B73F5E
; 字段 2 —— world_id：偏移 4，长度 4，线类型 u32（世界 ID（日志串 `world_id=`））
;   B73F9B
; 字段 3 —— pcard：偏移 8，长度 424，线类型 struct（驾驶员卡片数据块（跨度 424B；日志串 `pcard=`））
;   B73FB0|B73FBF
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73FCF
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x66）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7411C —— `vt[0x150]`（3 实参）
```

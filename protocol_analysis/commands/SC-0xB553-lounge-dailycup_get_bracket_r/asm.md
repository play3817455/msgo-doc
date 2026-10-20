# 汇编证据 —— SC-0xB553-lounge-dailycup_get_bracket_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xDC` @ `B74B70`）

```asm
; VA: B74B70（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xDC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B74BB1
; 字段 2 —— index：偏移 4，长度 4，线类型 u32（对阵表索引（日志串 `index=`））
;   B74BF1
; 字段 3 —— bracket：偏移 8，长度 212，线类型 struct（每日杯对阵表（跨度 212B；日志串 `bracket=`））
;   B74C06|B74C15
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B74C25
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x236）报错
```

## E4 去向（用途锚点）

```asm
; VA: B74D78 —— `vt[0x55C]`（3 实参）
```

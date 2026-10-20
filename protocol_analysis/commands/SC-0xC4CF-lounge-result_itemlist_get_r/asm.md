# 汇编证据 —— SC-0xC4CF-lounge-result_itemlist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1D0` @ `B78243`）

```asm
; VA: B78243（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1D0
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ritem_num：偏移 0，长度 4，线类型 u32（物品条目数（上限 23））
;   0xb7826e|0xb7829a
; 字段 2 —— ritem：偏移 4，长度 8n，线类型 array<item_info,23>（结算物品列表（日志串 `ritem={`））
;   0xb782a9|0xb782ca
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B782F8
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1A0）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7843D —— `vt[0x400]`（2 实参）
```

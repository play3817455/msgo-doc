# 汇编证据 —— SC-0xC8AF-lounge-itemcode_input_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9E` @ `B79870`）

```asm
; VA: B79870（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9E
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7989a|0xb798a9
; 字段 2 —— id_type_num：偏移 4，长度 4，线类型 u32（ID 类型个数（上限 5））
;   0xb798db|0xb79907
; 字段 3 —— id_type：偏移 8，长度 5，线类型 array<u8,5>（ID 类型列表（日志串 `id_type={`））
;   0xb79919|0xb79933
; 字段 4 —— itemid_num：偏移 13，长度 4，线类型 u32（物品个数（上限 5））
;   0xb79962|0xb79976
; 字段 5 —— itemid：偏移 17，长度 20，线类型 array<u32,5>（物品 ID 列表（日志串 `itemid={`））
;   0xb79989|0xb799aa
; 字段 6 —— amount_num：偏移 37，长度 4，线类型 u32（数量个数（上限 5））
;   0xb799de|0xb799f2
; 字段 7 —— amount：偏移 41，长度 20，线类型 array<u32,5>（数量列表（日志串 `amount={`））
;   0xb79a05|0xb79a22
; 字段 8 —— title：偏移 61，长度 L+1，线类型 bytes(≤97)（兑换码标题（NUL 结尾 日志串 `title="`））
;   0xb79a58
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B79A6C
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x199）报错
```

## E4 去向（用途锚点）

```asm
; VA: B79D1A —— `vt[0x3F0]`（8 实参）
```

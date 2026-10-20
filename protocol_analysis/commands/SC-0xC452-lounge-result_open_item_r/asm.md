# 汇编证据 —— SC-0xC452-lounge-result_open_item_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `B77C8C`）

```asm
; VA: B77C8C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb77cb6|0xb77cc5
; 字段 2 —— id_type：偏移 4，长度 1，线类型 u8（物品 ID 类型（日志串 `id_type=`；去向侧 `movzx` 取用 ⇒ 无符号））
;   0xb77cf6|0xb77d05
; 字段 3 —— itemid：偏移 5，长度 4，线类型 u32（物品 ID（日志串 `itemid=`））
;   0xb77d1a|0xb77d29
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B77D39
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x19C）报错
```

## E4 去向（用途锚点）

```asm
; VA: B77E8F —— `vt[0x3F8]`（3 实参）
```

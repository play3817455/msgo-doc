# 汇编证据 —— SC-0x994C-lounge-item_buyback_delete_term_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x41` @ `B6DE30`）

```asm
; VA: B6DE30（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x41
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— delete_term：偏移 0，长度 L+1，线类型 string（回购删除期限文本（日志串 `delete_term='...'`；NUL 结尾））
;   `B6DE60`、`B6DF0D`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6DE8C
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x14E）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6DF6F —— `vt[0x350]`（1 实参）
```

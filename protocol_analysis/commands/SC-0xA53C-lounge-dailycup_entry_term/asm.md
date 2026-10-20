# 汇编证据 —— SC-0xA53C-lounge-dailycup_entry_term

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B70334`）

```asm
; VA: B70334（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— term_sec：偏移 0，长度 4，线类型 u32（报名期限秒（日志串 `term_sec=`））
;   `B70372`、`B7041C`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7039E
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x231）报错
```

## E4 去向（用途锚点）

```asm
; VA: B70475 —— `vt[0x54C]`（1 实参）
```

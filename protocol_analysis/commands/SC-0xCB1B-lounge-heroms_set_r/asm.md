# 汇编证据 —— SC-0xCB1B-lounge-heroms_set_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x30` @ `B7ADDC`）

```asm
; VA: B7ADDC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x30
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— heroms_uniqid：偏移 0，长度 8，线类型 u64（英雄机唯一 ID（日志串 `heroms_uniqid=`））
;   0xb7ae06|0xb7ae15
; 字段 2 —— grants：偏移 8，长度 40，线类型 array<u32,10>（英雄机授予列表（日志串 `grants={`；固定 10 元素 无线上 count））
;   0xb7ae46|0xb7ae57
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7AE84
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x240）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7AFE7 —— `vt[0x570]`（3 实参）
```

# 汇编证据 —— SC-0xCBC6-lounge-gacha_lineup_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x648` @ `B7AB31`）

```asm
; VA: B7AB31（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x648
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7ab5b|0xb7ab6a
; 字段 2 —— quantity_num：偏移 4，长度 4，线类型 u32（扭蛋阵容条目数（上限 200））
;   0xb7ab9c|0xb7abc8
; 字段 3 —— quantity：偏移 8，长度 6n，线类型 array<gacha_lineup,200>（扭蛋阵容列表（日志串 `quantity={`））
;   0xb7abda|0xb7abfb
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7AC29
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x18D）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7ADA2 —— `vt[0x3D8]`（3 实参）
```

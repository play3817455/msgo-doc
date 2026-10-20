# 汇编证据 —— SC-0xA832-lounge-msma_add

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA74` @ `B70CBA`）

```asm
; VA: B70CBA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xA74
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ms：偏移 0，长度 303，线类型 struct<ms_lounge>（机体数据块（线长 303B = 读取器 `sub_B43570` 整函数展开；结构跨度 312B；日志串 `ms=`））
;   B70CEC|B70CFB
; 字段 2 —— unlockw_num：偏移 var，长度 4，线类型 u32（解锁武器数量（上限 30））
;   B70D2D|B70D59
; 字段 3 —— unlockw：偏移 var，长度 30·n₁，线类型 array<struct,30>（解锁武器列表（元素线长 30 / 槽步进 32））
;   B70D6B|B70D8B|B70D97
; 字段 4 —— equip_num：偏移 var，长度 4，线类型 u32（装备编成数量（上限 7））
;   B70DBF|B70DD3
; 字段 5 —— equip_set：偏移 var，长度 121·n₂，线类型 array<struct,121>（装备编成列表（元素线长 121 / 槽步进 128；读取器 `sub_B43C50` = 8+2+12+4+4+40+4+4+43））
;   B70DE6|B70E0A|B70E16
; 字段 6 —— adop_num：偏移 var，长度 4，线类型 u32（采纳列表数量（上限 31））
;   B70E41|B70E55
; 字段 7 —— adop_list：偏移 var，长度 13·n₃，线类型 array<struct,13>（采纳列表（元素线长 13 / 槽步进 16））
;   B70E68|B70E8A|B70E96
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B70EB8
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xCB）报错
```

## E4 去向（用途锚点）

```asm
; VA: B71147 —— `vt[0x238]`（7 实参）
```

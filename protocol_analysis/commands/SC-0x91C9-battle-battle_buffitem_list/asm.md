# 汇编证据 —— SC-0x91C9-battle-battle_buffitem_list

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE0` @ `B249FD`）

```asm
; VA: B249FD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xE0
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— buffitem：偏移 0，长度 6×14=84，线类型 array<struct,14>（战斗增益道具列表（14 元定长；日志 `buffitem={itemid=,is_used=,is_usable=}`））
;   `B24A2F`、`B24A46`、`B24B49`
; 字段 2 —— buffitem_ex：偏移 var，长度 6×14=84，线类型 array<struct,14>（战斗增益道具附加列表（14 元定长；日志 `buffitem_ex={...}`））
;   `B24A78`、`B24A89`、`B24BAB`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B24AB6
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x10D）报错
```

## E4 去向（用途锚点）

```asm
; VA: B24C4B —— `vt[0x338]`（2 实参）
```

## E5 补充证据

```asm
; 预留：B24A2F / B24A78  call sub_B06140   ; 各推进 0x70(=112) = 14 × 8
; 元素：B24A46 / B24A89  call sub_B07E70   ; u32+u8+u8 = 6B
```

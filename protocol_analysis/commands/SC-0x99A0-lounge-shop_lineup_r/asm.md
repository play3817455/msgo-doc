# 汇编证据 —— SC-0x99A0-lounge-shop_lineup_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2EE9` @ `B6E18B`）

```asm
; VA: B6E18B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2EE9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6E1CC`、`B6E34A`
; 字段 2 —— id_type：偏移 4，长度 1，线类型 u8（道具 ID 类型（日志串 `id_type=`，字节打印器））
;   `B6E20C`、`B6E372`
; 字段 3 —— count：偏移 5，长度 4，线类型 u32（列表元素个数（上界检查 `cmp ebx,1F4h` @`B6E24E` ⇒ ≤500））
;   `B6E222`
; 字段 4 —— item_list：偏移 9，长度 23N，线类型 array<struct,N>（商店陈列列表（日志 `item_list={shopitem_id,gp_x01,gp_x10,cp_x01,cp_x10,bit_eff,stock}`））
;   `B6E260`、`B6E27D`、`B6E38F`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6E2AB
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x177）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6E452 —— `vt[0x3A8]`（4 实参）
```

## E5 补充证据

```asm
; 数组预留：B6E260  call sub_B416C0  ; 按 count 推进，槽步进 0x18(=24)
; 元素读取：B6E27D  call sub_B458A0  ; u32×5+u8+u16 = 23B
; 循环步进：B6E289  add [var_2C48],18h ; B6E291 cmp edi,ebx
```

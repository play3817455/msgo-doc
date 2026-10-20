# 汇编证据 —— SC-0x9193-lounge-result_item_fullopen_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x12C` @ `B6C8CA`）

```asm
; VA: B6C8CA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x12C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— item_list：偏移 0，长度 8×15=120，线类型 array<struct,15>（开启结果道具列表（15 元定长；日志 `ritem={id_type=,itemid=,is_itmbox=,amount=}`））
;   `B6C8FC`、`B6C90D`、`B6C9CD`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6C93A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x19E）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6CA67 —— `vt[0x3FC]`（1 实参）
```

## E5 补充证据

```asm
; 数组预留：B6C8FC  call sub_B41760   ; 整块推进 0x12C(=300) = 15 × 20
; 元素读取：B6C90D  call sub_B45350   ; u8+u32+u8+u16 = 8B
; 循环：B6C91C  add ebx,14h ; B6C91F cmp edi,0Fh ; B6C922 jb 0xB6C907
```

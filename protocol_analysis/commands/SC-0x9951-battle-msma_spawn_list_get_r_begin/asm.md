# 汇编证据 —— SC-0x9951-battle-msma_spawn_list_get_r_begin

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B24C7D`）

```asm
; VA: B24C7D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— spawn1st_post：偏移 0，长度 4，线类型 u32（首位投放点（日志串 `spawn1st_post=`））
;   `B24CBB`、`B24DA1`
; 字段 2 —— is_1st：偏移 4，长度 4，线类型 u32（是否首个（日志串 `is_1st=`））
;   `B24CF8`、`B24DC6`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B24D08
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x47）报错
```

## E4 去向（用途锚点）

```asm
; VA: B24E26 —— `vt[0x12C]`（2 实参）
```

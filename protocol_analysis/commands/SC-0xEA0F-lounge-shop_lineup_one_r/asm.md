# 汇编证据 —— SC-0xEA0F-lounge-shop_lineup_one_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1d` @ `0xB845DF`）

```asm
; VA: 0xB845DF（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB845DF  push    0x1d          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB8461A  ...     ; 读点（窗口内第 1 个读事件）
0xB84747  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— id_type：线类型 u8，线长 1
0xB8465A  ...     ; 读点（窗口内第 2 个读事件）
0xB8476F  push    offset aid_type     ; 日志格式串锚点

; 字段 3 —— item：线类型 struct<item>，线长 23
0xB8467E  ...     ; 读点（窗口内第 3 个读事件）
0xB84790  push    offset aitem     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB846AA
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB8481E
; mov edx, [client]
; mov edx, [edx+3ACh]
; call edx          ; vt[0x3AC]（2 实参）
```

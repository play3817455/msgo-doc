# 汇编证据 —— SC-0xF66B-lounge-gacha_exec_w_buy_ticket_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x115` @ `0xB87202`）

```asm
; VA: 0xB87202（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB87202  push    0x115          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB87240  ...     ; 读点（窗口内第 1 个读事件）
0xB873EF  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— gacha_id：线类型 u32，线长 4
0xB87280  ...     ; 读点（窗口内第 2 个读事件）
0xB87419  push    offset agacha_id     ; 日志格式串锚点

; 字段 3 —— prize_count：线类型 u32，线长 4
0xB87296  ...     ; 读点（窗口内第 3 个读事件）

; 字段 4 —— prize：线类型 array<prize,11>，线长 264
0xB872FA  ...     ; 读点（窗口内第 4 个读事件）
0xB87434  push    offset aprize     ; 日志格式串锚点

; 字段 5 —— n_last1B：线类型 u8，线长 1
0xB8733C  ...     ; 读点（窗口内第 5 个读事件）
0xB874B9  push    offset an_last1B     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB87350
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB8752D
; mov edx, [client]
; mov edx, [edx+3E4h]
; call edx          ; vt[0x3E4]（5 实参）
```

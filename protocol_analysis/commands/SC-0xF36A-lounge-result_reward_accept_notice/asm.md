# 汇编证据 —— SC-0xF36A-lounge-result_reward_accept_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB869DE`）

```asm
; VA: 0xB869DE（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB869DE  push    0x8          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— item_id：线类型 u32，线长 4
0xB86A19  ...     ; 读点（窗口内第 1 个读事件）
0xB86B08  push    offset aitem_id     ; 日志格式串锚点

; 字段 2 —— amount：线类型 u32，线长 4
0xB86A59  ...     ; 读点（窗口内第 2 个读事件）
0xB86B2D  push    offset aamount     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB86A69
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86B8D
; mov edx, [client]
; mov edx, [edx+40Ch]
; call edx          ; vt[0x40C]（2 实参）
```

# 汇编证据 —— SC-0xF0CA-lounge-chat_whisper_up_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xd6` @ `0xB860B1`）

```asm
; VA: 0xB860B1（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB860B1  push    0xd6          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB860EF  ...     ; 读点（窗口内第 1 个读事件）
0xB86211  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— to_pilot_id：线类型 u32，线长 4
0xB8612C  ...     ; 读点（窗口内第 2 个读事件）
0xB8623B  push    offset ato_pilot_id     ; 日志格式串锚点

; 字段 3 —— to_pilot_name：线类型 str，线长 25
0xB86151  ...     ; 读点（窗口内第 3 个读事件）
0xB86268  push    offset ato_pilot_name     ; 日志格式串锚点

; 字段 4 —— msg：线类型 str，线长 181
0xB86168  ...     ; 读点（窗口内第 4 个读事件）
0xB8629B  push    offset amsg     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB86178
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB86310
; mov edx, [client]
; mov edx, [edx+11Ch]
; call edx          ; vt[0x11C]（4 实参）
```

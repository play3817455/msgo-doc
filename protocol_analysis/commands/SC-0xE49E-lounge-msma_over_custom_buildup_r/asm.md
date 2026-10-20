# 汇编证据 —— SC-0xE49E-lounge-msma_over_custom_buildup_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3c` @ `0xB83847`）

```asm
; VA: 0xB83847（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB83847  push    0x3c          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB83882  ...     ; 读点（窗口内第 1 个读事件）
0xB839D5  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— uniq_msid：线类型 u64，线长 8
0xB838C2  ...     ; 读点（窗口内第 2 个读事件）
0xB839FF  push    offset auniq_msid     ; 日志格式串锚点

; 字段 3 —— buildup_cnt：线类型 u32，线长 4
0xB83902  ...     ; 读点（窗口内第 3 个读事件）
0xB83A29  push    offset abuildup_cnt     ; 日志格式串锚点

; 字段 4 —— buildup_info：线类型 struct<buildup_info>，线长 42
0xB83926  ...     ; 读点（窗口内第 4 个读事件）
0xB83A4C  push    offset abuildup_info     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB83936
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB83ABE
; mov edx, [client]
; mov edx, [edx+5BCh]
; call edx          ; vt[0x5BC]（5 实参）
```

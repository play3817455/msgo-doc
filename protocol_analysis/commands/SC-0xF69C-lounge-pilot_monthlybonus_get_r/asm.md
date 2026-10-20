# 汇编证据 —— SC-0xF69C-lounge-pilot_monthlybonus_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x52` @ `0xB87562`）

```asm
; VA: 0xB87562（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB87562  push    0x52          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB8759D  ...     ; 读点（窗口内第 1 个读事件）
0xB8772D  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— archive：线类型 u8，线长 1
0xB875DA  ...     ; 读点（窗口内第 2 个读事件）
0xB87755  push    offset aarchive     ; 日志格式串锚点

; 字段 3 —— holding_id：线类型 u32，线长 4
0xB875FE  ...     ; 读点（窗口内第 3 个读事件）
0xB87781  push    offset aholding_id     ; 日志格式串锚点

; 字段 4 —— holding_term：线类型 str，线长 65
0xB87623  ...     ; 读点（窗口内第 4 个读事件）
0xB877AE  push    offset aholding_term     ; 日志格式串锚点

; 字段 5 —— logincnt：线类型 u32，线长 4
0xB87660  ...     ; 读点（窗口内第 5 个读事件）
0xB877E3  push    offset alogincnt     ; 日志格式串锚点

; 字段 6 —— xwarcnt：线类型 u32，线长 4
0xB87684  ...     ; 读点（窗口内第 6 个读事件）
0xB87808  push    offset axwarcnt     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB87694
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB87883
; mov edx, [client]
; mov edx, [edx+188h]
; call edx          ; vt[0x188]（6 实参）
```

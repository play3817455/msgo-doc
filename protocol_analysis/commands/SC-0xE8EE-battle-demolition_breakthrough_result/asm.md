# 汇编证据 —— SC-0xE8EE-battle-demolition_breakthrough_result

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB2F43C`）

```asm
; VA: 0xB2F43C（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2F43C  push    0x5          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— group_id：线类型 u32，线长 4
0xB2F477  ...     ; 读点（窗口内第 1 个读事件）
0xB2F566  push    offset agroup_id     ; 日志格式串锚点

; 字段 2 —— is_succcess：线类型 u8，线长 1
0xB2F4B7  ...     ; 读点（窗口内第 2 个读事件）
0xB2F589  push    offset ais_succcess     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2F4C7
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2F5EC
; mov edx, [client]
; mov edx, [edx+34Ch]
; call edx          ; vt[0x34C]（2 实参）
```

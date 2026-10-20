# 汇编证据 —— SC-0xE31F-battle-roomlobby_pilot_leave_appeal

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口（**零负载**：无 `vt[0x78]` 缓冲申请）

```asm
; 无 push IMM + call <分配器> 指纹
```

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何读取原语调用）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2E0A1
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2E17D
; mov edx, [client]
; mov edx, [edx+84h]
; call edx          ; vt[0x84]（0 实参）
```

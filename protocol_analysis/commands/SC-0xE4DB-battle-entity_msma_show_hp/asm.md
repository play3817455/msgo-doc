# 汇编证据 —— SC-0xE4DB-battle-entity_msma_show_hp

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6c` @ `0xB2E8DD`）

```asm
; VA: 0xB2E8DD（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB2E8DD  push    0x6c          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id_num：线类型 u32，线长 4
0xB2E90A  ...     ; 读点（窗口内第 1 个读事件）

; 字段 2 —— ent_id：线类型 u16[16]，线长 32
0xB2E96A  ...     ; 读点（窗口内第 2 个读事件）
0xB2EADA  push    offset aent_id     ; 日志格式串锚点

; 字段 3 —— hp_max_num：线类型 u32，线长 4
0xB2E99B  ...     ; 读点（窗口内第 3 个读事件）

; 字段 4 —— hp_max：线类型 u32[16]，线长 64
0xB2E9FA  ...     ; 读点（窗口内第 4 个读事件）
0xB2EB53  push    offset ahp_max     ; 日志格式串锚点

; 字段 5 —— gauge_max：线类型 u32，线长 4
0xB2EA39  ...     ; 读点（窗口内第 5 个读事件）
0xB2EBCA  push    offset agauge_max     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB2EA4D
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB2EC3E
; mov edx, [client]
; mov edx, [edx+178h]
; call edx          ; vt[0x178]（5 实参）
```

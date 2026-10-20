# 汇编证据 —— SC-0xE969-lounge-friend_xworld_search_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19dc` @ `0xB84856`）

```asm
; VA: 0xB84856（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB84856  push    0x19dc          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB84894  ...     ; 读点（窗口内第 1 个读事件）
0xB84A6A  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— pilot_id：线类型 u32，线长 4
0xB848D4  ...     ; 读点（窗口内第 2 个读事件）
0xB84A94  push    offset apilot_id     ; 日志格式串锚点

; 字段 3 —— connet_world_num：线类型 u32，线长 4
0xB848F8  ...     ; 读点（窗口内第 3 个读事件）
0xB84ABE  push    offset aconnet_world_num     ; 日志格式串锚点

; 字段 4 —— connet_world_id：线类型 u32，线长 4
0xB8491C  ...     ; 读点（窗口内第 4 个读事件）
0xB84AE8  push    offset aconnet_world_id     ; 日志格式串锚点

; 字段 5 —— friend_detail_num：线类型 u32，线长 4
0xB84936  ...     ; 读点（窗口内第 5 个读事件）

; 字段 6 —— friend_details：线类型 array<friend_detail,50>，线长 5650
0xB8499A  ...     ; 读点（窗口内第 6 个读事件）
0xB84B03  push    offset afriend_details     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB849CB
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB84BDC
; mov edx, [client]
; mov edx, [edx+370h]
; call edx          ; vt[0x370]（6 实参）
```

# 汇编证据 —— SC-0xE69C-lounge-clan_mshipbid_request_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x28` @ `0xB83F35`）

```asm
; VA: 0xB83F35（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB83F35  push    0x28          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：线类型 u32，线长 4
0xB83F70  ...     ; 读点（窗口内第 1 个读事件）
0xB840C4  push    offset aresult     ; 日志格式串锚点

; 字段 2 —— mclan_id：线类型 u32，线长 4
0xB83FB0  ...     ; 读点（窗口内第 2 个读事件）
0xB840EE  push    offset amclan_id     ; 日志格式串锚点

; 字段 3 —— mclan_name：线类型 str，线长 31
0xB83FD5  ...     ; 读点（窗口内第 3 个读事件）
0xB8411B  push    offset amclan_name     ; 日志格式串锚点

; 字段 4 —— clan_kind：线类型 u8，线长 1
0xB84015  ...     ; 读点（窗口内第 4 个读事件）
0xB84149  push    offset aclan_kind     ; 日志格式串锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB84025
; cmp <游标>, <报文末尾> ＋ jz/jnz（失败走错误出口）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB841B8
; mov edx, [client]
; mov edx, [edx+42Ch]
; call edx          ; vt[0x42C]（4 实参）
```

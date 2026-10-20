# 汇编证据 —— SC-0xCFF9-lounge-chat_clan_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD2` @ `B7BB47`）

```asm
; VA: B7BB47（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xD2
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（发言机师 ID（日志串 `pilot_id=`））
;   0xb7bb71|0xb7bb80
; 字段 2 —— pilot_name：偏移 4，长度 L1+1，线类型 bytes(≤25)（发言机师名（NUL 结尾 日志串 `pilot_name="`））
;   0xb7bbbe
; 字段 3 —— msg：偏移 var，长度 L2+1，线类型 bytes(≤181)（公会聊天内容（NUL 结尾 日志串 `msg="`））
;   0xb7bbd5
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7BBE5
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x50）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7BD4C —— `vt[0x118]`（3 实参）
```

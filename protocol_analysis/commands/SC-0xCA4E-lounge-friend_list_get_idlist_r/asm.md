# 汇编证据 —— SC-0xCA4E-lounge-friend_list_get_idlist_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x198` @ `B7A18D`）

```asm
; VA: B7A18D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x198
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7a1b7|0xb7a1c6
; 字段 2 —— friend_num：偏移 4，长度 4，线类型 u32（好友数（上限 100））
;   0xb7a1f8|0xb7a224
; 字段 3 —— friend_idlist：偏移 8，长度 4n，线类型 array<u32,100>（好友 ID 列表（日志串 `friend_idlist={`））
;   0xb7a233|0xb7a250
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7A27E
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x150）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7A3F1 —— `vt[0x354]`（3 实参）
```

# 汇编证据 —— SC-0x918E-lounge-debug_message

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB9` @ `B6C6C8`）

```asm
; VA: B6C6C8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xB9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— msg：偏移 0，长度 L+1，线类型 string（调试消息文本（日志串 `msg='...'`；NUL 结尾））
;   `B6C70A`、`B6C7FC`
; 字段 2 —— color：偏移 var，长度 4，线类型 u32（消息颜色（日志串 `color=`））
;   `B6C74A`、`B6C82C`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6C75A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x222）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6C88A —— `vt[0x520]`（2 实参）
```

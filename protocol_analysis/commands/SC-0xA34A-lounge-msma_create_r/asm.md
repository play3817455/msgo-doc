# 汇编证据 —— SC-0xA34A-lounge-msma_create_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `B6FCEC`）

```asm
; VA: B6FCEC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x14
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6FD2A`、`B6FE7D`
; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（新机体唯一 ID（日志串 `uniqid_ms=`））
;   `B6FD6A`、`B6FEA7`
; 字段 3 —— workres：偏移 12，长度 4，线类型 u32（工地资源（日志串 `workres=`））
;   `B6FDAA`、`B6FED1`
; 字段 4 —— mech_npcpict：偏移 16，长度 4，线类型 u32（机体 NPC 头像（日志串 `mech_npcpict=`））
;   `B6FDCE`、`B6FEF6`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6FDDE
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xFF）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6FF68 —— `vt[0x2A4]`（5 实参）
```

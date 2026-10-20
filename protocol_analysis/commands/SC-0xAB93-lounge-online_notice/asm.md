# 汇编证据 —— SC-0xAB93-lounge-online_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x25` @ `B71E69`）

```asm
; VA: B71E69（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x25
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（驾驶员 ID（日志串 `pilot_id=`））
;   B71EA7
; 字段 2 —— pilot_name：偏移 4，长度 变长(槽 25)，线类型 bytes(NUL 串)（驾驶员名（日志串 `pilot_name="..."`））
;   B71EE8|B71ED5
; 字段 3 —— count：偏移 var，长度 4，线类型 u32（在线人数（日志串 `count=`））
;   B71F28
; 字段 4 —— type：偏移 var，长度 4，线类型 u32（通知类型（日志串 `type=`））
;   B71F4C
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B71F5C
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x157）报错
```

## E4 去向（用途锚点）

```asm
; VA: B720EE —— `vt[0x364]`（4 实参）
```

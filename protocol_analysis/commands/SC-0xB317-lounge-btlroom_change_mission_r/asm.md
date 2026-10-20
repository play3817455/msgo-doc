# 汇编证据 —— SC-0xB317-lounge-btlroom_change_mission_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x52` @ `B7396D`）

```asm
; VA: B7396D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x52
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B739AB
; 字段 2 —— room_name：偏移 4，长度 变长(槽 73)，线类型 bytes(NUL 串)（房间名（日志串 `room_name="..."`））
;   B739EC|B739D9
; 字段 3 —— mission_id：偏移 var，长度 4，线类型 u32（新任务 ID（日志串 `mission_id=`））
;   B73A2C
; 字段 4 —— is_lock：偏移 var，长度 1，线类型 u8（房间是否锁定（日志串 `is_lock=`））
;   B73A50|B73BD2
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73A60
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x95）报错
```

## E4 去向（用途锚点）

```asm
; VA: B73BF3 —— `vt[0x1BC]`（4 实参）
```

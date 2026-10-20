# 汇编证据 —— SC-0xB099-lounge-xwar_booking_room_created

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B72F5C`）

```asm
; VA: B72F5C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— matching_type：偏移 0，长度 4，线类型 u32（匹配类型（日志串 `matching_type=`））
;   B72F9A
; 字段 2 —— room_id：偏移 4，长度 4，线类型 u32（房间 ID（日志串 `room_id=`））
;   B72FDA
; 字段 3 —— wait_sec：偏移 8，长度 4，线类型 u32（等待秒数（日志串 `wait_sec=`））
;   B72FFE
; 字段 4 —— mission_id：偏移 12，长度 4，线类型 u32（任务 ID（日志串 `mission_id=`））
;   B73022
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73036
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xAB）报错
```

## E4 去向（用途锚点）

```asm
; VA: B731BC —— `vt[0x1EC]`（4 实参）
```

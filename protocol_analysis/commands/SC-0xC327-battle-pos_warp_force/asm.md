# 汇编证据 —— SC-0xC327-battle-pos_warp_force

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B2AD06`）

```asm
; VA: B2AD06（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID（日志串 `ent_id=`））
;   0xb2ad30|0xb2ad3f
; 字段 2 —— pos_x：偏移 2，长度 2，线类型 u16（X 坐标（日志串 `pos_x=`））
;   0xb2ad6d|0xb2ad7c
; 字段 3 —— pos_y：偏移 4，长度 2，线类型 u16（Y 坐标（日志串 `pos_y=`））
;   0xb2ad91|0xb2ada0
; 字段 4 —— pos_z：偏移 6，长度 2，线类型 u16（Z 坐标（日志串 `pos_z=`））
;   0xb2adb5|0xb2adc4
; 字段 5 —— dir：偏移 8，长度 2，线类型 u16（朝向（日志串 `dir=`））
;   0xb2addd|0xb2adec
; 字段 6 —— reason：偏移 10，长度 2，线类型 u16（强制传送原因（日志串 `reason=`））
;   0xb2ae05|0xb2ae14
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2AE28
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x6A）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2B016 —— `vt[0x194]`（6 实参）
```

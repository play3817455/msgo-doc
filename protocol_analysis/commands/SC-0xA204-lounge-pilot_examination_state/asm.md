# 汇编证据 —— SC-0xA204-lounge-pilot_examination_state

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x48` @ `B6FAFC`）

```asm
; VA: B6FAFC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x48
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（驾驶员 ID（日志串 `pilot_id=`））
;   `B6FB3A`、`B6FC29`
; 字段 2 —— exam_state：偏移 4，长度 68，线类型 struct（考核状态结构体（日志串 `exam_state=`；claim == 线长 == 68））
;   `B6FB6B`、`B6FB7A`、`B6FC4C`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6FB8A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x229）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6FCAC —— `vt[0x534]`（2 实参）
```

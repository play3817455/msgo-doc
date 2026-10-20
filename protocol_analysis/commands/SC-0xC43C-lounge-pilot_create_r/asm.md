# 汇编证据 —— SC-0xC43C-lounge-pilot_create_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB4` @ `B77EC9`）

```asm
; VA: B77EC9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xB4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb77ef3|0xb77f02
; 字段 2 —— pilot：偏移 4，长度 159，线类型 struct(176)（新建机师详情（日志串 `pilot=` 打印器 `sub_B08AD0`））
;   0xb77f30|0xb77f3f
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B77F4F
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x10）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7806B —— `vt[0x88]`（2 实参）
```

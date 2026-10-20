# 汇编证据 —— SC-0xC29F-lounge-event_notice_add_dialog_show

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x30D` @ `B773F5`）

```asm
; VA: B773F5（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x30D
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— notice_id：偏移 0，长度 4，线类型 u32（公告 ID（日志串 `notice_id=`））
;   0xb7741f|0xb7742e
; 字段 2 —— url：偏移 4，长度 L+1，线类型 bytes(≤769)（公告跳转 URL（NUL 结尾 日志串 `url="`））
;   0xb77474
; 字段 3 —— width：偏移 var，长度 4，线类型 u32（对话框宽（日志串 `width=`））
;   0xb774a5|0xb774b4
; 字段 4 —— height：偏移 var，长度 4，线类型 u32（对话框高（日志串 `height=`））
;   0xb774c9|0xb774d8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B774E8
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x205）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7767A —— `vt[0x4DC]`（4 实参）
```

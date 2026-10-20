# 汇编证据 —— SC-0x9B54-lounge-block_list_add_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B6E492`）

```asm
; VA: B6E492（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6E4D0`、`B6E5BF`
; 字段 2 —— send_sysmes：偏移 4，长度 4，线类型 u32（是否发送系统消息（日志串 `send_sysmes=`））
;   `B6E510`、`B6E5E4`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6E520
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x163）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6E644 —— `vt[0x37C]`（2 实参）
```

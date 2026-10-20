# 汇编证据 —— SC-0x93AC-lounge-chat_dcteam_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD2` @ `B6D93F`）

```asm
; VA: B6D93F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xD2
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（发言驾驶员 ID（日志串 `pilot_id=`））
;   `B6D980`、`B6DA7E`
; 字段 2 —— pilot_name：偏移 4，长度 Ln+1，线类型 string（驾驶员名（日志串 `pilot_name='...'`；NUL 结尾，槽预算 25））
;   `B6D9BE`、`B6DAAB`
; 字段 3 —— msg：偏移 var，长度 Lm+1，线类型 string（部队频道消息文本（日志串 `msg='...'`；NUL 结尾，槽预算 181））
;   `B6D9D5`、`B6DADE`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6D9E5
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x57）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6DB4C —— `vt[0x128]`（3 实参）
```

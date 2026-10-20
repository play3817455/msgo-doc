# 汇编证据 —— SC-0x93EF-lounge-xwar_reward_accept_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B6D75B`）

```asm
; VA: B6D75B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— item_id：偏移 0，长度 4，线类型 u32（奖励道具 ID（日志串 `item_id=`））
;   `B6D799`、`B6D888`
; 字段 2 —— amount：偏移 4，长度 4，线类型 u32（奖励数量（日志串 `amount=`））
;   `B6D7D9`、`B6D8AD`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6D7E9
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xA2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6D90D —— `vt[0x1D8]`（2 实参）
```

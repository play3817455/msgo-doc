# 汇编证据 —— SC-0xA148-lounge-season_rankerbattle_replay_info

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2C` @ `B6F917`）

```asm
; VA: B6F917（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— replay_info：偏移 0，长度 38，线类型 struct（录像信息结构体（日志串 `replay_info=`；claim 40 / 线长 38））
;   `B6F946`、`B6F955`、`B6FA42`
; 字段 2 —— win_troops：偏移 38，长度 4，线类型 u32（胜利方部队（日志串 `win_troops=`））
;   `B6F995`、`B6FA69`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6F9A5
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x268）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6FAC7 —— `vt[0x5D4]`（2 实参）
```

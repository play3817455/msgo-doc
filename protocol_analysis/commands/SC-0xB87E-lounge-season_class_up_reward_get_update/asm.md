# 汇编证据 —— SC-0xB87E-lounge-season_class_up_reward_get_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2E` @ `B75640`）

```asm
; VA: B75640（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2E
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（驾驶员 ID（日志串 `pilot_id=`））
;   B7567E
; 字段 2 —— get_num：偏移 4，长度 4，线类型 u32（已领取条目数（上限 19））
;   B756B0|B756DC
; 字段 3 —— sc_lv_up_reward_get：偏移 8，长度 2·n，线类型 array<u16,19>（赛季等级提升奖励领取状态（日志串 `sc_lv_up_reward_get={...}`））
;   B756EB|B7570A|B75716
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B75738
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x250）报错
```

## E4 去向（用途锚点）

```asm
; VA: B758AD —— `vt[0x590]`（3 实参）
```

# 汇编证据 —— SC-0xACB0-battle-commander_get_pilotinfo_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `B282CD`）

```asm
; VA: B282CD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x7
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— target_member：偏移 0，长度 1，线类型 u8（目标队员编号（日志串 `target_member=`））
;   B2830B|B2852E
; 字段 2 —— target_ace：偏移 1，长度 2，线类型 u16（目标王牌编号（日志串 `target_ace=`））
;   B2834B|B2851E
; 字段 3 —— kill_cnt：偏移 3，长度 2，线类型 u16（击坠数（日志串 `kill_cnt=`））
;   B2836F|B2850E
; 字段 4 —— death_cnt：偏移 5，长度 2，线类型 u16（被击坠数（日志串 `death_cnt=`））
;   B28393
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B283A7
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xDA）报错
```

## E4 去向（用途锚点）

```asm
; VA: B28534 —— `vt[0x2A4]`（4 实参）
```

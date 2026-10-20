# 汇编证据 —— SC-0xA8F2-battle-weapon_hit_from_with_tumble

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `B26F5D`）

```asm
; VA: B26F5D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x10
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（受击实体 ID（日志串 `ent_id=`））
;   B26F9B
; 字段 2 —— hit_dir：偏移 2，长度 2，线类型 u16（受击方向（日志串 `hit_dir=`））
;   B26FDB
; 字段 3 —— spbits：偏移 4，长度 4，线类型 u32（特殊位标志（日志串 `spbits=`，十六进制打印））
;   B26FFF
; 字段 4 —— optbits：偏移 8，长度 4，线类型 u32（可选位标志（日志串 `optbits=`，十六进制打印））
;   B27023
; 字段 5 —— down_power：偏移 12，长度 2，线类型 u16（倒地冲击力（日志串 `down_power=`））
;   B2704B
; 字段 6 —— down_msec：偏移 14，长度 2，线类型 u16（倒地持续毫秒（日志串 `down_msec=`））
;   B27073
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B27087
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x9F）报错
```

## E4 去向（用途锚点）

```asm
; VA: B27277 —— `vt[0x1FC]`（6 实参）
```

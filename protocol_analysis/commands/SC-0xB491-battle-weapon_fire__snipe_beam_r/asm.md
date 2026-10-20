# 汇编证据 —— SC-0xB491-battle-weapon_fire__snipe_beam_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB` @ `B29905`）

```asm
; VA: B29905（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xB
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 4，线类型 u32（发射者实体 ID（日志串 `ent_id=`））
;   B29943
; 字段 2 —— target_x：偏移 4，长度 2，线类型 u16（目标 X（日志串 `target_x=`））
;   B29983
; 字段 3 —— target_y：偏移 6，长度 2，线类型 u16（目标 Y（日志串 `target_y=`））
;   B299A7
; 字段 4 —— target_z：偏移 8，长度 2，线类型 u16（目标 Z（日志串 `target_z=`））
;   B299CB
; 字段 5 —— begin1_end0：偏移 10，长度 1，线类型 u8（1=开火开始 / 0=结束（日志串 `begin1_end0=`））
;   B299F3|B29B98
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B29A07
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x89）报错
```

## E4 去向（用途锚点）

```asm
; VA: B29BC5 —— `vt[0x1C8]`（5 实参）
```

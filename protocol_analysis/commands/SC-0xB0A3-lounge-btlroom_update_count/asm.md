# 汇编证据 —— SC-0xB0A3-lounge-btlroom_update_count

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1400C` @ `B72B29`）

```asm
; VA: B72B29（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1400C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— room_num：偏移 0，长度 4，线类型 u32（房间数量（上限 10240））
;   B72B5C|B72B88
; 字段 2 —— room_ids：偏移 4，长度 4·n₁，线类型 array<u32,10240>（房间 ID 列表（日志串 `room_ids={...}`））
;   B72B9D|B72BBD|B72BC9
; 字段 3 —— eff_num：偏移 var，长度 4，线类型 u32（联邦方计数条目数（上限 10240））
;   B72BF1|B72C05
; 字段 4 —— count_effs：偏移 var，长度 2·n₂，线类型 array<u16,10240>（联邦方人数计数（日志串 `count_effs={...}`））
;   B72C1B|B72C3A|B72C46
; 字段 5 —— zeon_num：偏移 var，长度 4，线类型 u32（吉翁方计数条目数（上限 10240））
;   B72C6E|B72C82
; 字段 6 —— count_zeons：偏移 var，长度 2·n₃，线类型 array<u16,10240>（吉翁方人数计数（日志串 `count_zeons={...}`））
;   B72C98|B72CB5|B72CC1
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B72CE3
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x89）报错
```

## E4 去向（用途锚点）

```asm
; VA: B72F27 —— `vt[0x1A4]`（6 实参）
```

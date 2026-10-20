# 汇编证据 —— SC-0xA78D-battle-weapon_fire__funnel_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x51` @ `B2649D`）

```asm
; VA: B2649D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x51
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— from_ent_id：偏移 0，长度 4，线类型 u32（发射者实体 ID（日志串 `from_ent_id=`））
;   `B264DB`、`B26659`
; 字段 2 —— wslot_idx：偏移 4，长度 1，线类型 u8（武器槽序号（日志串 `wslot_idx=`，字节打印器））
;   `B2651B`、`B26681`
; 字段 3 —— fire_points_cnt：偏移 5，长度 4，线类型 u32（火力点个数（上界 `cmp ebx,0Ch` @`B2655D` ⇒ ≤12））
;   `B26531`
; 字段 4 —— fire_points：偏移 9，长度 6N，线类型 array<struct(3×u16),N>（火力点坐标列表（日志 `fire_points={x,y,z}`））
;   `B2656F`、`B2658C`、`B2669E`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B265BA
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x94）报错
```

## E4 去向（用途锚点）

```asm
; VA: B26761 —— `vt[0x1E0]`（4 实参）
```

## E5 补充证据

```asm
; 数组预留：B2656F  call sub_B05E70 ; 按 N 推进，槽步进 6
; 元素读取：B2658C  call sub_B07760 ; 3×u16 = 6B
```

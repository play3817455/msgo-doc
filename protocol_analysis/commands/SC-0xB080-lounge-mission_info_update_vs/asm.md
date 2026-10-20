# 汇编证据 —— SC-0xB080-lounge-mission_info_update_vs

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x40B` @ `B726D3`）

```asm
; VA: B726D3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x40B
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— exvs_num：偏移 0，长度 4，线类型 u32（exvs 任务 ID 数量（上限 128））
;   B72706|B7272F
; 字段 2 —— mission_ids_exvs：偏移 4，长度 4·n₁，线类型 array<u32,128>（参加演习(VS)的任务 ID 列表（日志串 `mission_ids_exvs={...}`））
;   B72741|B7275E|B7276A
; 字段 3 —— vslocal_num：偏移 var，长度 4，线类型 u32（vslocal 任务 ID 数量（上限 128））
;   B7278F|B727A3
; 字段 4 —— mission_ids_vslocal：偏移 var，长度 4·n₂，线类型 array<u32,128>（本地 VS 任务 ID 列表（日志串 `mission_ids_vslocal={...}`））
;   B727B9|B727D6|B727E2
; 字段 5 —— is_mission_vs_force_entry：偏移 var，长度 1，线类型 u8（是否强制进入 VS 任务（日志串 `is_mission_vs_force_entry=`））
;   B72815|B72AA1
; 字段 6 —— xwar_entry_is_freeze：偏移 var，长度 1，线类型 u8（XWAR 入场是否冻结（日志串 `xwar_entry_is_freeze=`））
;   B72852|B72AB1
; 字段 7 —— vswar_entry_is_freeze：偏移 var，长度 1，线类型 u8（VS 战入场是否冻结（日志串 `vswar_entry_is_freeze=`））
;   B72876|B72AB9
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B72886
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x5D）报错
```

## E4 去向（用途锚点）

```asm
; VA: B72ACF —— `vt[0x13C]`（7 实参）
```

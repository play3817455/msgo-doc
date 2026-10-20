# 汇编证据 —— SC-0xB43F-lounge-party_recruit_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x73A8` @ `B74151`）

```asm
; VA: B74151（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x73A8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— recruit_num：偏移 0，长度 4，线类型 u32（招募条目数（上限 200））
;   B74184|B741B0
; 字段 2 —— recruits：偏移 4，长度 80·n₁，线类型 array<struct,84>（招募列表（元素线长 80 / 槽步进 84；日志串 `recruits={...}`））
;   B741C2|B741DF|B741EB
; 字段 3 —— leader_num：偏移 var，长度 4，线类型 u32（队长条目数（上限 200））
;   B74213|B74223
; 字段 4 —— leaders：偏移 var，长度 52·n₂，线类型 array<struct,64>（队长列表（元素线长 52 / 槽步进 64；日志串 `leaders={...}`））
;   B7423F|B7425E|B7426A
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7428E
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xC2）报错
```

## E4 去向（用途锚点）

```asm
; VA: B74455 —— `vt[0x220]`（4 实参）
```

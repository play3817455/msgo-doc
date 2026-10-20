# 汇编证据 —— SC-0xD286-lounge-season_rankerbattle_entry_info

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7C15F`）

```asm
; VA: B7C15F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— reccode：偏移 0，长度 4，线类型 u32（报名码（日志串 `reccode=`））
;   0xb7c189|0xb7c198
; 字段 2 —— is_set：偏移 4，长度 4，线类型 u32（是否已设置（日志串 `is_set=`））
;   0xb7c1c9|0xb7c1d8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7C1E8
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x257）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7C30C —— `vt[0x5A8]`（2 实参）
```

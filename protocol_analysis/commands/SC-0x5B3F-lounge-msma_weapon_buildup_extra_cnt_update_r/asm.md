# 汇编证据 —— SC-0x5B3F-lounge-msma_weapon_buildup_extra_cnt_update_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE` @ `0xB63766`）

```asm
; VA: 0xB63766（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB63766  push    0xE          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB637A1  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB638B4

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB637E1  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB638E2

; 字段 3 —— weapon_buildup_extra_cnt：偏移 12，长度 2，线类型 u16（武器强化追加次数）
0xB63805  call    sub_B02DF0     ; u16
; 块内日志格式串 "weapon_buildup_extra_cnt=" → 含义锚点：0xB63908

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB63815
0xB63815  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB63815  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB63974
0xB63974  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2C8h]
;       call    <reg>          ; vt[0x2C8]（4 实参）
```

# 汇编证据 —— SC-0x548D-lounge-msma_equip_all_change_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x90` @ `0xB61446`）

```asm
; VA: 0xB61446（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB61446  push    0x90          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB61484  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB615D7

; 字段 2 —— uniqid_ms：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB614C4  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid_ms=" → 含义锚点：0xB61601

; 字段 3 —— equip_set：偏移 12，长度 121，线类型 struct<equip_set>（整份装备编成（claim 128 = 预留 `sub_B411D0` 槽步进 `0x80`；线长 121，读取器 `sub_B43C50`））
0xB61504  call    复合读取器（元素/结构体，见 notes.md）     ; struct<equip_set>
; 块内日志格式串 "equip_set=" → 含义锚点：0xB61629

; 字段 4 —— cost：偏移 133，长度 4，线类型 u32（当前机体 COST）
0xB61528  call    sub_B02DD0     ; u32
; 块内日志格式串 "cost=" → 含义锚点：0xB61650

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB61538
0xB61538  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB61538  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB616C0
0xB616C0  mov     <reg>, [obj]; mov <reg>, [<reg>+0x314h]
;       call    <reg>          ; vt[0x314]（5 实参）
```

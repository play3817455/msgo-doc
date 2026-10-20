# 汇编证据 —— SC-0x553F-battle-commander_support_gauge_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB1734A`）

```asm
; VA: 0xB1734A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1734A  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— gauge_val：偏移 0，长度 4，线类型 u32（支援槽值）
0xB17385  call    sub_B02DD0     ; u32
; 块内日志格式串 "gauge_val=" → 含义锚点：0xB17474

; 字段 2 —— no_complement：偏移 4，长度 1，线类型 u8（是否不补充）
0xB173C5  call    sub_B06230     ; u8
; 块内日志格式串 "no_complement=" → 含义锚点：0xB17497

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB173D5
0xB173D5  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB173D5  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB174FA
0xB174FA  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2B4h]
;       call    <reg>          ; vt[0x2B4]（2 实参）
```

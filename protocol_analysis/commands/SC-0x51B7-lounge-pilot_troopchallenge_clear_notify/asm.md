# 汇编证据 —— SC-0x51B7-lounge-pilot_troopchallenge_clear_notify

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB60456`）

```asm
; VA: 0xB60456（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB60456  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— challenge_info：偏移 0，长度 13，线类型 struct（部队挑战通关信息（claim 20 / 线长 13，读取器 `sub_B07540`））
0xB60482  call    复合读取器（元素/结构体，见 notes.md）     ; struct
; 块内日志格式串 "challenge_info=" → 含义锚点：0xB60533

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB604BA
0xB604BA  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB604BA  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB6058C
0xB6058C  mov     <reg>, [obj]; mov <reg>, [<reg>+0x17Ch]
;       call    <reg>          ; vt[0x17C]（1 实参）
```

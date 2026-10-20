# 汇编证据 —— SC-0x5A3D-lounge-activity_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x36A4` @ `0xB63526`）

```asm
; VA: 0xB63526（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB63526  push    0x36A4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— activity_count：偏移 0，长度 4，线类型 u32（活动条数（上限 `0x26`=38，`cmp ebx,26h`@`0xB63582`））
0xB63556  call    sub_B02DD0     ; u32
; 块内日志格式串 "activity_count=" → 含义锚点：0xB63672

; 字段 2 —— activity[]：偏移 4，长度 356，线类型 array<activity>（活动数组（元素线长 356 / 槽步进 `0x170`=368，预留 `sub_B41950`））
0xB63591  call    复合读取器（元素/结构体，见 notes.md）     ; array<activity>
; 块内日志格式串 "activity[]=" → 含义锚点：0xB63672

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB635DF
0xB635DF  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB635DF  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB6372E
0xB6372E  mov     <reg>, [obj]; mov <reg>, [<reg>+0x4E0h]
;       call    <reg>          ; vt[0x4E0]（2 实参）
```

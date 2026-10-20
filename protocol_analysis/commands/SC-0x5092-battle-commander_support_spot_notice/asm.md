# 汇编证据 —— SC-0x5092-battle-commander_support_spot_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x784` @ `0xB16D19`）

```asm
; VA: 0xB16D19（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB16D19  push    0x784          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— support_spot_count：偏移 0，长度 4，线类型 u32（支援地点数（上限 `0x1E`=30，`cmp ebx,1Eh`@`0xB16D75`））
0xB16D49  call    sub_B02DD0     ; u32
; 块内日志格式串 "support_spot_count=" → 含义锚点：0xB16E62

; 字段 2 —— support_spots[]：偏移 4，长度 37，线类型 array<support_spot>（支援地点数组（元素线长 37 / 槽步进 `0x40`=64，预留 `sub_B41AC0`））
0xB16D84  call    复合读取器（元素/结构体，见 notes.md）     ; array<support_spot>
; 块内日志格式串 "support_spots[]=" → 含义锚点：0xB16E62

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16DCF
0xB16DCF  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB16DCF  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB16F1B
0xB16F1B  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2ACh]
;       call    <reg>          ; vt[0x2AC]（2 实参）
```

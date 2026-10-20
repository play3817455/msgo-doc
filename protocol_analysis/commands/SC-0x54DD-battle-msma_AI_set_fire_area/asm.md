# 汇编证据 —— SC-0x54DD-battle-msma_AI_set_fire_area

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB17532`）

```asm
; VA: 0xB17532（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB17532  push    0x14          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID）
0xB1756D  call    sub_B02DF0     ; u16
; 块内日志格式串 "AI_ent_id=" → 含义锚点：0xB17799

; 字段 2 —— fire_sx：偏移 2，长度 2，线类型 u16（射击矩形起点 X）
0xB175AD  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_sx=" → 含义锚点：0xB177C4

; 字段 3 —— fire_sy：偏移 4，长度 2，线类型 u16（射击矩形起点 Y）
0xB175D1  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_sy=" → 含义锚点：0xB177EF

; 字段 4 —— fire_sz：偏移 6，长度 2，线类型 u16（射击矩形起点 Z）
0xB175F5  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_sz=" → 含义锚点：0xB1781A

; 字段 5 —— fire_ex：偏移 8，长度 2，线类型 u16（射击矩形终点 X）
0xB1761D  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_ex=" → 含义锚点：0xB17845

; 字段 6 —— fire_ey：偏移 10，长度 2，线类型 u16（射击矩形终点 Y）
0xB17645  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_ey=" → 含义锚点：0xB17870

; 字段 7 —— fire_ez：偏移 12，长度 2，线类型 u16（射击矩形终点 Z）
0xB1766D  call    sub_B02DF0     ; u16
; 块内日志格式串 "fire_ez=" → 含义锚点：0xB1789B

; 字段 8 —— end_x：偏移 14，长度 2，线类型 u16（终点 X）
0xB17695  call    sub_B02DF0     ; u16
; 块内日志格式串 "end_x=" → 含义锚点：0xB178C6

; 字段 9 —— end_y：偏移 16，长度 2，线类型 u16（终点 Y）
0xB176BD  call    sub_B02DF0     ; u16
; 块内日志格式串 "end_y=" → 含义锚点：0xB178F1

; 字段 10 —— end_z：偏移 18，长度 2，线类型 u16（终点 Z）
0xB176E5  call    sub_B02DF0     ; u16
; 块内日志格式串 "end_z=" → 含义锚点：0xB17917

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB176F9
0xB176F9  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB176F9  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB179BC
0xB179BC  mov     <reg>, [obj]; mov <reg>, [<reg>+0x260h]
;       call    <reg>          ; vt[0x260]（10 实参）
```

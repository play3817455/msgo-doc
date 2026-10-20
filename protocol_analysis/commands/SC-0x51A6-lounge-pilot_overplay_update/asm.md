# 汇编证据 —— SC-0x51A6-lounge-pilot_overplay_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB5FF2F`）

```asm
; VA: 0xB5FF2F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5FF2F  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— type：偏移 0，长度 1，线类型 u8（超玩类型）
0xB5FF6A  call    sub_B06230     ; u8
; 块内日志格式串 "type=" → 含义锚点：0xB6004E

; 字段 2 —— accum_playtime：偏移 1，长度 4，线类型 u32（累计游玩时长）
0xB5FFA7  call    sub_B02DD0     ; u32
; 块内日志格式串 "accum_playtime=" → 含义锚点：0xB60075

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5FFB7
0xB5FFB7  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB5FFB7  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB600D6
0xB600D6  mov     <reg>, [obj]; mov <reg>, [<reg>+0xA8h]
;       call    <reg>          ; vt[0xA8]（2 实参）
```

# 汇编证据 —— SC-0x5913-battle-roomlobby_roommaster_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB18838`）

```asm
; VA: 0xB18838（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18838  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— world_id：偏移 0，长度 4，线类型 u32（世界 ID）
0xB18873  call    sub_B02DD0     ; u32
; 块内日志格式串 "world_id=" → 含义锚点：0xB18959

; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（新房主飞行员 ID）
0xB188B0  call    sub_B02DD0     ; u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB1897E

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB188C0
0xB188C0  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB188C0  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB189DE
0xB189DE  mov     <reg>, [obj]; mov <reg>, [<reg>+0x90h]
;       call    <reg>          ; vt[0x90]（2 实参）
```

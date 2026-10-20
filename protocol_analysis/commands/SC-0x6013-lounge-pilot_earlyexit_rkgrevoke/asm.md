# 汇编证据 —— SC-0x6013-lounge-pilot_earlyexit_rkgrevoke

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB64516`）

```asm
; VA: 0xB64516（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB64516  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— remain_cnt：偏移 0，长度 4，线类型 u32（剩余次数）
0xB64551  call    sub_B02DD0     ; u32
; 块内日志格式串 "remain_cnt=" → 含义锚点：0xB645FB

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB6457D
0xB6457D  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB6457D  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB64654
0xB64654  mov     <reg>, [obj]; mov <reg>, [<reg>+0x528h]
;       call    <reg>          ; vt[0x528]（1 实参）
```

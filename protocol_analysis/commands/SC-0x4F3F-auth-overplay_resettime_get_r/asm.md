# 汇编证据 —— SC-0x4F3F-auth-overplay_resettime_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB0436C`）

```asm
; VA: 0xB0436C（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB0436C  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— reset_sec：偏移 0，长度 4，线类型 u32（超玩重置秒数）
0xB04394  call    sub_B02DD0     ; u32
; 块内日志格式串 "reset_sec=" → 含义锚点：0xB04442

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB043CA
0xB043CA  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB043CA  call    sub_B03020     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB044A0
0xB044A0  mov     <reg>, [obj]; mov <reg>, [<reg>+0x84h]
;       call    <reg>          ; vt[0x84]（1 实参）
```

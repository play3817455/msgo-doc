# 汇编证据 —— SC-0x5E97-lounge-msma_energy_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB63DC9`）

```asm
; VA: 0xB63DC9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB63DC9  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— uniqid：偏移 0，长度 8，线类型 u64（机体唯一 ID（u64））
0xB63E04  call    sub_B06200     ; u64
; 块内日志格式串 "uniqid=" → 含义锚点：0xB63EF3

; 字段 2 —— energy_now：偏移 8，长度 4，线类型 u32（当前能量）
0xB63E44  call    sub_B02DD0     ; u32
; 块内日志格式串 "energy_now=" → 含义锚点：0xB63F18

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB63E54
0xB63E54  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB63E54  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB63F7C
0xB63F7C  mov     <reg>, [obj]; mov <reg>, [<reg>+0x290h]
;       call    <reg>          ; vt[0x290]（3 实参）
```

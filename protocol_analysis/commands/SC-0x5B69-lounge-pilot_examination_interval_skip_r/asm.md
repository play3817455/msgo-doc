# 汇编证据 —— SC-0x5B69-lounge-pilot_examination_interval_skip_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB63C53`）

```asm
; VA: 0xB63C53（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB63C53  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB63C8E  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB63D38

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB63CBA
0xB63CBA  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB63CBA  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB63D91
0xB63D91  mov     <reg>, [obj]; mov <reg>, [<reg>+0x538h]
;       call    <reg>          ; vt[0x538]（1 实参）
```

# 汇编证据 —— SC-0x52A2-lounge-clan_subleader_set_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD` @ `0xB60F56`）

```asm
; VA: 0xB60F56（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB60F56  push    0xD          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB60F91  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB610CC

; 字段 2 —— pilot_id_sub：偏移 4，长度 4，线类型 u32（副队长飞行员 ID）
0xB60FD1  call    sub_B02DD0     ; u32
; 块内日志格式串 "pilot_id_sub=" → 含义锚点：0xB610F6

; 字段 3 —— is_set：偏移 8，长度 4，线类型 u32（是否设置（线宽 **u32**，`sub_B02DD0`@`0xB60FF5`））
0xB60FF5  call    sub_B02DD0     ; u32
; 块内日志格式串 "is_set=" → 含义锚点：0xB61120

; 字段 4 —— clan_kind：偏移 12，长度 1，线类型 u8（战队种类）
0xB61019  call    sub_B06230     ; u8
; 块内日志格式串 "clan_kind=" → 含义锚点：0xB61143

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB6102D
0xB6102D  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB6102D  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB611B4
0xB611B4  mov     <reg>, [obj]; mov <reg>, [<reg>+0x43Ch]
;       call    <reg>          ; vt[0x43C]（4 实参）
```

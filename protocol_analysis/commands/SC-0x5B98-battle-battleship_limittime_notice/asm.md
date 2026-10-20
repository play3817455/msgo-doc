# 汇编证据 —— SC-0x5B98-battle-battleship_limittime_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB18BAC`）

```asm
; VA: 0xB18BAC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18BAC  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— to_ent_id：偏移 0，长度 2，线类型 u16（目标实体 ID）
0xB18BE7  call    sub_B02DF0     ; u16
; 块内日志格式串 "to_ent_id=" → 含义锚点：0xB18CD7

; 字段 2 —— limit_msec：偏移 2，长度 4，线类型 u32（时限毫秒）
0xB18C27  call    sub_B02DD0     ; u32
; 块内日志格式串 "limit_msec=" → 含义锚点：0xB18CFC

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB18C37
0xB18C37  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB18C37  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB18D5D
0xB18D5D  mov     <reg>, [obj]; mov <reg>, [<reg>+0x30Ch]
;       call    <reg>          ; vt[0x30C]（2 实参）
```

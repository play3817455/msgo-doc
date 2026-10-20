# 汇编证据 —— SC-0x5157-battle-access_state

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB170CB`）

```asm
; VA: 0xB170CB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB170CB  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— to_ent_id：偏移 0，长度 2，线类型 u16（目标实体 ID）
0xB17106  call    sub_B02DF0     ; u16
; 块内日志格式串 "to_ent_id=" → 含义锚点：0xB1721A

; 字段 2 —— from_ent_id：偏移 2，长度 2，线类型 u16（来源实体 ID）
0xB17146  call    sub_B02DF0     ; u16
; 块内日志格式串 "from_ent_id=" → 含义锚点：0xB17245

; 字段 3 —— remain_msec：偏移 4，长度 4，线类型 u32（剩余毫秒）
0xB1716A  call    sub_B02DD0     ; u32
; 块内日志格式串 "remain_msec=" → 含义锚点：0xB1726A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1717A
0xB1717A  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB1717A  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB172D3
0xB172D3  mov     <reg>, [obj]; mov <reg>, [<reg>+0x284h]
;       call    <reg>          ; vt[0x284]（3 实参）
```

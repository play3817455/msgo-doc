# 汇编证据 —— SC-0x5C4F-battle-entity_msma_detach

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB18A3A`）

```asm
; VA: 0xB18A3A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18A3A  push    0x2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB18A75  call    sub_B02DF0     ; u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB18B1A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB18A9E
0xB18A9E  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB18A9E  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB18B74
0xB18B74  mov     <reg>, [obj]; mov <reg>, [<reg>+0x16Ch]
;       call    <reg>          ; vt[0x16C]（1 实参）
```

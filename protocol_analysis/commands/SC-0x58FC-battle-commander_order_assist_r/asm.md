# 汇编证据 —— SC-0x58FC-battle-commander_order_assist_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1` @ `0xB18379`）

```asm
; VA: 0xB18379（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18379  push    0x1          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— type：偏移 0，长度 1，线类型 u8（指令协助类型）
0xB183B4  call    sub_B06230     ; u8
; 块内日志格式串 "type=" → 含义锚点：0xB1845C

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB183E0
0xB183E0  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB183E0  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB184B8
0xB184B8  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2A8h]
;       call    <reg>          ; vt[0x2A8]（1 实参）
```

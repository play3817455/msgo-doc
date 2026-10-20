# 汇编证据 —— SC-0x4FCE-battle-msma_AI_move_stuckescape_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB1688E`）

```asm
; VA: 0xB1688E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1688E  push    0x2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID）
0xB168C9  call    sub_B02DF0     ; u16
; 块内日志格式串 "AI_ent_id=" → 含义锚点：0xB16974

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB168F5
0xB168F5  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB168F5  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB169CE
0xB169CE  mov     <reg>, [obj]; mov <reg>, [<reg>+0x270h]
;       call    <reg>          ; vt[0x270]（1 实参）
```

# 汇编证据 —— SC-0x5080-battle-msma_AI_suspend

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2` @ `0xB16F53`）

```asm
; VA: 0xB16F53（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB16F53  push    0x2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— AI_ent_id：偏移 0，长度 2，线类型 u16（AI 实体 ID）
0xB16F8E  call    sub_B02DF0     ; u16
; 块内日志格式串 "AI_ent_id=" → 含义锚点：0xB17039

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16FBA
0xB16FBA  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB16FBA  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB17093
0xB17093  mov     <reg>, [obj]; mov <reg>, [<reg>+0x24Ch]
;       call    <reg>          ; vt[0x24C]（1 实参）
```

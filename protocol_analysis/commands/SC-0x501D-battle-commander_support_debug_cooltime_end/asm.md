# 汇编证据 —— SC-0x501D-battle-commander_support_debug_cooltime_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口（零负载，无缓冲申请）

```asm
; 处理块 `0xB16BC7`..`0xB16D04` 内**没有** `mov edx,[eax+78h]` + `push IMM; call edx`
```

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何读取原语调用）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16BDF
0xB16BDF  cmp     游标, 末尾      ; 入口闭合校验（失败直接 retn）
```

## E4 去向（用途锚点）

```asm
; VA: 0xB16CC1
0xB16CC1  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2D8h]
;       call    <reg>          ; vt[0x2D8]（0 实参）
```

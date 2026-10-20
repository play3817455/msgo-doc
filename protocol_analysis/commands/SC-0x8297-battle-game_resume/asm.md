# 汇编证据 —— SC-0x8297-battle-game_resume

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 零负载（无解码缓冲申请）

```asm
; 块内不存在 `mov edx,[eax+78h]` + `push IMM; call edx` 形态
; 入口直接进入「游标 == 报文末尾」校验（见 E3）
```

## E2 字段读取序列（按线序）

```asm
; （零负载：块内无任何字段读取）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B21826
B21826  cmp     cursor, end      ; 入口闭合校验（不等则走 vt[0x64] 报错）
```

## E4 去向（用途锚点）

```asm
; VA: B218FA —— `vt[0x104]`（0 实参）
B218FA  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x104h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; 0xB21822  mov     ebx, [esp+1B3Ch+var_1B28]        ; 游标
; 0xB21826  cmp     ebx, [esp+1B3Ch+var_1B24]        ; 报文末尾
; 0xB2182C  jz      short loc_B21851                ; 相等 → 业务
; 0xB2182E  mov     eax, [esi]
; 0xB21830  mov     edx, [eax+64h]                  ; vt[0x64] 报错
; 0xB218F8  mov     edx, [esi]
; 0xB218FA  mov     eax, [edx+104h]                 ; vt[0x104]（去向，0 实参）
; 0xB21902  call    eax
```

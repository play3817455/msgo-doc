# 汇编证据 —— SC-0x80DC-lounge-second_chance_free_play_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1` @ `B69379`）

```asm
; VA: B69379（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69379  push    0x1          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— remain：偏移 0，长度 1，线类型 u8（剩余免费游玩次数（日志串 `remain=`））
B693B4  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B6945C → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B693E0
B693E0  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B694AF —— `vt[0x4C8]`（1 实参）
B694AF  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x4C8h]
;       call    <reg>
```

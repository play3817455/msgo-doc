# 汇编证据 —— SC-0x8944-lounge-chat_troops_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD2` @ `B6AEA9`）

```asm
; VA: B6AEA9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6AEA9  push    0xD2          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（发送者飞行员 ID（日志串 `pilot_id=`））
B6AEE7  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6AFE5 → 含义锚点

; 字段 2 —— pilot_name：偏移 4，长度 25，线类型 str（发送者飞行员名（日志串 `pilot_name="`））
B6AF25  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B6B012 → 含义锚点

; 字段 3 —— msg：偏移 29，长度 181，线类型 str（聊天内容（日志串 `msg="`））
B6AF3C  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B6B045 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6AF4C
B6AF4C  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6B0A2 —— `vt[0x114]`（3 实参）
B6B0A2  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x114h]
;       call    <reg>
```

# 汇编证据 —— SC-0x84CB-lounge-friend_list_mail_accept_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B6A60B`）

```asm
; VA: B6A60B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6A60B  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6A646  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6A735 → 含义锚点

; 字段 2 —— to_pilotid：偏移 4，长度 4，线类型 u32（目标飞行员 ID（日志串 `to_pilotid=`））
B6A686  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6A75A → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6A696
B6A696  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6A7AE —— `vt[0x35C]`（2 实参）
B6A7AE  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x35Ch]
;       call    <reg>
```

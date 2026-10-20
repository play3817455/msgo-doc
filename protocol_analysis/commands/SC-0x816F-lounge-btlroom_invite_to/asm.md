# 汇编证据 —— SC-0x816F-lounge-btlroom_invite_to

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3B` @ `B69779`）

```asm
; VA: B69779（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69779  push    0x3B          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— room_id：偏移 0，长度 4，线类型 u32（战斗房间 ID（日志串 `room_id=`））
B697B4  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69935 → 含义锚点

; 字段 2 —— room_pw：偏移 4，长度 25，线类型 str（房间密码（日志串 `room_pw="`））
B697F5  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B69962 → 含义锚点

; 字段 3 —— pilot_id：偏移 29，长度 4，线类型 u32（被邀请飞行员 ID（日志串 `pilot_id=`））
B69835  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69997 → 含义锚点

; 字段 4 —— pilot_name：偏移 33，长度 25，线类型 str（被邀请飞行员名（日志串 `pilot_name="`））
B6985A  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B699C4 → 含义锚点

; 字段 5 —— is_gm_camera：偏移 58，长度 1，线类型 u8（是否 GM 镜头（日志串 `is_gm_camera=`））
B69882  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B699F2 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B69896
B69896  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B69A49 —— `vt[0x1B8]`（5 实参）
B69A49  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x1B8h]
;       call    <reg>
```

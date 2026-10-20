# 汇编证据 —— SC-0x5C61-lounge-party_invite_to

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x25` @ `0xB639C2`）

```asm
; VA: 0xB639C2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB639C2  push    0x25          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— party_id：偏移 0，长度 4，线类型 u32（队伍 ID）
0xB639FD  call    sub_B02DD0     ; u32
; 块内日志格式串 "party_id=" → 含义锚点：0xB63B28

; 字段 2 —— channel_id：偏移 4，长度 4，线类型 u32（频道 ID）
0xB63A3D  call    sub_B02DD0     ; u32
; 块内日志格式串 "channel_id=" → 含义锚点：0xB63B52

; 字段 3 —— pilot_id：偏移 8，长度 4，线类型 u32（被邀请飞行员 ID）
0xB63A61  call    sub_B02DD0     ; u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB63B7C

; 字段 4 —— pilot_name：偏移 12，长度 25，线类型 str（被邀请飞行员名（槽位预算 `0x19`=25））
0xB63A79  call    sub_B02BA0     ; str
; 块内日志格式串 "pilot_name=" → 含义锚点：0xB63BA4

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB63AA5
0xB63AA5  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB63AA5  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB63C1B
0xB63C1B  mov     <reg>, [obj]; mov <reg>, [<reg>+0x200h]
;       call    <reg>          ; vt[0x200]（4 实参）
```

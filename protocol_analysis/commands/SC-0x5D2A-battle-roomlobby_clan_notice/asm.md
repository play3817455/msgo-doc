# 汇编证据 —— SC-0x5D2A-battle-roomlobby_clan_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x28` @ `0xB18D92`）

```asm
; VA: 0xB18D92（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18D92  push    0x28          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— team：偏移 0，长度 1，线类型 u8（队伍）
0xB18DCD  call    sub_B06230     ; u8
; 块内日志格式串 "team=" → 含义锚点：0xB18F83

; 字段 2 —— troops：偏移 1，长度 1，线类型 u8（部队）
0xB18E0A  call    sub_B06230     ; u8
; 块内日志格式串 "troops=" → 含义锚点：0xB18FAD

; 字段 3 —— clan_id：偏移 2，长度 4，线类型 u32（战队 ID）
0xB18E2E  call    sub_B02DD0     ; u32
; 块内日志格式串 "clan_id=" → 含义锚点：0xB18FD9

; 字段 4 —— clan_name：偏移 6，长度 31，线类型 str（战队名（槽位预算 `0x1F`=31））
0xB18E53  call    sub_B02BA0     ; str
; 块内日志格式串 "clan_name=" → 含义锚点：0xB19006

; 字段 5 —— clan_emb_base：偏移 37，长度 1，线类型 u8（战队徽章底）
0xB18E90  call    sub_B06230     ; u8
; 块内日志格式串 "clan_emb_base=" → 含义锚点：0xB19039

; 字段 6 —— clan_emb_parts1：偏移 38，长度 1，线类型 u8（战队徽章部件 1）
0xB18EB4  call    sub_B06230     ; u8
; 块内日志格式串 "clan_emb_parts1=" → 含义锚点：0xB19063

; 字段 7 —— clan_emb_parts2：偏移 39，长度 1，线类型 u8（战队徽章部件 2）
0xB18ED8  call    sub_B06230     ; u8
; 块内日志格式串 "clan_emb_parts2=" → 含义锚点：0xB19088

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB18EEC
0xB18EEC  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB18EEC  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB19110
0xB19110  mov     <reg>, [obj]; mov <reg>, [<reg>+0x9Ch]
;       call    <reg>          ; vt[0x9C]（7 实参）
```

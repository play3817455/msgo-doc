# 汇编证据 —— SC-0x30A9-battle-roomlobby_ban_vote_result

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x30` @ `0xB139C8`）

```asm
; VA: 0xB139C8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB139C8  push    0x30          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— state：偏移 0，长度 4，线类型 u32（封禁投票结果（房间状态））
0xB13A03  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "state=" → 含义锚点：0xB13B71

; 字段 2 —— vote_count：偏移 4，长度 20，线类型 u32[5]（投票计数（固定 5 元素，逐席位））
0xB13A46  call    复合读取器（元素/结构体，见 notes.md）     ; 读 u32[5]
; 块内日志格式串 "vote_count=" → 含义锚点：0xB13B8C

; 字段 3 —— ban_msma_id：偏移 24，长度 20，线类型 u32[5]（被禁机体 ID（固定 5 元素））
0xB13A86  call    复合读取器（元素/结构体，见 notes.md）     ; 读 u32[5]
; 块内日志格式串 "ban_msma_id=" → 含义锚点：0xB13BEE

; 字段 4 —— member_count：偏移 44，长度 4，线类型 u32（成员数）
0xB13AC4  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "member_count=" → 含义锚点：0xB13C58

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB13AF9
0xB13AF9  push    <模块/错误码>
0xB13AF9  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB13CC6
0xB13CC6  mov     edx, [obj]
;       mov     edx, [edx+0xC0h]
;       call    edx          ; vt[0xC0]（4 实参）
```

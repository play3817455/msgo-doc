# 汇编证据 —— SC-0x5383-lounge-btlroom_enter_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xBA` @ `0xB616F8`）

```asm
; VA: 0xB616F8（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB616F8  push    0xBA          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB61736  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB618CF

; 字段 2 —— matching_type：偏移 4，长度 4，线类型 u32（匹配类型）
0xB61776  call    sub_B02DD0     ; u32
; 块内日志格式串 "matching_type=" → 含义锚点：0xB618F9

; 字段 3 —— battlesv_host：偏移 8，长度 129，线类型 str（对战服务器主机（槽位预算 `0x81`=129））
0xB617A0  call    sub_B02BA0     ; str
; 块内日志格式串 "battlesv_host=" → 含义锚点：0xB61926

; 字段 4 —— battlesv_port：偏移 137，长度 4，线类型 u32（对战服务器端口）
0xB617E0  call    sub_B02DD0     ; u32
; 块内日志格式串 "battlesv_port=" → 含义锚点：0xB6195B

; 字段 5 —— room_id：偏移 141，长度 4，线类型 u32（房间 ID）
0xB61804  call    sub_B02DD0     ; u32
; 块内日志格式串 "room_id=" → 含义锚点：0xB61985

; 字段 6 —— otp_battle：偏移 145，长度 41，线类型 str（对战 OTP（槽位预算 `0x29`=41））
0xB6181C  call    sub_B02BA0     ; str
; 块内日志格式串 "otp_battle=" → 含义锚点：0xB619AD

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB61830
0xB61830  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB61830  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB61A30
0xB61A30  mov     <reg>, [obj]; mov <reg>, [<reg>+0x1B0h]
;       call    <reg>          ; vt[0x1B0]（6 实参）
```

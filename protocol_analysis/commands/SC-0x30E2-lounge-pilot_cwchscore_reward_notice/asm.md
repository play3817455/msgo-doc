# 汇编证据 —— SC-0x30E2-lounge-pilot_cwchscore_reward_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x47` @ `0xB5B3EC`）

```asm
; VA: 0xB5B3EC（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5B3EC  push    0x47          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— get_reward：偏移 0，长度 1，线类型 u8（是否获得奖励）
0xB5B427  call    sub_B06230     ; 读 u8
; 块内日志格式串 "get_reward=" → 含义锚点：0xB5B550

; 字段 2 —— num_reward：偏移 1，长度 1，线类型 u8（奖励数量）
0xB5B467  call    sub_B06230     ; 读 u8
; 块内日志格式串 "num_reward=" → 含义锚点：0xB5B57A

; 字段 3 —— highscore：偏移 2，长度 4，线类型 u32（最高分）
0xB5B48B  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "highscore=" → 含义锚点：0xB5B5A6

; 字段 4 —— coopwave_score_term：偏移 6，长度 65，线类型 str（协作波次评分条件串（槽位预算 `0x41`=65））
0xB5B4A3  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "coopwave_score_term=" → 含义锚点：0xB5B5CE

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5B4DA
0xB5B4DA  push    <模块/错误码>
0xB5B4DA  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5B647
0xB5B647  mov     edx, [obj]
;       mov     edx, [edx+0x4F0h]
;       call    edx          ; vt[0x4F0]（4 实参）
```

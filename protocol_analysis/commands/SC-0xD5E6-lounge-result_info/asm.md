# 汇编证据 —— SC-0xD5E6-lounge-result_info

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD518` @ `B7DA08`）

```asm
00B7D9F3  call    sub_B41120        ; lounge 守卫
00B7DA08  push    0D518h            ; 容量 = 0xD518
00B7DA0D  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序，节选）

```asm
00B7DA46  call    sub_B02DD0        ; 1 win_team：u32
00B7DA83  call    sub_B02DD0        ; 2 res_coop：u32
00B7DAAD  call    sub_B07880        ; 3 progress：struct（46B，claim 0x40）
00B7DAD7  call    sub_B44B70        ; 4 result：struct（555B，claim 0x258）
00B7DB05  call    sub_B453B0        ; 5 result_wbonus（4B）
00B7DB48  cmp     ebx, 68h          ; 6 score_ranking_A 计数上限 104
00B7DB7A  call    sub_B449E0        ; 6 score_ranking_A 元素（61B，槽 72）
00B7DCEB  call    sub_B02DF0        ; 10 ranking_highscore：u16
00B7DD1C  cmp     ebx, 94DCh        ; 11 debrief_info 计数上限 38108
00B7DD8C  call    sub_B434B0        ; 12 examination_list 元素（8B ×5）
00B7DDEB  cmp     edi, 5            ; 13 favms_add 计数上限 5
00B7DE4C  call    sub_B47120        ; 14 dcpoint（41B）
00B7DEEC  call    sub_B06200        ; 18 adop_uniq_msid：u64
00B7DF3C  call    sub_B02DD0        ; 20 season_class_up_promotion_point：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7DF50  cmp     eax, [esp+2C5Ch+var_2C40]
00B7DF56  jz      short loc_B7DF6F
```

## E4 去向（用途锚点）

```asm
00B7E5F7  call    edx               ; vt[0x3F4]，26 实参
```

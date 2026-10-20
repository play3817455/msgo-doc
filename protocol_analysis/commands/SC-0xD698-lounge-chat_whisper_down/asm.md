# 汇编证据 —— SC-0xD698-lounge-chat_whisper_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD2` @ `B7E629`）

```asm
00B7E614  call    sub_B41120        ; lounge 守卫
00B7E629  push    0D2h              ; 容量 = 0xD2
00B7E62E  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7E667  call    sub_B02DD0        ; 字段 1 from_pilot_id：u32
00B7E692  push    19h               ; 串槽预算 25
00B7E6A5  call    sub_B02BA0        ; 字段 2 from_pilot_name：NUL 串
00B7E6B1  push    0B5h              ; 串槽预算 181
00B7E6BC  call    sub_B02BA0        ; 字段 3 msg：NUL 串
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7E6CC  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7E6D2  jz      short loc_B7E6EB
```

## E4 去向（用途锚点）

```asm
00B7E833  call    edx               ; vt[0x120]，3 实参
```

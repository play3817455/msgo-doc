# 汇编证据 —— SC-0xD847-lounge-replay_get_access_url

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x101` @ `B7F0BB`）

```asm
00B7F0A6  call    sub_B41120        ; lounge 守卫
00B7F0D8  push    101h              ; 容量 = 0x101
00B7F0BB  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7F0D8  push    101h              ; 串槽预算 257
00B7F0EE  call    sub_B02BA0        ; 字段 1 url：NUL 串
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7F11A  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7F11E  jnz     short loc_B7F0FC
```

## E4 去向（用途锚点）

```asm
00B7F1FD  call    edx               ; vt[0x4E4]，1 实参
```

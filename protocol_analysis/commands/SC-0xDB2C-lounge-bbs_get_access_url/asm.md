# 汇编证据 —— SC-0xDB2C-lounge-bbs_get_access_url

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x101` @ `B80020`）

```asm
00B8000B  call    sub_B41120        ; lounge 守卫
00B80020  push    101h              ; 容量 = 0x101
00B80025  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B80053  call    sub_B02BA0        ; 字段 1 url：NUL 串（槽预算 257）
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B8007F  cmp     ebx, [esp+2C5Ch+var_2C40]
00B80083  jnz     short loc_B80061
```

## E4 去向（用途锚点）

```asm
00B80162  call    edx               ; vt[0x4EC]，1 实参
```

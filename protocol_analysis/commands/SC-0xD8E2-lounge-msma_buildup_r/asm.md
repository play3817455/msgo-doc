# 汇编证据 —— SC-0xD8E2-lounge-msma_buildup_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x20` @ `B7F8FA`）

```asm
00B7F8ED  call    sub_B41120        ; lounge 守卫
00B7F902  push    20h ; char        ; 容量 = 0x20
00B7F904  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7F93D  call    sub_B02DD0        ; 1 result：u32
00B7F97D  call    sub_B06200        ; 2 uniqid_ms：u64
00B7F9BD  call    sub_B02DD0        ; 3 ticket_id：u32
00B7F9E1  call    sub_B02DF0        ; 4 usenum：u16
00B7FA05  call    sub_B02DD0        ; 5 workres：u32
00B7FA2D  call    sub_B02DF0        ; 6 buildup_cnt：u16
00B7FA55  call    sub_B02DF0        ; 7 param_idx：u16
00B7FA7D  call    sub_B02DF0        ; 8 up_param：u16
00B7FAA5  call    sub_B02DD0        ; 9 mech_npcpict：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7FAB9  cmp     eax, [esp+2C5Ch+var_2C40]
00B7FADB  jz      short loc_B7FADB
```

## E4 去向（用途锚点）

```asm
00B7FD40  call    edx               ; vt[0x2B4]，10 实参
```

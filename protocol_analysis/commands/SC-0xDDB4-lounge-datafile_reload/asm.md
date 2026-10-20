# 汇编证据 —— SC-0xDDB4-lounge-datafile_reload

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8000112` @ `B81052`）

```asm
00B8103D  call    sub_B41120        ; lounge 守卫
00B81052  push    8000112h          ; 容量 = 0x8000112
00B81057  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B81090  call    sub_B02DD0        ; 1 result：u32
00B810BB  push    100h              ; 串槽预算 256
00B810D3  call    sub_B02BA0        ; 2 filepath：NUL 串
00B81110  call    sub_B02DD0        ; 3 hashval：u32
00B81134  call    sub_B02DD0        ; 4 src_bytes：u32
00B81158  call    sub_B02DF0        ; 5 compress：u16
00B81172  call    sub_B02DD0        ; 6 bin_num：u32
00B81186  cmp     ebx, 8000000h     ; 上限 0x8000000
00B8118C  ja      loc_B8109C        ; 越界 → 错误出口
00B8119C  call    sub_B05EA0        ; 按 count 预留 1B/槽（非字段）
00B811BC  call    sub_B06230        ; 7 bin 元素：u8
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B811E2  cmp     ecx, [esp+2C5Ch+var_2C40]
00B811E8  jz      short loc_B81201
```

## E4 去向（用途锚点）

```asm
00B81425  call    eax               ; vt[0x7C]，7 实参
```

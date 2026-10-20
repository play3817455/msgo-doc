# 汇编证据 —— SC-0xDE24-auth-proto_version_check_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B04817`）

```asm
00B04802  call    sub_B02C90        ; auth 守卫
00B04817  push    0Ch               ; 容量 = 0xC
00B04819  call    edx               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B04844  call    sub_B02DD0        ; 1 version：u32
00B04885  call    sub_B02DD0        ; 2 crc：u32
00B04897  call    sub_B02DD0        ; 3 gentime：u32
```

## E3 长度闭合（**成功分支**，auth 无收尾函数）

```asm
00B048A7  cmp     ebx, [esp+124h+var_108]
00B048AB  jnz     short loc_B04850   ; 不等 → 错误出口
```

## E4 去向（用途锚点）

```asm
00B049DB  call    edx               ; vt[0x68]，3 实参
```

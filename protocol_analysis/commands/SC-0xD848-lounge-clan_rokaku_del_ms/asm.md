# 汇编证据 —— SC-0xD848-lounge-clan_rokaku_del_ms

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7F4C6`）

```asm
00B7F4B1  call    sub_B41120        ; lounge 守卫
00B7F4C6  push    8                 ; 容量 = 0x8（> 线长 4，分配富余）
00B7F4C8  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B7F4F2  call    sub_B41470        ; 预留 4B 槽（非字段）
00B7F501  call    sub_B02DD0        ; 字段 1 uniq_msid：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B7F52D  cmp     ebx, [esp+2C5Ch+var_2C40]
00B7F531  jnz     short loc_B7F50F
```

## E4 去向（用途锚点）

```asm
00B7F604  call    edx               ; vt[0x48C]，1 实参
```

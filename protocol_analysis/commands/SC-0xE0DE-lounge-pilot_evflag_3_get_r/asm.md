# 汇编证据 —— SC-0xE0DE-lounge-pilot_evflag_3_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B82424`）

```asm
00B8240F  call    sub_B41120        ; lounge 守卫
00B82424  push    8                 ; 容量 = 0x8
00B82426  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B82450  call    sub_B41A10        ; 预留 8B 槽（u64，非字段）
00B8245F  call    sub_B06200        ; 字段 1 evflag3：u64
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B82488  cmp     eax, [esp+2C5Ch+var_2C40]
00B8248E  jz      short loc_B824A5
```

## E4 去向（用途锚点，低槽）

```asm
00B82577  call    eax               ; vt[0xA4]，2 实参（u64 拆低/高）
```

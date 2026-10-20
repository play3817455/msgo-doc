# 汇编证据 —— SC-0xDDE9-battle-module_toggle_level

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA` @ `B2D35C`）

```asm
00B2D347  call    sub_B05DA0        ; battle 守卫
00B2D35C  push    0Ah               ; 容量 = 0xA
00B2D35E  call    eax               ; vt[0x78]
```

## E2 字段读取序列（按线序）

```asm
00B2D397  call    sub_B02DF0        ; 1 ent_id：u16
00B2D3D7  call    sub_B02DD0        ; 2 level_up_flag：u32
00B2D3FB  call    sub_B02DD0        ; 3 next_level_max：u32
```

## E3 长度闭合（游标 == 报文末尾）

```asm
00B2D40B  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2D411  jz      short loc_B2D42D
```

## E4 去向（用途锚点）

```asm
00B2D562  call    eax               ; vt[0x380]，3 实参
```

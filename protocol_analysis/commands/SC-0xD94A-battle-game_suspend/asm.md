# 汇编证据 —— SC-0xD94A-battle-game_suspend

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口（**无**解码缓冲申请）

```asm
00B2C702  call    sub_B05DA0        ; battle 守卫
00B2C707  test    al, al
00B2C709  jz      loc_B317C7        ; 失败出口
```

## E2 零字段（无任何 bounded 读取）

```asm
; 块内只有 `sub_ABB2F0` / `sub_CA0CE0` / `sub_B03020` 等非 IO 调用，无 `sub_B02DD0`/`B02DF0`/`B06230`/`B06200`/`B02BA0`
```

## E3 长度闭合（**入口即闭合**，游标 == 报文末尾）

```asm
00B2C70F  mov     ebx, [esp+1B3Ch+var_1B28]
00B2C713  cmp     ebx, [esp+1B3Ch+var_1B24]
00B2C719  jz      short loc_B2C73E
```

## E4 去向（用途锚点，**无实参**）

```asm
00B2C7EF  call    eax               ; vt[0x100]，0 实参
```

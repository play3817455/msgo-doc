# 汇编证据 —— CS-0xF4B9-battle-battleship_get_down

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3FB20`（`0x00B3FB20`..`0x00B3FCCE`），函数 `sub_B3FB20`
- 命令名字符串：`)<-_proto_battle_client::send_battleship_get_down(` @ `0x00EE1700`
- opcode 写入：`0x00B3FB94`
- 声明容量：`0x6`（分配器容量 `push` @ `0x00B3FB66`）
- 提交（`sub_B02FF0`）：`0x00B3FBFF`
- 发送去向：`vt[0x58]` @ `0x00B3FC5C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3FB6F  push    eax
  00B3FB70  lea     ecx, [esp+44h+var_2C]
  00B3FB74  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3FB79  lea     ecx, [edi+6]
  00B3FB7C  lea     eax, [edi+2]
  00B3FB7F  cmp     eax, ecx
  00B3FB81  mov     [esp+40h+var_4], 0
  00B3FB89  ja      loc_B3FCB9
  00B3FB8F  lea     ebx, [eax+1]
  00B3FB92  cmp     ebx, ecx
  00B3FB94  mov     word ptr [edi], 0F4B9h   ; <<< 内联写线（u16）
  00B3FB99  ja      loc_B3FCB9
  00B3FB9F  mov     cl, [esp+40h+arg_0]
  00B3FBA3  mov     [eax], cl   ; <<< 内联写线（u8）
  00B3FBA5  mov     ebp, [esi+3FF0h]
  00B3FBAB  test    ebp, ebp
  00B3FBAD  jz      loc_B3FC5A
  00B3FBB3  lea     edx, [esp+40h+var_28]
  00B3FBB7  push    edx
  00B3FBB8  call    sub_CA0CE0
  00B3FBBD  add     esp, 4
  00B3FBC0  mov     ecx, [esi+8]
  00B3FBC3  push    offset aProtoBattleCli_290
  00B3FBC8  push    ecx
  00B3FBC9  push    offset aId
  00B3FBCE  push    eax
  00B3FBCF  push    ebp
  00B3FBD0  mov     byte ptr [esp+54h+var_4], 1
  00B3FBD5  call    sub_B03020
  00B3FBDA  add     esp, 8
  00B3FBDD  push    eax
  00B3FBDE  call    sub_41D990
  00B3FBE3  add     esp, 8
  00B3FBE6  mov     ecx, eax
  00B3FBE8  call    sub_ADC810
  00B3FBED  push    eax
  00B3FBEE  call    sub_41D990
  00B3FBF3  add     esp, 8
  00B3FBF6  lea     ecx, [esp+40h+var_28]
  00B3FBFA  mov     byte ptr [esp+40h+var_4], 0
  00B3FBFF  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3FBFF  call    sub_B02FF0
  00B3FC04  lea     edx, [esp+40h+arg_0]
  00B3FC08  push    edx
  00B3FC09  push    offset aReason
  00B3FC0E  push    ebp
  00B3FC0F  call    sub_41D990
  00B3FC14  add     esp, 8
  00B3FC17  push    eax
  00B3FC18  call    sub_B0C1F0
  00B3FC1D  add     esp, 8
  00B3FC20  push    offset aByte
  00B3FC25  mov     eax, ebx
  00B3FC27  sub     eax, edi
  00B3FC29  push    eax
  00B3FC2A  push    offset asc_EDAD58
  00B3FC2F  push    ebp
  00B3FC30  call    sub_41D990
  00B3FC35  add     esp, 8
  00B3FC38  mov     ecx, eax
  00B3FC3A  call    sub_B03580
  00B3FC3F  push    eax
  00B3FC40  call    sub_41D990
  00B3FC45  add     esp, 8
  00B3FC48  mov     ebp, eax
  00B3FC4A  push    0Ah
  00B3FC4C  mov     ecx, ebp
  00B3FC4E  call    sub_B036E0
  00B3FC53  mov     ecx, ebp
  00B3FC55  call    sub_40DDF0
  00B3FC5A  mov     edx, [esi]
  00B3FC5C  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B3FC5A  mov     edx, [esi]
  00B3FC5C  mov     eax, [edx+58h]
  00B3FC5F  sub     ebx, edi
  00B3FC61  push    ebx
  00B3FC62  push    edi
  00B3FC63  mov     ecx, esi
  00B3FC65  call    eax
  00B3FC67  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3FB94` | u16 / 2 |
| `reason` | `0xB3FBA3` | u8 / 1 |

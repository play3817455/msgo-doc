# 汇编证据 —— CS-0xE9C0-lounge-btlroom_commander_cheer

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B909E0`（`0x00B909E0`..`0x00B90B66`），函数 `sub_B909E0`
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_commander_cheer(` @ `0x00EEAEFC`
- opcode 写入：`0x00B90A39`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B90A26`）
- 提交（`sub_B02FF0`）：`0x00B90AA3`
- 发送去向：`vt[0x58]` @ `0x00B90AE4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B90A2F  push    eax
  00B90A30  lea     ecx, [esp+44h+var_2C]
  00B90A34  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B90A39  mov     word ptr [edi], 0E9C0h   ; <<< 内联写线（u16）
  00B90A3E  mov     ebp, [esi+7C0Ch]
  00B90A44  test    ebp, ebp
  00B90A46  mov     [esp+40h+var_4], 0
  00B90A4E  lea     ebx, [edi+2]
  00B90A51  jz      loc_B90AE2
  00B90A57  lea     ecx, [esp+40h+var_28]
  00B90A5B  push    ecx
  00B90A5C  call    sub_CA0CE0
  00B90A61  add     esp, 4
  00B90A64  mov     edx, [esi+8]
  00B90A67  push    offset aProtoLoungeCli_570
  00B90A6C  push    edx
  00B90A6D  push    offset aId
  00B90A72  push    eax
  00B90A73  push    ebp
  00B90A74  mov     byte ptr [esp+54h+var_4], 1
  00B90A79  call    sub_B03020
  00B90A7E  add     esp, 8
  00B90A81  push    eax
  00B90A82  call    sub_41D990
  00B90A87  add     esp, 8
  00B90A8A  mov     ecx, eax
  00B90A8C  call    sub_ADC810
  00B90A91  push    eax
  00B90A92  call    sub_41D990
  00B90A97  add     esp, 8
  00B90A9A  lea     ecx, [esp+40h+var_28]
  00B90A9E  mov     byte ptr [esp+40h+var_4], 0
  00B90AA3  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B90AA3  call    sub_B02FF0
  00B90AA8  push    offset aByte
  00B90AAD  mov     eax, ebx
  00B90AAF  sub     eax, edi
  00B90AB1  push    eax
  00B90AB2  push    offset asc_EDAD58
  00B90AB7  push    ebp
  00B90AB8  call    sub_41D990
  00B90ABD  add     esp, 8
  00B90AC0  mov     ecx, eax
  00B90AC2  call    sub_B03580
  00B90AC7  push    eax
  00B90AC8  call    sub_41D990
  00B90ACD  add     esp, 8
  00B90AD0  mov     ebp, eax
  00B90AD2  push    0Ah
  00B90AD4  mov     ecx, ebp
  00B90AD6  call    sub_B036E0
  00B90ADB  mov     ecx, ebp
  00B90ADD  call    sub_40DDF0
  00B90AE2  mov     edx, [esi]
  00B90AE4  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B90AE2  mov     edx, [esi]
  00B90AE4  mov     eax, [edx+58h]
  00B90AE7  sub     ebx, edi
  00B90AE9  push    ebx
  00B90AEA  push    edi
  00B90AEB  mov     ecx, esi
  00B90AED  call    eax
  00B90AEF  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B90A39` | u16 / 2 |

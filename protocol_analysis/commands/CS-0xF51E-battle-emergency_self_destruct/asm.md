# 汇编证据 —— CS-0xF51E-battle-emergency_self_destruct

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B3CB20`（`0x00B3CB20`..`0x00B3CCA6`），函数 `sub_B3CB20`
- 命令名字符串：`)<-_proto_battle_client::send_emergency_self_destruct(` @ `0x00EE11FC`
- opcode 写入：`0x00B3CB79`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00B3CB66`）
- 提交（`sub_B02FF0`）：`0x00B3CBE3`
- 发送去向：`vt[0x58]` @ `0x00B3CC24`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B3CB6F  push    eax
  00B3CB70  lea     ecx, [esp+44h+var_2C]
  00B3CB74  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B3CB79  mov     word ptr [edi], 0F51Eh   ; <<< 内联写线（u16）
  00B3CB7E  mov     ebp, [esi+3EBCh]
  00B3CB84  test    ebp, ebp
  00B3CB86  mov     [esp+40h+var_4], 0
  00B3CB8E  lea     ebx, [edi+2]
  00B3CB91  jz      loc_B3CC22
  00B3CB97  lea     ecx, [esp+40h+var_28]
  00B3CB9B  push    ecx
  00B3CB9C  call    sub_CA0CE0
  00B3CBA1  add     esp, 4
  00B3CBA4  mov     edx, [esi+8]
  00B3CBA7  push    offset aProtoBattleCli_293
  00B3CBAC  push    edx
  00B3CBAD  push    offset aId
  00B3CBB2  push    eax
  00B3CBB3  push    ebp
  00B3CBB4  mov     byte ptr [esp+54h+var_4], 1
  00B3CBB9  call    sub_B03020
  00B3CBBE  add     esp, 8
  00B3CBC1  push    eax
  00B3CBC2  call    sub_41D990
  00B3CBC7  add     esp, 8
  00B3CBCA  mov     ecx, eax
  00B3CBCC  call    sub_ADC810
  00B3CBD1  push    eax
  00B3CBD2  call    sub_41D990
  00B3CBD7  add     esp, 8
  00B3CBDA  lea     ecx, [esp+40h+var_28]
  00B3CBDE  mov     byte ptr [esp+40h+var_4], 0
  00B3CBE3  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B3CBE3  call    sub_B02FF0
  00B3CBE8  push    offset aByte
  00B3CBED  mov     eax, ebx
  00B3CBEF  sub     eax, edi
  00B3CBF1  push    eax
  00B3CBF2  push    offset asc_EDAD58
  00B3CBF7  push    ebp
  00B3CBF8  call    sub_41D990
  00B3CBFD  add     esp, 8
  00B3CC00  mov     ecx, eax
  00B3CC02  call    sub_B03580
  00B3CC07  push    eax
  00B3CC08  call    sub_41D990
  00B3CC0D  add     esp, 8
  00B3CC10  mov     ebp, eax
  00B3CC12  push    0Ah
  00B3CC14  mov     ecx, ebp
  00B3CC16  call    sub_B036E0
  00B3CC1B  mov     ecx, ebp
  00B3CC1D  call    sub_40DDF0
  00B3CC22  mov     edx, [esi]
  00B3CC24  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B3CC22  mov     edx, [esi]
  00B3CC24  mov     eax, [edx+58h]
  00B3CC27  sub     ebx, edi
  00B3CC29  push    ebx
  00B3CC2A  push    edi
  00B3CC2B  mov     ecx, esi
  00B3CC2D  call    eax
  00B3CC2F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3CB79` | u16 / 2 |

# 汇编证据 —— CS-0x8196-lounge-clan_rokaku_ms_deck_set

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2D40 @ `0xba2d40`（`0xba2d40`..`0xba2f32`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_rokaku_ms_deck_set(` @ `0xeecce8`
- opcode 写入：`0xba2db4`
- 声明容量：`0xE`（分配器容量 `push` @ `0xba2d86`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba2d8a  mov     ebp, eax
  0xba2d8c  mov     eax, [edi+0Ch]
  0xba2d8f  push    eax
  0xba2d90  lea     ecx, [esp+44h+var_2C]
  0xba2d94  call    sub_ABB2F0
  0xba2d99  lea     ecx, [ebp+0Eh]
  0xba2d9c  lea     eax, [ebp+2]
  0xba2d9f  cmp     eax, ecx
  0xba2da1  mov     [esp+40h+var_4], 0
  0xba2da9  ja      loc_BA2F1D
  0xba2daf  lea     edx, [eax+8]
  0xba2db2  cmp     edx, ecx
  0xba2db4  mov     word ptr [ebp+0], 8196h
  0xba2dba  ja      loc_BA2F1D
  0xba2dc0  mov     esi, [esp+40h+arg_0]
  0xba2dc4  mov     [eax], esi
  0xba2dc6  mov     esi, [esp+40h+arg_4]
  0xba2dca  lea     ebx, [edx+4]
  0xba2dcd  cmp     ebx, ecx
  0xba2dcf  mov     [eax+4], esi
  0xba2dd2  ja      loc_BA2F1D
  0xba2dd8  mov     ecx, [esp+40h+arg_8]
  0xba2ddc  mov     [edx], ecx
  0xba2dde  mov     esi, [edi+8144h]
  0xba2de4  test    esi, esi
  0xba2de6  jz      loc_BA2EBE
  0xba2dec  lea     edx, [esp+40h+var_28]
  0xba2df0  push    edx
  0xba2df1  call    sub_CA0CE0
  0xba2df6  add     esp, 4
  0xba2df9  mov     ecx, [edi+8]
  0xba2dfc  push    offset aProtoLoungeCli_567; ")<-_proto_lounge_client::send_clan_roka"...
  0xba2e01  push    ecx
  0xba2e02  push    offset aId; " (id:"
  0xba2e07  push    eax
  0xba2e08  push    esi
  0xba2e09  mov     byte ptr [esp+54h+var_4], 1
  0xba2e0e  call    sub_B03020
  0xba2e13  add     esp, 8
  0xba2e16  push    eax
  0xba2e17  call    sub_41D990
  0xba2e1c  add     esp, 8
  0xba2e1f  mov     ecx, eax
  0xba2e21  call    sub_ADC810
  0xba2e26  push    eax
  0xba2e27  call    sub_41D990
  0xba2e2c  add     esp, 8
  0xba2e2f  lea     ecx, [esp+40h+var_28]
  0xba2e33  mov     byte ptr [esp+40h+var_4], 0
  0xba2e38  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba2e4c  push    offset aUniqMsid; "uniq_msid="
  0xba2e6f  push    offset aDecktype; "decktype="
  0xba2e84  push    offset aByte; "]byte"
  0xba2e8e  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba2ec0  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba2db4` | u16 |
| `uniq_msid` | `0xBA2DC4, 0xBA2DCF` | u64 |
| `decktype` | `0xBA2DDC` | u32 |

# 汇编证据 —— CS-0x6CF9-lounge-clan_memb_exp_use

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA30D0 @ `0xba30d0`（`0xba30d0`..`0xba327d`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_memb_exp_use(` @ `0xeecd5c`
- opcode 写入：`0xba3144`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba311a  mov     ebp, eax
  0xba311c  mov     eax, [esi+0Ch]
  0xba311f  push    eax
  0xba3120  lea     ecx, [esp+44h+var_2C]
  0xba3124  call    sub_ABB2F0
  0xba3129  lea     ecx, [ebp+6]
  0xba312c  lea     eax, [ebp+2]
  0xba312f  cmp     eax, ecx
  0xba3131  mov     [esp+40h+var_4], 0
  0xba3139  ja      loc_BA3268
  0xba313f  lea     ebx, [eax+4]
  0xba3142  cmp     ebx, ecx
  0xba3144  mov     word ptr [ebp+0], 6CF9h
  0xba314a  ja      loc_BA3268
  0xba3150  mov     ecx, [esp+40h+arg_0]
  0xba3154  mov     [eax], ecx
  0xba3156  mov     edi, [esi+8154h]
  0xba315c  test    edi, edi
  0xba315e  jz      loc_BA3209
  0xba3164  lea     edx, [esp+40h+var_28]
  0xba3168  push    edx
  0xba3169  call    sub_CA0CE0
  0xba316e  add     esp, 4
  0xba3171  mov     ecx, [esi+8]
  0xba3174  push    offset aProtoLoungeCli_489; ")<-_proto_lounge_client::send_clan_memb"...
  0xba3179  push    ecx
  0xba317a  push    offset aId; " (id:"
  0xba317f  push    eax
  0xba3180  push    edi
  0xba3181  mov     byte ptr [esp+54h+var_4], 1
  0xba3186  call    sub_B03020
  0xba318b  add     esp, 8
  0xba318e  push    eax
  0xba318f  call    sub_41D990
  0xba3194  add     esp, 8
  0xba3197  mov     ecx, eax
  0xba3199  call    sub_ADC810
  0xba319e  push    eax
  0xba319f  call    sub_41D990
  0xba31a4  add     esp, 8
  0xba31a7  lea     ecx, [esp+40h+var_28]
  0xba31ab  mov     byte ptr [esp+40h+var_4], 0
  0xba31b0  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba31ba  push    offset aExp; "exp="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba31cf  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba320b  mov     eax, [edx+58h]
  0xba320e  sub     ebx, ebp
  0xba3210  push    ebx
  0xba3211  push    ebp
  0xba3212  mov     ecx, esi
  0xba3214  call    eax
  0xba3216  test    al, al
  0xba3218  jz      short loc_BA3268
  0xba321a  mov     eax, [esi+79A8h]
  0xba3220  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA3144` | u16 |
| `exp` | `0xBA3154` | u32 |

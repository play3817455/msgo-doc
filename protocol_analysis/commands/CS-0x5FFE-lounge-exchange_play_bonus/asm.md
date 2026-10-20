# 汇编证据 —— CS-0x5FFE-lounge-exchange_play_bonus

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9D450 @ `0xb9d450`（`0xb9d450`..`0xb9d5fd`）
- 命令名字符串：`)<-_proto_lounge_client::send_exchange_play_bonus(` @ `0xeec3a8`
- opcode 写入：`0xb9d4c4`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9d49a  mov     ebp, eax
  0xb9d49c  mov     eax, [esi+0Ch]
  0xb9d49f  push    eax
  0xb9d4a0  lea     ecx, [esp+44h+var_2C]
  0xb9d4a4  call    sub_ABB2F0
  0xb9d4a9  lea     ecx, [ebp+6]
  0xb9d4ac  lea     eax, [ebp+2]
  0xb9d4af  cmp     eax, ecx
  0xb9d4b1  mov     [esp+40h+var_4], 0
  0xb9d4b9  ja      loc_B9D5E8
  0xb9d4bf  lea     ebx, [eax+4]
  0xb9d4c2  cmp     ebx, ecx
  0xb9d4c4  mov     word ptr [ebp+0], 5FFEh
  0xb9d4ca  ja      loc_B9D5E8
  0xb9d4d0  mov     ecx, [esp+40h+arg_0]
  0xb9d4d4  mov     [eax], ecx
  0xb9d4d6  mov     edi, [esi+7FACh]
  0xb9d4dc  test    edi, edi
  0xb9d4de  jz      loc_B9D589
  0xb9d4e4  lea     edx, [esp+40h+var_28]
  0xb9d4e8  push    edx
  0xb9d4e9  call    sub_CA0CE0
  0xb9d4ee  add     esp, 4
  0xb9d4f1  mov     ecx, [esi+8]
  0xb9d4f4  push    offset aProtoLoungeCli_586; ")<-_proto_lounge_client::send_exchange_"...
  0xb9d4f9  push    ecx
  0xb9d4fa  push    offset aId; " (id:"
  0xb9d4ff  push    eax
  0xb9d500  push    edi
  0xb9d501  mov     byte ptr [esp+54h+var_4], 1
  0xb9d506  call    sub_B03020
  0xb9d50b  add     esp, 8
  0xb9d50e  push    eax
  0xb9d50f  call    sub_41D990
  0xb9d514  add     esp, 8
  0xb9d517  mov     ecx, eax
  0xb9d519  call    sub_ADC810
  0xb9d51e  push    eax
  0xb9d51f  call    sub_41D990
  0xb9d524  add     esp, 8
  0xb9d527  lea     ecx, [esp+40h+var_28]
  0xb9d52b  mov     byte ptr [esp+40h+var_4], 0
  0xb9d530  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9d53a  push    offset aRewardId; "reward_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9d54f  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9d58b  mov     eax, [edx+58h]
  0xb9d58e  sub     ebx, ebp
  0xb9d590  push    ebx
  0xb9d591  push    ebp
  0xb9d592  mov     ecx, esi
  0xb9d594  call    eax
  0xb9d596  test    al, al
  0xb9d598  jz      short loc_B9D5E8
  0xb9d59a  mov     eax, [esi+79A8h]
  0xb9d5a0  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9D4C4` | u16 |
| `reward_id` | `0xB9D4D4` | u32 |

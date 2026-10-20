# 汇编证据 —— CS-0x511B-lounge-season_rankerbattle_team_info_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA84B0 @ `0xba84b0`（`0xba84b0`..`0xba865d`）
- 命令名字符串：`)<-_proto_lounge_client::send_season_rankerbattle_team_info_get(` @ `0xeed688`
- opcode 写入：`0xba8524`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba84fa  mov     ebp, eax
  0xba84fc  mov     eax, [esi+0Ch]
  0xba84ff  push    eax
  0xba8500  lea     ecx, [esp+44h+var_2C]
  0xba8504  call    sub_ABB2F0
  0xba8509  lea     ecx, [ebp+6]
  0xba850c  lea     eax, [ebp+2]
  0xba850f  cmp     eax, ecx
  0xba8511  mov     [esp+40h+var_4], 0
  0xba8519  ja      loc_BA8648
  0xba851f  lea     ebx, [eax+4]
  0xba8522  cmp     ebx, ecx
  0xba8524  mov     word ptr [ebp+0], 511Bh
  0xba852a  ja      loc_BA8648
  0xba8530  mov     ecx, [esp+40h+arg_0]
  0xba8534  mov     [eax], ecx
  0xba8536  mov     edi, [esi+8354h]
  0xba853c  test    edi, edi
  0xba853e  jz      loc_BA85E9
  0xba8544  lea     edx, [esp+40h+var_28]
  0xba8548  push    edx
  0xba8549  call    sub_CA0CE0
  0xba854e  add     esp, 4
  0xba8551  mov     ecx, [esi+8]
  0xba8554  push    offset aProtoLoungeCli_547; ")<-_proto_lounge_client::send_season_ra"...
  0xba8559  push    ecx
  0xba855a  push    offset aId; " (id:"
  0xba855f  push    eax
  0xba8560  push    edi
  0xba8561  mov     byte ptr [esp+54h+var_4], 1
  0xba8566  call    sub_B03020
  0xba856b  add     esp, 8
  0xba856e  push    eax
  0xba856f  call    sub_41D990
  0xba8574  add     esp, 8
  0xba8577  mov     ecx, eax
  0xba8579  call    sub_ADC810
  0xba857e  push    eax
  0xba857f  call    sub_41D990
  0xba8584  add     esp, 8
  0xba8587  lea     ecx, [esp+40h+var_28]
  0xba858b  mov     byte ptr [esp+40h+var_4], 0
  0xba8590  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba859a  push    offset aTroops; "troops="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba85af  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba85eb  mov     eax, [edx+58h]
  0xba85ee  sub     ebx, ebp
  0xba85f0  push    ebx
  0xba85f1  push    ebp
  0xba85f2  mov     ecx, esi
  0xba85f4  call    eax
  0xba85f6  test    al, al
  0xba85f8  jz      short loc_BA8648
  0xba85fa  mov     eax, [esi+79A8h]
  0xba8600  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA8524` | u16 |
| `troops` | `0xBA8534` | u32 |

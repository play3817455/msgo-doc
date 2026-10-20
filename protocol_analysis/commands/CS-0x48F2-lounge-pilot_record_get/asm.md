# 汇编证据 —— CS-0x48F2-lounge-pilot_record_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8E290 @ `0xb8e290`（`0xb8e290`..`0xb8e4c9`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_record_get(` @ `0xeeaa90`
- opcode 写入：`0xb8e30c`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8e2da  mov     ebp, eax
  0xb8e2dc  mov     eax, [edi+0Ch]
  0xb8e2df  push    eax
  0xb8e2e0  lea     ecx, [esp+4Ch+var_34]
  0xb8e2e4  call    sub_ABB2F0
  0xb8e2e9  lea     ecx, [ebp+0Eh]
  0xb8e2ec  lea     eax, [ebp+2]
  0xb8e2ef  cmp     eax, ecx
  0xb8e2f1  mov     [esp+48h+var_4], 0
  0xb8e2f9  mov     [esp+48h+var_30], ebp
  0xb8e2fd  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8e301  ja      loc_B8E4B4
  0xb8e307  lea     edx, [eax+4]
  0xb8e30a  cmp     edx, ecx
  0xb8e30c  mov     word ptr [ebp+0], 48F2h
  0xb8e312  ja      loc_B8E4B4
  0xb8e318  mov     esi, [esp+48h+arg_0]
  0xb8e31c  mov     [eax], esi
  0xb8e31e  mov     eax, edx
  0xb8e320  lea     edx, [eax+4]
  0xb8e323  cmp     edx, ecx
  0xb8e325  ja      loc_B8E4B4
  0xb8e32b  mov     ecx, [esp+48h+arg_4]
  0xb8e32f  mov     [esp+48h+var_30], edx
  0xb8e333  lea     edx, [esp+48h+var_30]
  0xb8e337  mov     [eax], ecx
  0xb8e339  push    edx
  0xb8e33a  lea     eax, [esp+4Ch+arg_8]
  0xb8e33e  push    eax
  0xb8e33f  call    sub_B061C0
  0xb8e344  add     esp, 8
  0xb8e347  test    al, al
  0xb8e349  jz      loc_B8E4B4
  0xb8e34f  mov     esi, [edi+7B4Ch]
  0xb8e355  test    esi, esi
  0xb8e357  mov     ebx, [esp+48h+var_30]
  0xb8e35b  jz      loc_B8E458
  0xb8e361  lea     ecx, [esp+48h+var_28]
  0xb8e365  push    ecx
  0xb8e366  call    sub_CA0CE0
  0xb8e36b  add     esp, 4
  0xb8e36e  mov     edx, [edi+8]
  0xb8e371  push    offset aProtoLoungeCli_362; ")<-_proto_lounge_client::send_pilot_rec"...
  0xb8e376  push    edx
  0xb8e377  push    offset aId; " (id:"
  0xb8e37c  push    eax
  0xb8e37d  push    esi
  0xb8e37e  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8e383  call    sub_B03020
  0xb8e388  add     esp, 8
  0xb8e38b  push    eax
  0xb8e38c  call    sub_41D990
  0xb8e391  add     esp, 8
  0xb8e394  mov     ecx, eax
  0xb8e396  call    sub_ADC810
  0xb8e39b  push    eax
  0xb8e39c  call    sub_41D990
  0xb8e3a1  add     esp, 8
  0xb8e3a4  lea     ecx, [esp+48h+var_28]
  0xb8e3a8  mov     byte ptr [esp+48h+var_4], 0
  0xb8e3ad  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8e3bc  push    offset aPilotId; "pilot_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8e3e4  push    offset aWorldId; "world_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8e407  push    offset aIsCheckmedal; "is_checkmedal="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8e41e  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8e45a  mov     eax, [edx+58h]
  0xb8e45d  sub     ebx, ebp
  0xb8e45f  push    ebx
  0xb8e460  push    ebp
  0xb8e461  mov     ecx, edi
  0xb8e463  call    eax
  0xb8e465  test    al, al
  0xb8e467  jz      short loc_B8E4B4
  0xb8e469  mov     eax, [edi+79A8h]
  0xb8e46f  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8E30C` | u16 |
| `pilot_id` | `0xB8E31C` | u32 |
| `world_id` | `0xB8E337` | u32 |
| `is_checkmedal` | `0xB8E33F` | u8 |

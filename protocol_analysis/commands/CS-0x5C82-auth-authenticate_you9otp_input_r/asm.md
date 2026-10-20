# 汇编证据 —— CS-0x5C82-auth-authenticate_you9otp_input_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B05370 @ `0xb05370`（`0xb05370`..`0xb055cf`）
- 命令名字符串：`)<-_proto_auth_client::send_authenticate_you9otp_input_r(` @ `0xedb048`
- opcode 写入：`0xb053e9`
- 声明容量：`0x26`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb053b7  mov     ebp, eax
  0xb053b9  mov     eax, [edi+0Ch]
  0xb053bc  push    eax
  0xb053bd  lea     ecx, [esp+4Ch+var_34]
  0xb053c1  call    sub_ABB2F0
  0xb053c6  lea     ecx, [ebp+26h]
  0xb053c9  lea     eax, [ebp+2]
  0xb053cc  cmp     eax, ecx
  0xb053ce  mov     [esp+48h+var_4], 0
  0xb053d6  mov     [esp+48h+var_30], ebp
  0xb053da  mov     dword ptr [esp+48h+var_2C], ecx
  0xb053de  ja      loc_B055BA
  0xb053e4  lea     edx, [eax+4]
  0xb053e7  cmp     edx, ecx
  0xb053e9  mov     word ptr [ebp+0], 5C82h
  0xb053ef  ja      loc_B055BA
  0xb053f5  mov     ecx, [esp+48h+arg_0]
  0xb053f9  mov     [esp+48h+var_30], edx
  0xb053fd  push    11h
  0xb053ff  lea     edx, [esp+4Ch+var_30]
  0xb05403  mov     [eax], ecx
  0xb05405  mov     eax, [esp+4Ch+arg_4]
  0xb05409  push    edx
  0xb0540a  push    eax
  0xb0540b  call    sub_B02B40   <<< pushN=17(0x11)
  0xb05410  add     esp, 0Ch
  0xb05413  test    al, al
  0xb05415  jz      loc_B055BA
  0xb0541b  mov     edx, [esp+48h+arg_8]
  0xb0541f  push    9
  0xb05421  lea     ecx, [esp+4Ch+var_30]
  0xb05425  push    ecx
  0xb05426  push    edx
  0xb05427  call    sub_B02B40   <<< pushN=9(0x9)
  0xb0542c  add     esp, 0Ch
  0xb0542f  test    al, al
  0xb05431  jz      loc_B055BA
  0xb05437  mov     esi, [edi+3A4h]
  0xb0543d  test    esi, esi
  0xb0543f  mov     ebx, [esp+48h+var_30]
  0xb05443  jz      loc_B0555E
  0xb05449  lea     eax, [esp+48h+var_28]
  0xb0544d  push    eax
  0xb0544e  call    sub_CA0CE0
  0xb05453  add     esp, 4
  0xb05456  mov     ecx, [edi+8]
  0xb05459  push    offset aProtoAuthClien_5; ")<-_proto_auth_client::send_authenticat"...
  0xb0545e  push    ecx
  0xb0545f  push    offset aId; " (id:"
  0xb05464  push    eax
  0xb05465  push    esi
  0xb05466  mov     byte ptr [esp+5Ch+var_4], 1
  0xb0546b  call    sub_B03020
  0xb05470  add     esp, 8
  0xb05473  push    eax
  0xb05474  call    sub_41D990
  0xb05479  add     esp, 8
  0xb0547c  mov     ecx, eax
  0xb0547e  call    sub_ADC810
  0xb05483  push    eax
  0xb05484  call    sub_41D990
  0xb05489  add     esp, 8
  0xb0548c  lea     ecx, [esp+48h+var_28]
  0xb05490  mov     byte ptr [esp+48h+var_4], 0
  0xb05495  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb054a4  push    offset aOtpType; "otp_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb054d1  push    offset aOtpMatrixCode; "otp_matrix_code=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb05504  push    offset aInputOtp; "input_otp=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb05524  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb05560  mov     edx, [eax+58h]
  0xb05563  sub     ebx, ebp
  0xb05565  push    ebx
  0xb05566  push    ebp
  0xb05567  mov     ecx, edi
  0xb05569  call    edx
  0xb0556b  test    al, al
  0xb0556d  jz      short loc_B055BA
  0xb0556f  mov     eax, [edi+380h]
  0xb05575  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB053E9` | u16 |
| `otp_type` | `0xB05403` | u32 |
| `otp_matrix_code` | `0xB0540B` | bytes |
| `input_otp` | `0xB05427` | bytes |

# 汇编证据 —— CS-0x44CD-auth-authenticate_bnpotp_input_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B05190 @ `0xb05190`（`0xb05190`..`0xb0536c`）
- 命令名字符串：`)<-_proto_auth_client::send_authenticate_bnpotp_input_r(` @ `0xedb00c`
- opcode 写入：`0xb05219`
- 声明容量：`0x206`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb051da  mov     edi, eax
  0xb051dc  mov     eax, [esi+0Ch]
  0xb051df  push    eax
  0xb051e0  lea     ecx, [esp+4Ch+var_34]
  0xb051e4  call    sub_ABB2F0
  0xb051e9  lea     ecx, [edi+206h]
  0xb051ef  lea     eax, [edi+2]
  0xb051f2  cmp     eax, ecx
  0xb051f4  mov     [esp+48h+var_4], 0
  0xb051fc  mov     [esp+48h+var_30], edi
  0xb05200  mov     dword ptr [esp+48h+var_2C], ecx
  0xb05204  ja      loc_B05357
  0xb0520a  mov     edx, [esp+48h+arg_0]
  0xb0520e  push    201h
  0xb05213  lea     ecx, [esp+4Ch+var_30]
  0xb05217  push    ecx
  0xb05218  push    edx
  0xb05219  mov     word ptr [edi], 44CDh
  0xb0521e  mov     [esp+54h+var_30], eax
  0xb05222  call    sub_B02B40   <<< pushN=513(0x201)
  0xb05227  add     esp, 0Ch
  0xb0522a  test    al, al
  0xb0522c  jz      loc_B05357
  0xb05232  mov     ebp, [esi+39Ch]
  0xb05238  test    ebp, ebp
  0xb0523a  mov     ebx, [esp+48h+var_30]
  0xb0523e  jz      loc_B052F9
  0xb05244  lea     eax, [esp+48h+var_28]
  0xb05248  push    eax
  0xb05249  call    sub_CA0CE0
  0xb0524e  add     esp, 4
  0xb05251  mov     ecx, [esi+8]
  0xb05254  push    offset aProtoAuthClien_4; ")<-_proto_auth_client::send_authenticat"...
  0xb05259  push    ecx
  0xb0525a  push    offset aId; " (id:"
  0xb0525f  push    eax
  0xb05260  push    ebp
  0xb05261  mov     byte ptr [esp+5Ch+var_4], 1
  0xb05266  call    sub_B03020
  0xb0526b  add     esp, 8
  0xb0526e  push    eax
  0xb0526f  call    sub_41D990
  0xb05274  add     esp, 8
  0xb05277  mov     ecx, eax
  0xb05279  call    sub_ADC810
  0xb0527e  push    eax
  0xb0527f  call    sub_41D990
  0xb05284  add     esp, 8
  0xb05287  lea     ecx, [esp+48h+var_28]
  0xb0528b  mov     byte ptr [esp+48h+var_4], 0
  0xb05290  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb0529f  push    offset aInputOtp; "input_otp=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb052bf  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb052fb  mov     eax, [edx+58h]
  0xb052fe  mov     ebp, ebx
  0xb05300  sub     ebp, edi
  0xb05302  push    ebp
  0xb05303  push    edi
  0xb05304  mov     ecx, esi
  0xb05306  call    eax
  0xb05308  test    al, al
  0xb0530a  jz      short loc_B05357
  0xb0530c  mov     eax, [esi+380h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB05219` | u16 |
| `input_otp` | `0xB05222` | bytes |

# 汇编证据 —— CS-0x61AF-lounge-btlroom_enter

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8FE80 @ `0xb8fe80`（`0xb8fe80`..`0xb90196`）
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_enter(` @ `0xeeade8`
- opcode 写入：`0xb8fefc`
- 声明容量：`0x32`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8feca  mov     ebp, eax
  0xb8fecc  mov     eax, [edi+0Ch]
  0xb8fecf  push    eax
  0xb8fed0  lea     ecx, [esp+4Ch+var_34]
  0xb8fed4  call    sub_ABB2F0
  0xb8fed9  lea     ecx, [ebp+32h]
  0xb8fedc  lea     eax, [ebp+2]
  0xb8fedf  cmp     eax, ecx
  0xb8fee1  mov     [esp+48h+var_4], 0
  0xb8fee9  mov     [esp+48h+var_30], ebp
  0xb8feed  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8fef1  ja      loc_B90181
  0xb8fef7  lea     edx, [eax+4]
  0xb8fefa  cmp     edx, ecx
  0xb8fefc  mov     word ptr [ebp+0], 61AFh
  0xb8ff02  ja      loc_B90181
  0xb8ff08  mov     esi, [esp+48h+arg_0]
  0xb8ff0c  mov     [eax], esi
  0xb8ff0e  mov     eax, edx
  0xb8ff10  lea     edx, [eax+4]
  0xb8ff13  cmp     edx, ecx
  0xb8ff15  ja      loc_B90181
  0xb8ff1b  mov     ecx, [esp+48h+arg_4]
  0xb8ff1f  mov     [esp+48h+var_30], edx
  0xb8ff23  push    19h
  0xb8ff25  lea     edx, [esp+4Ch+var_30]
  0xb8ff29  mov     [eax], ecx
  0xb8ff2b  mov     eax, [esp+4Ch+arg_8]
  0xb8ff2f  push    edx
  0xb8ff30  push    eax
  0xb8ff31  call    sub_B02B40   <<< pushN=25(0x19)
  0xb8ff36  add     esp, 0Ch
  0xb8ff39  test    al, al
  0xb8ff3b  jz      loc_B90181
  0xb8ff41  lea     ecx, [esp+48h+var_30]
  0xb8ff45  push    ecx
  0xb8ff46  lea     edx, [esp+4Ch+arg_C]
  0xb8ff4a  push    edx
  0xb8ff4b  call    sub_B061C0
  0xb8ff50  add     esp, 8
  0xb8ff53  test    al, al
  0xb8ff55  jz      loc_B90181
  0xb8ff5b  lea     eax, [esp+48h+var_30]
  0xb8ff5f  push    eax
  0xb8ff60  lea     ecx, [esp+4Ch+arg_10]
  0xb8ff64  push    ecx
  0xb8ff65  call    sub_B061C0
  0xb8ff6a  add     esp, 8
  0xb8ff6d  test    al, al
  0xb8ff6f  jz      loc_B90181
  0xb8ff75  lea     edx, [esp+48h+var_30]
  0xb8ff79  push    edx
  0xb8ff7a  lea     eax, [esp+4Ch+arg_14]
  0xb8ff7e  push    eax
  0xb8ff7f  call    sub_B02D80
  0xb8ff84  add     esp, 8
  0xb8ff87  test    al, al
  0xb8ff89  jz      loc_B90181
  0xb8ff8f  mov     esi, [edi+7BE8h]
  0xb8ff95  test    esi, esi
  0xb8ff97  mov     ebx, [esp+48h+var_30]
  0xb8ff9b  jz      loc_B90122
  0xb8ffa1  lea     ecx, [esp+48h+var_28]
  0xb8ffa5  push    ecx
  0xb8ffa6  call    sub_CA0CE0
  0xb8ffab  add     esp, 4
  0xb8ffae  mov     edx, [edi+8]
  0xb8ffb1  push    offset aProtoLoungeCli_408; ")<-_proto_lounge_client::send_btlroom_e"...
  0xb8ffb6  push    edx
  0xb8ffb7  push    offset aId; " (id:"
  0xb8ffbc  push    eax
  0xb8ffbd  push    esi
  0xb8ffbe  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8ffc3  call    sub_B03020
  0xb8ffc8  add     esp, 8
  0xb8ffcb  push    eax
  0xb8ffcc  call    sub_41D990
  0xb8ffd1  add     esp, 8
  0xb8ffd4  mov     ecx, eax
  0xb8ffd6  call    sub_ADC810
  0xb8ffdb  push    eax
  0xb8ffdc  call    sub_41D990
  0xb8ffe1  add     esp, 8
  0xb8ffe4  lea     ecx, [esp+48h+var_28]
  0xb8ffe8  mov     byte ptr [esp+48h+var_4], 0
  0xb8ffed  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8fffc  push    offset aMatchingType; "matching_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb90024  push    offset aRoomId; "room_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb90051  push    offset aRoomPw; "room_pw=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb90084  push    offset aIsAudience; "is_audience="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb900ae  push    offset aAudienceTeamsi; "audience_teamside="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb900d3  push    offset aExtruleId; "extrule_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb900e8  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb90124  mov     eax, [edx+58h]
  0xb90127  sub     ebx, ebp
  0xb90129  push    ebx
  0xb9012a  push    ebp
  0xb9012b  mov     ecx, edi
  0xb9012d  call    eax
  0xb9012f  test    al, al
  0xb90131  jz      short loc_B90181
  0xb90133  mov     eax, [edi+79A8h]
  0xb90139  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8FEFC` | u16 |
| `matching_type` | `0xB8FF0C` | u32 |
| `room_id` | `0xB8FF29` | u32 |
| `room_pw` | `0xB8FF31` | bytes |
| `is_audience` | `0xB8FF4B` | u8 |
| `audience_teamside` | `0xB8FF65` | u8 |
| `extrule_id` | `0xB8FF7F` | u32 |

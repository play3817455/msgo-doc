# 汇编证据 —— CS-0x6DF1-lounge-btlroom_create

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8FAC0 @ `0xb8fac0`（`0xb8fac0`..`0xb8fe7b`）
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_create(` @ `0xeeadb8`
- opcode 写入：`0xb8fb42`
- 声明容量：`0x82`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8fb0d  mov     ebp, eax
  0xb8fb0f  mov     eax, [edi+0Ch]
  0xb8fb12  push    eax
  0xb8fb13  lea     ecx, [esp+4Ch+var_34]
  0xb8fb17  call    sub_ABB2F0
  0xb8fb1c  lea     ecx, [ebp+82h]
  0xb8fb22  lea     eax, [ebp+2]
  0xb8fb25  cmp     eax, ecx
  0xb8fb27  mov     [esp+48h+var_4], 0
  0xb8fb2f  mov     [esp+48h+var_30], ebp
  0xb8fb33  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8fb37  ja      loc_B8FE66
  0xb8fb3d  lea     edx, [eax+4]
  0xb8fb40  cmp     edx, ecx
  0xb8fb42  mov     word ptr [ebp+0], 6DF1h
  0xb8fb48  ja      loc_B8FE66
  0xb8fb4e  mov     ecx, [esp+48h+arg_0]
  0xb8fb52  mov     [esp+48h+var_30], edx
  0xb8fb56  push    49h ; 'I'
  0xb8fb58  lea     edx, [esp+4Ch+var_30]
  0xb8fb5c  mov     [eax], ecx
  0xb8fb5e  mov     eax, [esp+4Ch+arg_4]
  0xb8fb62  push    edx
  0xb8fb63  push    eax
  0xb8fb64  call    sub_B02B40   <<< pushN=73(0x49)
  0xb8fb69  add     esp, 0Ch
  0xb8fb6c  test    al, al
  0xb8fb6e  jz      loc_B8FE66
  0xb8fb74  mov     edx, [esp+48h+arg_8]
  0xb8fb78  push    19h
  0xb8fb7a  lea     ecx, [esp+4Ch+var_30]
  0xb8fb7e  push    ecx
  0xb8fb7f  push    edx
  0xb8fb80  call    sub_B02B40   <<< pushN=25(0x19)
  0xb8fb85  add     esp, 0Ch
  0xb8fb88  test    al, al
  0xb8fb8a  jz      loc_B8FE66
  0xb8fb90  lea     eax, [esp+48h+var_30]
  0xb8fb94  push    eax
  0xb8fb95  lea     ecx, [esp+4Ch+arg_C]
  0xb8fb99  push    ecx
  0xb8fb9a  call    sub_B02D80
  0xb8fb9f  add     esp, 8
  0xb8fba2  test    al, al
  0xb8fba4  jz      loc_B8FE66
  0xb8fbaa  lea     edx, [esp+48h+var_30]
  0xb8fbae  push    edx
  0xb8fbaf  lea     eax, [esp+4Ch+arg_10]
  0xb8fbb3  push    eax
  0xb8fbb4  call    sub_B02D80
  0xb8fbb9  add     esp, 8
  0xb8fbbc  test    al, al
  0xb8fbbe  jz      loc_B8FE66
  0xb8fbc4  lea     ecx, [esp+48h+var_30]
  0xb8fbc8  push    ecx
  0xb8fbc9  lea     edx, [esp+4Ch+arg_14]
  0xb8fbcd  push    edx
  0xb8fbce  call    sub_B061C0
  0xb8fbd3  add     esp, 8
  0xb8fbd6  test    al, al
  0xb8fbd8  jz      loc_B8FE66
  0xb8fbde  lea     eax, [esp+48h+var_30]
  0xb8fbe2  push    eax
  0xb8fbe3  lea     ecx, [esp+4Ch+arg_18]
  0xb8fbe7  push    ecx
  0xb8fbe8  call    sub_B061C0
  0xb8fbed  add     esp, 8
  0xb8fbf0  test    al, al
  0xb8fbf2  jz      loc_B8FE66
  0xb8fbf8  lea     edx, [esp+48h+var_30]
  0xb8fbfc  push    edx
  0xb8fbfd  lea     eax, [esp+4Ch+arg_1C]
  0xb8fc01  push    eax
  0xb8fc02  call    sub_B061C0
  0xb8fc07  add     esp, 8
  0xb8fc0a  test    al, al
  0xb8fc0c  jz      loc_B8FE66
  0xb8fc12  mov     esi, [edi+7BE0h]
  0xb8fc18  test    esi, esi
  0xb8fc1a  mov     ebx, [esp+48h+var_30]
  0xb8fc1e  jz      loc_B8FE07
  0xb8fc24  lea     ecx, [esp+48h+var_28]
  0xb8fc28  push    ecx
  0xb8fc29  call    sub_CA0CE0
  0xb8fc2e  add     esp, 4
  0xb8fc31  mov     edx, [edi+8]
  0xb8fc34  push    offset aProtoLoungeCli_409; ")<-_proto_lounge_client::send_btlroom_c"...
  0xb8fc39  push    edx
  0xb8fc3a  push    offset aId; " (id:"
  0xb8fc3f  push    eax
  0xb8fc40  push    esi
  0xb8fc41  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8fc46  call    sub_B03020
  0xb8fc4b  add     esp, 8
  0xb8fc4e  push    eax
  0xb8fc4f  call    sub_41D990
  0xb8fc54  add     esp, 8
  0xb8fc57  mov     ecx, eax
  0xb8fc59  call    sub_ADC810
  0xb8fc5e  push    eax
  0xb8fc5f  call    sub_41D990
  0xb8fc64  add     esp, 8
  0xb8fc67  lea     ecx, [esp+48h+var_28]
  0xb8fc6b  mov     byte ptr [esp+48h+var_4], 0
  0xb8fc70  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8fc7f  push    offset aMatchingType; "matching_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fcac  push    offset aRoomName; "room_name=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fce4  push    offset aRoomPw; "room_pw=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fd17  push    offset aMissionId; "mission_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fd3f  push    offset aExtruleId; "extrule_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fd67  push    offset aIsLock; "is_lock="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fd91  push    offset aIsVsclan; "is_vsclan="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fdb6  push    offset aIsEvCaravan; "is_ev_caravan="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8fdcd  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8fe09  mov     edx, [eax+58h]
  0xb8fe0c  sub     ebx, ebp
  0xb8fe0e  push    ebx
  0xb8fe0f  push    ebp
  0xb8fe10  mov     ecx, edi
  0xb8fe12  call    edx
  0xb8fe14  test    al, al
  0xb8fe16  jz      short loc_B8FE66
  0xb8fe18  mov     eax, [edi+79A8h]
  0xb8fe1e  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8FB42` | u16 |
| `matching_type` | `0xB8FB5C` | u32 |
| `room_name` | `0xB8FB64` | bytes |
| `room_pw` | `0xB8FB80` | bytes |
| `mission_id` | `0xB8FB9A` | u32 |
| `extrule_id` | `0xB8FBB4` | u32 |
| `is_lock` | `0xB8FBCE` | u8 |
| `is_vsclan` | `0xB8FBE8` | u8 |
| `is_ev_caravan` | `0xB8FC02` | u8 |

# 汇编证据 —— CS-0xF24B-battle-authenticate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B31B10`（`0x00B31B10`..`0x00B31E1E`），函数 `sub_B31B10`
- 命令名字符串：`)<-_proto_battle_client::send_authenticate(` @ `0x00EE0574`
- opcode 写入：`0x00B31B89`
- 声明容量：`0x42`（分配器容量 `push` @ `0x00B31B53`）
- 提交（`sub_B02FF0`）：`0x00B31C7A`
- 发送去向：`vt[0x58]` @ `0x00B31DAF`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B31B5C  push    eax
  00B31B5D  lea     ecx, [esp+4Ch+var_34]
  00B31B61  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B31B66  lea     ecx, [ebp+42h]
  00B31B69  lea     eax, [ebp+2]
  00B31B6C  cmp     eax, ecx
  00B31B6E  mov     [esp+48h+var_4], 0
  00B31B76  mov     [esp+48h+var_30], ebp
  00B31B7A  mov     dword ptr [esp+48h+var_2C], ecx
  00B31B7E  ja      loc_B31E09
  00B31B84  lea     edx, [eax+4]
  00B31B87  cmp     edx, ecx
  00B31B89  mov     word ptr [ebp+0], 0F24Bh   ; <<< 内联写线（u16）
  00B31B8F  ja      loc_B31E09
  00B31B95  mov     esi, [esp+48h+arg_0]
  00B31B99  mov     [eax], esi   ; <<< 内联写线（u32）
  00B31B9B  mov     eax, edx
  00B31B9D  lea     edx, [eax+4]
  00B31BA0  cmp     edx, ecx
  00B31BA2  ja      loc_B31E09
  00B31BA8  mov     ecx, [esp+48h+arg_4]
  00B31BAC  mov     [esp+48h+var_30], edx
  00B31BB0  lea     edx, [esp+48h+var_30]
  00B31BB4  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B31BB6  push    edx
  00B31BB7  lea     eax, [esp+4Ch+arg_8]
  00B31BBB  push    eax
  00B31BBC  call    sub_B02D80   ; <<< 写线原语 u32
  00B31BC1  add     esp, 8
  00B31BC4  test    al, al
  00B31BC6  jz      loc_B31E09
  00B31BCC  lea     ecx, [esp+48h+var_30]
  00B31BD0  push    ecx
  00B31BD1  lea     edx, [esp+4Ch+arg_C]
  00B31BD5  push    edx
  00B31BD6  call    sub_B02D80   ; <<< 写线原语 u32
  00B31BDB  add     esp, 8
  00B31BDE  test    al, al
  00B31BE0  jz      loc_B31E09
  00B31BE6  mov     ecx, dword ptr [esp+48h+arg_10]
  00B31BEA  push    29h
  00B31BEC  lea     eax, [esp+4Ch+var_30]
  00B31BF0  push    eax
  00B31BF1  push    ecx
  00B31BF2  call    sub_B02B40   ; <<< 写线原语 str
  00B31BF7  add     esp, 0Ch
  00B31BFA  test    al, al
  00B31BFC  jz      loc_B31E09
  00B31C02  lea     edx, [esp+48h+var_30]
  00B31C06  push    edx
  00B31C07  lea     eax, [esp+4Ch+arg_14]
  00B31C0B  push    eax
  00B31C0C  call    sub_B061C0   ; <<< 写线原语 u8
  00B31C11  add     esp, 8
  00B31C14  test    al, al
  00B31C16  jz      loc_B31E09
  00B31C1C  mov     esi, [edi+3C00h]
  00B31C22  test    esi, esi
  00B31C24  mov     ebx, [esp+48h+var_30]
  00B31C28  jz      loc_B31DAD
  00B31C2E  lea     ecx, [esp+48h+var_28]
  00B31C32  push    ecx
  00B31C33  call    sub_CA0CE0
  00B31C38  add     esp, 4
  00B31C3B  mov     edx, [edi+8]
  00B31C3E  push    offset aProtoBattleCli_217
  00B31C43  push    edx
  00B31C44  push    offset aId
  00B31C49  push    eax
  00B31C4A  push    esi
  00B31C4B  mov     byte ptr [esp+5Ch+var_4], 1
  00B31C50  call    sub_B03020
  00B31C55  add     esp, 8
  00B31C58  push    eax
  00B31C59  call    sub_41D990
  00B31C5E  add     esp, 8
  00B31C61  mov     ecx, eax
  00B31C63  call    sub_ADC810
  00B31C68  push    eax
  00B31C69  call    sub_41D990
  00B31C6E  add     esp, 8
  00B31C71  lea     ecx, [esp+48h+var_28]
  00B31C75  mov     byte ptr [esp+48h+var_4], 0
  00B31C7A  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B31C7A  call    sub_B02FF0
  00B31C7F  mov     eax, [esp+48h+arg_0]
  00B31C83  push    offset word_F641DC
  00B31C88  push    eax
  00B31C89  push    offset aUserid
  00B31C8E  push    esi
  00B31C8F  call    sub_41D990
  00B31C94  add     esp, 8
  00B31C97  mov     ecx, eax
  00B31C99  call    sub_B03580
  00B31C9E  push    eax
  00B31C9F  call    sub_41D990
  00B31CA4  mov     ecx, [esp+50h+arg_4]
  00B31CA8  add     esp, 8
  00B31CAB  push    offset word_F641DC
  00B31CB0  push    ecx
  00B31CB1  push    offset aWorldId
  00B31CB6  push    esi
  00B31CB7  call    sub_41D990
  00B31CBC  add     esp, 8
  00B31CBF  mov     ecx, eax
  00B31CC1  call    sub_B03580
  00B31CC6  push    eax
  00B31CC7  call    sub_41D990
  00B31CCC  mov     edx, [esp+50h+arg_8]
  00B31CD0  add     esp, 8
  00B31CD3  push    offset word_F641DC
  00B31CD8  push    edx
  00B31CD9  push    offset aPilotId
  00B31CDE  push    esi
  00B31CDF  call    sub_41D990
  00B31CE4  add     esp, 8
  00B31CE7  mov     ecx, eax
  00B31CE9  call    sub_B03580
  00B31CEE  push    eax
  00B31CEF  call    sub_41D990
  00B31CF4  mov     eax, [esp+50h+arg_C]
  00B31CF8  add     esp, 8
  00B31CFB  push    offset word_F641DC
  00B31D00  push    eax
  00B31D01  push    offset aRoomId
  00B31D06  push    esi
  00B31D07  call    sub_41D990
  00B31D0C  add     esp, 8
  00B31D0F  mov     ecx, eax
  00B31D11  call    sub_B03580
  00B31D16  push    eax
  00B31D17  call    sub_41D990
  00B31D1C  mov     ecx, dword ptr [esp+50h+arg_10]
  00B31D20  add     esp, 8
  00B31D23  push    offset word_F641DC
  00B31D28  push    offset asc_EDAD54
  00B31D2D  push    ecx
  00B31D2E  push    offset aOtpBattle
  00B31D33  push    esi
  00B31D34  call    sub_41D990
  00B31D39  add     esp, 8
  00B31D3C  push    eax
  00B31D3D  call    sub_41D990
  00B31D42  add     esp, 8
  00B31D45  push    eax
  00B31D46  call    sub_41D990
  00B31D4B  add     esp, 8
  00B31D4E  push    eax
  00B31D4F  call    sub_41D990
  00B31D54  add     esp, 8
  00B31D57  lea     edx, [esp+48h+arg_14]
  00B31D5B  push    edx
  00B31D5C  push    offset aIsComeback
  00B31D61  push    esi
  00B31D62  call    sub_41D990
  00B31D67  add     esp, 8
  00B31D6A  push    eax
  00B31D6B  call    sub_B0C1F0
  00B31D70  add     esp, 8
  00B31D73  push    offset aByte
  00B31D78  mov     eax, ebx
  00B31D7A  sub     eax, ebp
  00B31D7C  push    eax
  00B31D7D  push    offset asc_EDAD58
  00B31D82  push    esi
  00B31D83  call    sub_41D990
  00B31D88  add     esp, 8
  00B31D8B  mov     ecx, eax
  00B31D8D  call    sub_B03580
  00B31D92  push    eax
  00B31D93  call    sub_41D990
  00B31D98  add     esp, 8
  00B31D9B  mov     esi, eax
  00B31D9D  push    0Ah
  00B31D9F  mov     ecx, esi
  00B31DA1  call    sub_B036E0
  00B31DA6  mov     ecx, esi
  00B31DA8  call    sub_40DDF0
  00B31DAD  mov     edx, [edi]
  00B31DAF  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B31DAD  mov     edx, [edi]
  00B31DAF  mov     eax, [edx+58h]
  00B31DB2  sub     ebx, ebp
  00B31DB4  push    ebx
  00B31DB5  push    ebp
  00B31DB6  mov     ecx, edi
  00B31DB8  call    eax
  00B31DBA  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B31B89` | u16 / 2 |
| `userid` | `0xB31B95`;`0xB31B99` | u32 / 4 |
| `world_id` | `0xB31BA8`;`0xB31BB4` | u32 / 4 |
| `pilot_id` | `0xB31BBC` | u32 / 4 |
| `room_id` | `0xB31BD6` | u32 / 4 |
| `otp_battle` | `0xB31BEA`;`0xB31BF2` | str / var |
| `is_comeback` | `0xB31C0C` | u8 / 1 |

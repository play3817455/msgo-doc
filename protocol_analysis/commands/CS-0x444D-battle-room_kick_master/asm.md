# 汇编证据 —— CS-0x444D-battle-room_kick_master

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B330C0 @ `0xb330c0`（`0xb330c0`..`0xb332a3`）
- 命令名字符串：`)<-_proto_battle_client::send_room_kick_master(` @ `0xee0808`
- opcode 写入：`0xb33134`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3310a  mov     ebp, eax
  0xb3310c  mov     eax, [edi+0Ch]
  0xb3310f  push    eax
  0xb33110  lea     ecx, [esp+44h+var_2C]
  0xb33114  call    sub_ABB2F0
  0xb33119  lea     ecx, [ebp+0Ah]
  0xb3311c  lea     eax, [ebp+2]
  0xb3311f  cmp     eax, ecx
  0xb33121  mov     [esp+40h+var_4], 0
  0xb33129  ja      loc_B3328E
  0xb3312f  lea     edx, [eax+4]
  0xb33132  cmp     edx, ecx
  0xb33134  mov     word ptr [ebp+0], 444Dh
  0xb3313a  ja      loc_B3328E
  0xb33140  mov     esi, [esp+40h+arg_0]
  0xb33144  lea     ebx, [edx+4]
  0xb33147  cmp     ebx, ecx
  0xb33149  mov     [eax], esi
  0xb3314b  ja      loc_B3328E
  0xb33151  mov     ecx, [esp+40h+arg_4]
  0xb33155  mov     [edx], ecx
  0xb33157  mov     esi, [edi+3CA4h]
  0xb3315d  test    esi, esi
  0xb3315f  jz      loc_B33232
  0xb33165  lea     edx, [esp+40h+var_28]
  0xb33169  push    edx
  0xb3316a  call    sub_CA0CE0
  0xb3316f  add     esp, 4
  0xb33172  mov     ecx, [edi+8]
  0xb33175  push    offset aProtoBattleCli_223; ")<-_proto_battle_client::send_room_kick"...
  0xb3317a  push    ecx
  0xb3317b  push    offset aId; " (id:"
  0xb33180  push    eax
  0xb33181  push    esi
  0xb33182  mov     byte ptr [esp+54h+var_4], 1
  0xb33187  call    sub_B03020
  0xb3318c  add     esp, 8
  0xb3318f  push    eax
  0xb33190  call    sub_41D990
  0xb33195  add     esp, 8
  0xb33198  mov     ecx, eax
  0xb3319a  call    sub_ADC810
  0xb3319f  push    eax
  0xb331a0  call    sub_41D990
  0xb331a5  add     esp, 8
  0xb331a8  lea     ecx, [esp+40h+var_28]
  0xb331ac  mov     byte ptr [esp+40h+var_4], 0
  0xb331b1  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb331c0  push    offset aWorldId; "world_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb331e3  push    offset aPilotId; "pilot_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb331f8  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb33234  mov     eax, [edx+58h]
  0xb33237  sub     ebx, ebp
  0xb33239  push    ebx
  0xb3323a  push    ebp
  0xb3323b  mov     ecx, edi
  0xb3323d  call    eax
  0xb3323f  test    al, al
  0xb33241  jz      short loc_B3328E
  0xb33243  mov     eax, [edi+3BF0h]
  0xb33249  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB33134` | u16 |
| `world_id` | `0xB33149` | u32 |
| `pilot_id` | `0xB33155` | u32 |

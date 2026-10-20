# 汇编证据 —— CS-0x6486-battle-commander_support_execute

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3E580 @ `0xb3e580`（`0xb3e580`..`0xb3e882`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_support_execute(` @ `0xee14c4`
- opcode 写入：`0xb3e5fc`
- 声明容量：`0x1A`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3e5ca  mov     ebp, eax
  0xb3e5cc  mov     eax, [edi+0Ch]
  0xb3e5cf  push    eax
  0xb3e5d0  lea     ecx, [esp+4Ch+var_34]
  0xb3e5d4  call    sub_ABB2F0
  0xb3e5d9  lea     eax, [ebp+1Ah]
  0xb3e5dc  lea     ecx, [ebp+2]
  0xb3e5df  cmp     ecx, eax
  0xb3e5e1  mov     [esp+48h+var_4], 0
  0xb3e5e9  mov     [esp+48h+var_30], ebp
  0xb3e5ed  mov     dword ptr [esp+48h+var_2C], eax
  0xb3e5f1  ja      loc_B3E86D
  0xb3e5f7  lea     edx, [ecx+4]
  0xb3e5fa  cmp     edx, eax
  0xb3e5fc  mov     word ptr [ebp+0], 6486h
  0xb3e602  ja      loc_B3E86D
  0xb3e608  mov     esi, [esp+48h+arg_0]
  0xb3e60c  mov     [ecx], esi
  0xb3e60e  lea     ecx, [edx+2]
  0xb3e611  cmp     ecx, eax
  0xb3e613  ja      loc_B3E86D
  0xb3e619  mov     ax, word ptr [esp+48h+arg_4]
  0xb3e61e  mov     [esp+48h+var_30], ecx
  0xb3e622  lea     ecx, [esp+48h+var_30]
  0xb3e626  mov     [edx], ax
  0xb3e629  push    ecx
  0xb3e62a  lea     edx, [esp+4Ch+arg_8]
  0xb3e62e  push    edx
  0xb3e62f  call    sub_B02DA0
  0xb3e634  add     esp, 8
  0xb3e637  test    al, al
  0xb3e639  jz      loc_B3E86D
  0xb3e63f  lea     eax, [esp+48h+var_30]
  0xb3e643  push    eax
  0xb3e644  lea     ecx, [esp+4Ch+arg_C]
  0xb3e648  push    ecx
  0xb3e649  call    sub_B02DA0
  0xb3e64e  add     esp, 8
  0xb3e651  test    al, al
  0xb3e653  jz      loc_B3E86D
  0xb3e659  lea     edx, [esp+48h+var_30]
  0xb3e65d  push    edx
  0xb3e65e  lea     eax, [esp+4Ch+arg_10]
  0xb3e662  push    eax
  0xb3e663  call    sub_B061C0
  0xb3e668  add     esp, 8
  0xb3e66b  test    al, al
  0xb3e66d  jz      loc_B3E86D
  0xb3e673  lea     ecx, [esp+48h+var_30]
  0xb3e677  push    ecx
  0xb3e678  lea     edx, [esp+4Ch+arg_14]
  0xb3e67c  push    edx
  0xb3e67d  call    sub_B02D80
  0xb3e682  add     esp, 8
  0xb3e685  test    al, al
  0xb3e687  jz      loc_B3E86D
  0xb3e68d  mov     esi, [edi+3F78h]
  0xb3e693  test    esi, esi
  0xb3e695  mov     ebx, [esp+48h+var_30]
  0xb3e699  jz      loc_B3E80E
  0xb3e69f  lea     eax, [esp+48h+var_28]
  0xb3e6a3  push    eax
  0xb3e6a4  call    sub_CA0CE0
  0xb3e6a9  add     esp, 4
  0xb3e6ac  mov     ecx, [edi+8]
  0xb3e6af  push    offset aProtoBattleCli_280; ")<-_proto_battle_client::send_commander"...
  0xb3e6b4  push    ecx
  0xb3e6b5  push    offset aId; " (id:"
  0xb3e6ba  push    eax
  0xb3e6bb  push    esi
  0xb3e6bc  mov     byte ptr [esp+5Ch+var_4], 1
  0xb3e6c1  call    sub_B03020
  0xb3e6c6  add     esp, 8
  0xb3e6c9  push    eax
  0xb3e6ca  call    sub_41D990
  0xb3e6cf  add     esp, 8
  0xb3e6d2  mov     ecx, eax
  0xb3e6d4  call    sub_ADC810
  0xb3e6d9  push    eax
  0xb3e6da  call    sub_41D990
  0xb3e6df  add     esp, 8
  0xb3e6e2  lea     ecx, [esp+48h+var_28]
  0xb3e6e6  mov     byte ptr [esp+48h+var_4], 0
  0xb3e6eb  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3e6fa  push    offset aSupportType; "support_type="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e722  push    offset aTargetX; "target_x="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e74a  push    offset aTargetY; "target_y="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e772  push    offset aTargetZ; "target_z="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e79a  push    offset aSptSpotIndex; "spt_spot_index="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e7bf  push    offset aVal; "val="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3e7d4  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3e810  mov     edx, [eax+58h]
  0xb3e813  sub     ebx, ebp
  0xb3e815  push    ebx
  0xb3e816  push    ebp
  0xb3e817  mov     ecx, edi
  0xb3e819  call    edx
  0xb3e81b  test    al, al
  0xb3e81d  jz      short loc_B3E86D
  0xb3e81f  mov     eax, [edi+3BF0h]
  0xb3e825  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3E5FC` | u16 |
| `support_type` | `0xB3E60C` | u32 |
| `target_x` | `0xB3E626` | u16 |
| `target_y` | `0xB3E62F` | u16 |
| `target_z` | `0xB3E649` | u16 |
| `spt_spot_index` | `0xB3E663` | u8 |
| `val` | `0xB3E67D` | u32 |

# 汇编证据 —— CS-0x7CA0-battle-weapon_fire__shot_single

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B364E0 @ `0xb364e0`（`0xb364e0`..`0xb368a7`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__shot_single(` @ `0xee0c60`
- opcode 写入：`0xb3655c`
- 声明容量：`0x26`（分配器容量 `push` @ `0xb36526`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3652a  mov     ebp, eax
  0xb3652c  mov     eax, [edi+0Ch]
  0xb3652f  push    eax
  0xb36530  lea     ecx, [esp+4Ch+var_34]
  0xb36534  call    sub_ABB2F0
  0xb36539  lea     eax, [ebp+26h]
  0xb3653c  lea     ecx, [ebp+2]
  0xb3653f  cmp     ecx, eax
  0xb36541  mov     [esp+48h+var_4], 0
  0xb36549  mov     [esp+48h+var_30], ebp
  0xb3654d  mov     dword ptr [esp+48h+var_2C], eax
  0xb36551  ja      loc_B36892
  0xb36557  lea     edx, [ecx+4]
  0xb3655a  cmp     edx, eax
  0xb3655c  mov     word ptr [ebp+0], 7CA0h
  0xb36562  ja      loc_B36892
  0xb36568  mov     esi, [esp+48h+arg_0]
  0xb3656c  mov     [ecx], esi
  0xb3656e  lea     ecx, [edx+2]
  0xb36571  cmp     ecx, eax
  0xb36573  ja      loc_B36892
  0xb36579  mov     ax, word ptr [esp+48h+arg_4]
  0xb3657e  mov     [esp+48h+var_30], ecx
  0xb36582  lea     ecx, [esp+48h+var_30]
  0xb36586  mov     [edx], ax
  0xb36589  push    ecx
  0xb3658a  lea     edx, [esp+4Ch+arg_8]
  0xb3658e  push    edx
  0xb3658f  call    sub_B02DA0
  0xb36594  add     esp, 8
  0xb36597  test    al, al
  0xb36599  jz      loc_B36892
  0xb3659f  lea     eax, [esp+48h+var_30]
  0xb365a3  push    eax
  0xb365a4  lea     ecx, [esp+4Ch+arg_C]
  0xb365a8  push    ecx
  0xb365a9  call    sub_B02DA0
  0xb365ae  add     esp, 8
  0xb365b1  test    al, al
  0xb365b3  jz      loc_B36892
  0xb365b9  lea     edx, [esp+48h+var_30]
  0xb365bd  push    edx
  0xb365be  lea     eax, [esp+4Ch+arg_10]
  0xb365c2  push    eax
  0xb365c3  call    sub_B02DA0
  0xb365c8  add     esp, 8
  0xb365cb  test    al, al
  0xb365cd  jz      loc_B36892
  0xb365d3  lea     ecx, [esp+48h+var_30]
  0xb365d7  push    ecx
  0xb365d8  lea     edx, [esp+4Ch+arg_14]
  0xb365dc  push    edx
  0xb365dd  call    sub_B02DA0
  0xb365e2  add     esp, 8
  0xb365e5  test    al, al
  0xb365e7  jz      loc_B36892
  0xb365ed  lea     eax, [esp+48h+var_30]
  0xb365f1  push    eax
  0xb365f2  lea     ecx, [esp+4Ch+arg_18]
  0xb365f6  push    ecx
  0xb365f7  call    sub_B061C0
  0xb365fc  add     esp, 8
  0xb365ff  test    al, al
  0xb36601  jz      loc_B36892
  0xb36607  lea     edx, [esp+48h+var_30]
  0xb3660b  push    edx
  0xb3660c  lea     eax, [esp+4Ch+arg_1C]
  0xb36610  push    eax
  0xb36611  call    sub_B02DA0
  0xb36616  add     esp, 8
  0xb36619  test    al, al
  0xb3661b  jz      loc_B36892
  0xb36621  lea     ecx, [esp+48h+var_30]
  0xb36625  push    ecx
  0xb36626  lea     edx, [esp+4Ch+arg_20]
  0xb3662a  push    edx
  0xb3662b  call    sub_B061C0
  0xb36630  add     esp, 8
  0xb36633  test    al, al
  0xb36635  jz      loc_B36892
  0xb3663b  mov     esi, [edi+3DC8h]
  0xb36641  test    esi, esi
  0xb36643  mov     ebx, [esp+48h+var_30]
  0xb36647  jz      loc_B36836
  0xb3664d  lea     eax, [esp+48h+var_28]
  0xb36651  push    eax
  0xb36652  call    sub_CA0CE0
  0xb36657  add     esp, 4
  0xb3665a  mov     ecx, [edi+8]
  0xb3665d  push    offset aProtoBattleCli_245; ")<-_proto_battle_client::send_weapon_fi"...
  0xb36662  push    ecx
  0xb36663  push    offset aId; " (id:"
  0xb36668  push    eax
  0xb36669  push    esi
  0xb3666a  mov     byte ptr [esp+5Ch+var_4], 1
  0xb3666f  call    sub_B03020
  0xb36674  add     esp, 8
  0xb36677  push    eax
  0xb36678  call    sub_41D990
  0xb3667d  add     esp, 8
  0xb36680  mov     ecx, eax
  0xb36682  call    sub_ADC810
  0xb36687  push    eax
  0xb36688  call    sub_41D990
  0xb3668d  add     esp, 8
  0xb36690  lea     ecx, [esp+48h+var_28]
  0xb36694  mov     byte ptr [esp+48h+var_4], 0
  0xb36699  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb366a8  push    offset aFrameCount; "frame_count="
  0xb366d0  push    offset aTargetX; "target_x="
  0xb366f8  push    offset aTargetY; "target_y="
  0xb36720  push    offset aTargetZ; "target_z="
  0xb36748  push    offset aRcntBulletMgz; "rcnt_bullet_mgz="
  0xb36770  push    offset aRcntBulletAll; "rcnt_bullet_all="
  0xb36798  push    offset aChargeLv; "charge_lv="
  0xb367c2  push    offset aAiEntId; "AI_ent_id="
  0xb367e5  push    offset aSalvoSlot; "salvo_slot="
  0xb367fc  push    offset aByte; "]byte"
  0xb36806  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb36838  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3655c` | u16 |
| `frame_count` | `0xB3656C` | u32 |
| `target_x` | `0xB36586` | u16 |
| `target_y` | `0xB3658F` | u16 |
| `target_z` | `0xB365A9` | u16 |
| `rcnt_bullet_mgz` | `0xB365C3` | u16 |
| `rcnt_bullet_all` | `0xB365DD` | u16 |
| `charge_lv` | `0xB365F7` | u8 |
| `AI_ent_id` | `0xB36611` | u16 |
| `salvo_slot` | `0xB3662B` | u8 |

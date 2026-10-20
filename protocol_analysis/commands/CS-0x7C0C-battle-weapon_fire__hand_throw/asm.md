# 汇编证据 —— CS-0x7C0C-battle-weapon_fire__hand_throw

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B379F0 @ `0xb379f0`（`0xb379f0`..`0xb37f5c`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__hand_throw(` @ `0xee0d8c`
- opcode 写入：`0xb37a6c`
- 声明容量：`0x3E`（分配器容量 `push` @ `0xb37a36`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb37a3a  mov     ebp, eax
  0xb37a3c  mov     eax, [edi+0Ch]
  0xb37a3f  push    eax
  0xb37a40  lea     ecx, [esp+4Ch+var_34]
  0xb37a44  call    sub_ABB2F0
  0xb37a49  lea     eax, [ebp+3Eh]
  0xb37a4c  lea     ecx, [ebp+2]
  0xb37a4f  cmp     ecx, eax
  0xb37a51  mov     [esp+48h+var_4], 0
  0xb37a59  mov     [esp+48h+var_30], ebp
  0xb37a5d  mov     dword ptr [esp+48h+var_2C], eax
  0xb37a61  ja      loc_B37F47
  0xb37a67  lea     edx, [ecx+4]
  0xb37a6a  cmp     edx, eax
  0xb37a6c  mov     word ptr [ebp+0], 7C0Ch
  0xb37a72  ja      loc_B37F47
  0xb37a78  mov     esi, [esp+48h+arg_0]
  0xb37a7c  mov     [ecx], esi
  0xb37a7e  lea     ecx, [edx+2]
  0xb37a81  cmp     ecx, eax
  0xb37a83  ja      loc_B37F47
  0xb37a89  mov     ax, word ptr [esp+48h+arg_4]
  0xb37a8e  mov     [esp+48h+var_30], ecx
  0xb37a92  lea     ecx, [esp+48h+var_30]
  0xb37a96  mov     [edx], ax
  0xb37a99  push    ecx
  0xb37a9a  lea     edx, [esp+4Ch+arg_8]
  0xb37a9e  push    edx
  0xb37a9f  call    sub_B02DA0
  0xb37aa4  add     esp, 8
  0xb37aa7  test    al, al
  0xb37aa9  jz      loc_B37F47
  0xb37aaf  lea     eax, [esp+48h+var_30]
  0xb37ab3  push    eax
  0xb37ab4  lea     ecx, [esp+4Ch+arg_C]
  0xb37ab8  push    ecx
  0xb37ab9  call    sub_B02DA0
  0xb37abe  add     esp, 8
  0xb37ac1  test    al, al
  0xb37ac3  jz      loc_B37F47
  0xb37ac9  lea     edx, [esp+48h+var_30]
  0xb37acd  push    edx
  0xb37ace  lea     eax, [esp+4Ch+arg_10]
  0xb37ad2  push    eax
  0xb37ad3  call    sub_B02DA0
  0xb37ad8  add     esp, 8
  0xb37adb  test    al, al
  0xb37add  jz      loc_B37F47
  0xb37ae3  lea     ecx, [esp+48h+var_30]
  0xb37ae7  push    ecx
  0xb37ae8  lea     edx, [esp+4Ch+arg_14]
  0xb37aec  push    edx
  0xb37aed  call    sub_B02DA0
  0xb37af2  add     esp, 8
  0xb37af5  test    al, al
  0xb37af7  jz      loc_B37F47
  0xb37afd  lea     eax, [esp+48h+var_30]
  0xb37b01  push    eax
  0xb37b02  lea     ecx, [esp+4Ch+arg_18]
  0xb37b06  push    ecx
  0xb37b07  call    sub_B02DA0
  0xb37b0c  add     esp, 8
  0xb37b0f  test    al, al
  0xb37b11  jz      loc_B37F47
  0xb37b17  lea     edx, [esp+48h+var_30]
  0xb37b1b  push    edx
  0xb37b1c  lea     eax, [esp+4Ch+arg_1C]
  0xb37b20  push    eax
  0xb37b21  call    sub_B02DA0
  0xb37b26  add     esp, 8
  0xb37b29  test    al, al
  0xb37b2b  jz      loc_B37F47
  0xb37b31  lea     ecx, [esp+48h+var_30]
  0xb37b35  push    ecx
  0xb37b36  lea     edx, [esp+4Ch+arg_20]
  0xb37b3a  push    edx
  0xb37b3b  call    sub_B02DA0
  0xb37b40  add     esp, 8
  0xb37b43  test    al, al
  0xb37b45  jz      loc_B37F47
  0xb37b4b  lea     eax, [esp+48h+var_30]
  0xb37b4f  push    eax
  0xb37b50  lea     ecx, [esp+4Ch+arg_24]
  0xb37b54  push    ecx
  0xb37b55  call    sub_B061C0
  0xb37b5a  add     esp, 8
  0xb37b5d  test    al, al
  0xb37b5f  jz      loc_B37F47
  0xb37b65  lea     edx, [esp+48h+var_30]
  0xb37b69  push    edx
  0xb37b6a  lea     eax, [esp+4Ch+arg_28]
  0xb37b6e  push    eax
  0xb37b6f  call    sub_B061C0
  0xb37b74  add     esp, 8
  0xb37b77  test    al, al
  0xb37b79  jz      loc_B37F47
  0xb37b7f  lea     ecx, [esp+48h+var_30]
  0xb37b83  push    ecx
  0xb37b84  lea     edx, [esp+4Ch+arg_2C]
  0xb37b88  push    edx
  0xb37b89  call    sub_B02D80
  0xb37b8e  add     esp, 8
  0xb37b91  test    al, al
  0xb37b93  jz      loc_B37F47
  0xb37b99  lea     eax, [esp+48h+var_30]
  0xb37b9d  push    eax
  0xb37b9e  lea     ecx, [esp+4Ch+arg_30]
  0xb37ba5  push    ecx
  0xb37ba6  call    sub_B061C0
  0xb37bab  add     esp, 8
  0xb37bae  test    al, al
  0xb37bb0  jz      loc_B37F47
  0xb37bb6  lea     edx, [esp+48h+var_30]
  0xb37bba  push    edx
  0xb37bbb  lea     eax, [esp+4Ch+arg_34]
  0xb37bc2  push    eax
  0xb37bc3  call    sub_B02DA0
  0xb37bc8  add     esp, 8
  0xb37bcb  test    al, al
  0xb37bcd  jz      loc_B37F47
  0xb37bd3  lea     ecx, [esp+48h+var_30]
  0xb37bd7  push    ecx
  0xb37bd8  lea     edx, [esp+4Ch+arg_38]
  0xb37bdf  push    edx
  0xb37be0  call    sub_B061C0
  0xb37be5  add     esp, 8
  0xb37be8  test    al, al
  0xb37bea  jz      loc_B37F47
  0xb37bf0  mov     esi, [edi+3DECh]
  0xb37bf6  test    esi, esi
  0xb37bf8  mov     ebx, [esp+48h+var_30]
  0xb37bfc  jz      loc_B37EEB
  0xb37c02  lea     eax, [esp+48h+var_28]
  0xb37c06  push    eax
  0xb37c07  call    sub_CA0CE0
  0xb37c0c  add     esp, 4
  0xb37c0f  mov     ecx, [edi+8]
  0xb37c12  push    offset aProtoBattleCli_252; ")<-_proto_battle_client::send_weapon_fi"...
  0xb37c17  push    ecx
  0xb37c18  push    offset aId; " (id:"
  0xb37c1d  push    eax
  0xb37c1e  push    esi
  0xb37c1f  mov     byte ptr [esp+5Ch+var_4], 1
  0xb37c24  call    sub_B03020
  0xb37c29  add     esp, 8
  0xb37c2c  push    eax
  0xb37c2d  call    sub_41D990
  0xb37c32  add     esp, 8
  0xb37c35  mov     ecx, eax
  0xb37c37  call    sub_ADC810
  0xb37c3c  push    eax
  0xb37c3d  call    sub_41D990
  0xb37c42  add     esp, 8
  0xb37c45  lea     ecx, [esp+48h+var_28]
  0xb37c49  mov     byte ptr [esp+48h+var_4], 0
  0xb37c4e  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb37c5d  push    offset aFrameCount; "frame_count="
  0xb37c85  push    offset aLaunchX; "launch_x="
  0xb37cad  push    offset aLaunchY; "launch_y="
  0xb37cd5  push    offset aLaunchZ; "launch_z="
  0xb37cfd  push    offset aTargetX; "target_x="
  0xb37d25  push    offset aTargetY; "target_y="
  0xb37d4d  push    offset aTargetZ; "target_z="
  0xb37d75  push    offset aTargetEntId; "target_ent_id="
  0xb37d9d  push    offset aMsec; "msec="
  0xb37dc5  push    offset aShot0Impact1; "shot0_impact1="
  0xb37def  push    offset aFxOpt; "fx_opt="
  0xb37e1c  push    offset aImpactGrenadeI; "impact_grenade_id="
  0xb37e47  push    offset aChargeLv; "charge_lv="
  0xb37e74  push    offset aAiEntId; "AI_ent_id="
  0xb37e9a  push    offset aSalvoSlot; "salvo_slot="
  0xb37eb1  push    offset aByte; "]byte"
  0xb37ebb  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb37eed  mov     edx, [eax+58h]
  0xb37f10  add     dword ptr [edi+1A58h], 1
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb37a6c` | u16 |
| `frame_count` | `0xB37A7C` | u32 |
| `launch_x` | `0xB37A96` | u16 |
| `launch_y` | `0xB37A9F` | u16 |
| `launch_z` | `0xB37AB9` | u16 |
| `target_x` | `0xB37AD3` | u16 |
| `target_y` | `0xB37AED` | u16 |
| `target_z` | `0xB37B07` | u16 |
| `target_ent_id` | `0xB37B21` | u16 |
| `msec` | `0xB37B3B` | u16 |
| `shot0_impact1` | `0xB37B55` | u8 |
| `fx_opt` | `0xB37B6F` | u8 |
| `impact_grenade_id` | `0xB37B89` | u32 |
| `charge_lv` | `0xB37BA6` | u8 |
| `AI_ent_id` | `0xB37BC3` | u16 |
| `salvo_slot` | `0xB37BE0` | u8 |

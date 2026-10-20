# 汇编证据 —— CS-0x8898-battle-weapon_fire__damage_field

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3AD30 @ `0xb3ad30`（`0xb3ad30`..`0xb3b342`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__damage_field(` @ `0xee1080`
- opcode 写入：`0xb3adb1`
- 声明容量：`0x4A`（分配器容量 `push` @ `0xb3ad7b`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3ad7f  mov     ebx, eax
  0xb3ad81  mov     eax, [edi+0Ch]
  0xb3ad84  push    eax
  0xb3ad85  lea     ecx, [esp+50h+var_38]
  0xb3ad89  call    sub_ABB2F0
  0xb3ad8e  lea     eax, [ebx+4Ah]
  0xb3ad91  lea     ecx, [ebx+2]
  0xb3ad94  cmp     ecx, eax
  0xb3ad96  mov     [esp+4Ch+var_4], 0
  0xb3ad9e  mov     [esp+4Ch+var_34], ebx
  0xb3ada2  mov     dword ptr [esp+4Ch+var_30], eax
  0xb3ada6  ja      loc_B3B31A
  0xb3adac  lea     edx, [ecx+4]
  0xb3adaf  cmp     edx, eax
  0xb3adb1  mov     word ptr [ebx], 8898h
  0xb3adb6  ja      loc_B3B31A
  0xb3adbc  mov     esi, [ebp+arg_0]
  0xb3adbf  mov     [ecx], esi
  0xb3adc1  lea     ecx, [edx+2]
  0xb3adc4  cmp     ecx, eax
  0xb3adc6  ja      loc_B3B31A
  0xb3adcc  mov     ax, word ptr [ebp+arg_4]
  0xb3add0  mov     [esp+4Ch+var_34], ecx
  0xb3add4  lea     ecx, [esp+4Ch+var_34]
  0xb3add8  mov     [edx], ax
  0xb3addb  push    ecx
  0xb3addc  lea     edx, [ebp+arg_8]
  0xb3addf  push    edx
  0xb3ade0  call    sub_B02DA0
  0xb3ade5  add     esp, 8
  0xb3ade8  test    al, al
  0xb3adea  jz      loc_B3B31A
  0xb3adf0  lea     eax, [esp+4Ch+var_34]
  0xb3adf4  push    eax
  0xb3adf5  lea     ecx, [ebp+arg_C]
  0xb3adf8  push    ecx
  0xb3adf9  call    sub_B02DA0
  0xb3adfe  add     esp, 8
  0xb3ae01  test    al, al
  0xb3ae03  jz      loc_B3B31A
  0xb3ae09  lea     edx, [esp+4Ch+var_34]
  0xb3ae0d  push    edx
  0xb3ae0e  lea     eax, [ebp+arg_10]
  0xb3ae11  push    eax
  0xb3ae12  call    sub_B02DA0
  0xb3ae17  add     esp, 8
  0xb3ae1a  test    al, al
  0xb3ae1c  jz      loc_B3B31A
  0xb3ae22  lea     ecx, [esp+4Ch+var_34]
  0xb3ae26  push    ecx
  0xb3ae27  lea     edx, [ebp+arg_14]
  0xb3ae2a  push    edx
  0xb3ae2b  call    sub_B02DA0
  0xb3ae30  add     esp, 8
  0xb3ae33  test    al, al
  0xb3ae35  jz      loc_B3B31A
  0xb3ae3b  lea     eax, [esp+4Ch+var_34]
  0xb3ae3f  push    eax
  0xb3ae40  lea     ecx, [ebp+arg_18]
  0xb3ae43  push    ecx
  0xb3ae44  call    sub_B02DA0
  0xb3ae49  add     esp, 8
  0xb3ae4c  test    al, al
  0xb3ae4e  jz      loc_B3B31A
  0xb3ae54  lea     edx, [esp+4Ch+var_34]
  0xb3ae58  push    edx
  0xb3ae59  lea     eax, [ebp+arg_1C]
  0xb3ae5c  push    eax
  0xb3ae5d  call    sub_B02DA0
  0xb3ae62  add     esp, 8
  0xb3ae65  test    al, al
  0xb3ae67  jz      loc_B3B31A
  0xb3ae6d  lea     ecx, [esp+4Ch+var_34]
  0xb3ae71  push    ecx
  0xb3ae72  lea     edx, [ebp+arg_20]
  0xb3ae75  push    edx
  0xb3ae76  call    sub_B02DA0
  0xb3ae7b  add     esp, 8
  0xb3ae7e  test    al, al
  0xb3ae80  jz      loc_B3B31A
  0xb3ae86  lea     eax, [esp+4Ch+var_34]
  0xb3ae8a  push    eax
  0xb3ae8b  lea     ecx, [ebp+arg_24]
  0xb3ae8e  push    ecx
  0xb3ae8f  call    sub_B02DA0
  0xb3ae94  add     esp, 8
  0xb3ae97  test    al, al
  0xb3ae99  jz      loc_B3B31A
  0xb3ae9f  lea     edx, [esp+4Ch+var_34]
  0xb3aea3  push    edx
  0xb3aea4  lea     eax, [ebp+arg_28]
  0xb3aea7  push    eax
  0xb3aea8  call    sub_B02DA0
  0xb3aead  add     esp, 8
  0xb3aeb0  test    al, al
  0xb3aeb2  jz      loc_B3B31A
  0xb3aeb8  lea     ecx, [esp+4Ch+var_34]
  0xb3aebc  push    ecx
  0xb3aebd  lea     edx, [ebp+arg_2C]
  0xb3aec0  push    edx
  0xb3aec1  call    sub_B02DA0
  0xb3aec6  add     esp, 8
  0xb3aec9  test    al, al
  0xb3aecb  jz      loc_B3B31A
  0xb3aed1  lea     eax, [esp+4Ch+var_34]
  0xb3aed5  push    eax
  0xb3aed6  lea     ecx, [ebp+arg_30]
  0xb3aed9  push    ecx
  0xb3aeda  call    sub_B061C0
  0xb3aedf  add     esp, 8
  0xb3aee2  test    al, al
  0xb3aee4  jz      loc_B3B31A
  0xb3aeea  lea     edx, [esp+4Ch+var_34]
  0xb3aeee  push    edx
  0xb3aeef  lea     eax, [ebp+arg_34]
  0xb3aef2  push    eax
  0xb3aef3  call    sub_B061C0
  0xb3aef8  add     esp, 8
  0xb3aefb  test    al, al
  0xb3aefd  jz      loc_B3B31A
  0xb3af03  lea     ecx, [esp+4Ch+var_34]
  0xb3af07  push    ecx
  0xb3af08  lea     edx, [ebp+arg_38]
  0xb3af0b  push    edx
  0xb3af0c  call    sub_B02D80
  0xb3af11  add     esp, 8
  0xb3af14  test    al, al
  0xb3af16  jz      loc_B3B31A
  0xb3af1c  lea     eax, [esp+4Ch+var_34]
  0xb3af20  push    eax
  0xb3af21  lea     ecx, [ebp+arg_3C]
  0xb3af24  push    ecx
  0xb3af25  call    sub_B02D80
  0xb3af2a  add     esp, 8
  0xb3af2d  test    al, al
  0xb3af2f  jz      loc_B3B31A
  0xb3af35  lea     edx, [esp+4Ch+var_34]
  0xb3af39  push    edx
  0xb3af3a  lea     eax, [ebp+arg_40]
  0xb3af3d  push    eax
  0xb3af3e  call    sub_B061C0
  0xb3af43  add     esp, 8
  0xb3af46  test    al, al
  0xb3af48  jz      loc_B3B31A
  0xb3af4e  lea     ecx, [esp+4Ch+var_34]
  0xb3af52  push    ecx
  0xb3af53  lea     edx, [ebp+arg_44]
  0xb3af56  push    edx
  0xb3af57  call    sub_B02DA0
  0xb3af5c  add     esp, 8
  0xb3af5f  test    al, al
  0xb3af61  jz      loc_B3B31A
  0xb3af67  mov     esi, [edi+3E54h]
  0xb3af6d  test    esi, esi
  0xb3af6f  jz      loc_B3B2B8
  0xb3af75  lea     eax, [esp+4Ch+var_2C]
  0xb3af79  push    eax
  0xb3af7a  call    sub_CA0CE0
  0xb3af7f  add     esp, 4
  0xb3af82  mov     ecx, [edi+8]
  0xb3af85  push    offset aProtoBattleCli_206; ")<-_proto_battle_client::send_weapon_fi"...
  0xb3af8a  push    ecx
  0xb3af8b  push    offset aId; " (id:"
  0xb3af90  push    eax
  0xb3af91  push    esi
  0xb3af92  mov     byte ptr [esp+60h+var_4], 1
  0xb3af97  call    sub_B03020
  0xb3af9c  add     esp, 8
  0xb3af9f  push    eax
  0xb3afa0  call    sub_41D990
  0xb3afa5  add     esp, 8
  0xb3afa8  mov     ecx, eax
  0xb3afaa  call    sub_ADC810
  0xb3afaf  push    eax
  0xb3afb0  call    sub_41D990
  0xb3afb5  add     esp, 8
  0xb3afb8  lea     ecx, [esp+4Ch+var_2C]
  0xb3afbc  mov     byte ptr [esp+4Ch+var_4], 0
  0xb3afc1  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3afcf  push    offset aFrameCount; "frame_count="
  0xb3aff6  push    offset aLaunchX; "launch_x="
  0xb3b01d  push    offset aLaunchY; "launch_y="
  0xb3b044  push    offset aLaunchZ; "launch_z="
  0xb3b06b  push    offset aTarget1X; "target1_x="
  0xb3b092  push    offset aTarget1Y; "target1_y="
  0xb3b0b9  push    offset aTarget1Z; "target1_z="
  0xb3b0e0  push    offset aTarget2X; "target2_x="
  0xb3b107  push    offset aTarget2Y; "target2_y="
  0xb3b12e  push    offset aTarget2Z; "target2_z="
  0xb3b155  push    offset aTargetEntId; "target_ent_id="
  0xb3b17c  push    offset aMsec; "msec="
  0xb3b1a3  push    offset aShot0Impact1; "shot0_impact1="
  0xb3b1cc  push    offset aFxOpt; "fx_opt="
  0xb3b1f5  push    offset aImpactGrenadeI; "impact_grenade_id="
  0xb3b21c  push    offset aParentGrenadeI; "parent_grenade_id="
  0xb3b243  push    offset aChargeLv; "charge_lv="
  0xb3b267  push    offset aAiEntId; "AI_ent_id="
  0xb3b280  push    offset aByte; "]byte"
  0xb3b288  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb3b2be  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3adb1` | u16 |
| `frame_count` | `0xB3ADBF` | u32 |
| `launch_x` | `0xB3ADD8` | u16 |
| `launch_y` | `0xB3ADE0` | u16 |
| `launch_z` | `0xB3ADF9` | u16 |
| `target1_x` | `0xB3AE12` | u16 |
| `target1_y` | `0xB3AE2B` | u16 |
| `target1_z` | `0xB3AE44` | u16 |
| `target2_x` | `0xB3AE5D` | u16 |
| `target2_y` | `0xB3AE76` | u16 |
| `target2_z` | `0xB3AE8F` | u16 |
| `target_ent_id` | `0xB3AEA8` | u16 |
| `msec` | `0xB3AEC1` | u16 |
| `shot0_impact1` | `0xB3AEDA` | u8 |
| `fx_opt` | `0xB3AEF3` | u8 |
| `impact_grenade_id` | `0xB3AF0C` | u32 |
| `parent_grenade_id` | `0xB3AF25` | u32 |
| `charge_lv` | `0xB3AF3E` | u8 |
| `AI_ent_id` | `0xB3AF57` | u16 |

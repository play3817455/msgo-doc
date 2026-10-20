# 汇编证据 —— CS-0x770D-battle-weapon_hit_to

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3B7A0 @ `0xb3b7a0`（`0xb3b7a0`..`0xb3c282`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_hit_to(` @ `0xee10f8`
- opcode 写入：`0xb3b82a`
- 声明容量：`0x14E`（分配器容量 `push` @ `0xb3b7ea`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb3b7f1  mov     esi, eax
  0xb3b7f3  mov     eax, [edi+0Ch]
  0xb3b7f6  push    eax
  0xb3b7f7  lea     ecx, [esp+54h+var_3C]
  0xb3b7fb  mov     [esp+54h+var_34], esi
  0xb3b7ff  call    sub_ABB2F0
  0xb3b804  lea     ecx, [esi+14Eh]
  0xb3b80a  lea     eax, [esi+2]
  0xb3b80d  cmp     eax, ecx
  0xb3b80f  mov     [esp+50h+var_4], 0
  0xb3b817  mov     [esp+50h+var_30], esi
  0xb3b81b  mov     dword ptr [esp+50h+var_2C], ecx
  0xb3b81f  ja      loc_B3C26D
  0xb3b825  lea     edx, [eax+8]
  0xb3b828  cmp     edx, ecx
  0xb3b82a  mov     word ptr [esi], 770Dh
  0xb3b82f  ja      loc_B3C26D
  0xb3b835  mov     esi, [esp+50h+arg_0]
  0xb3b839  mov     [eax], esi
  0xb3b83b  mov     esi, [esp+50h+arg_4]
  0xb3b83f  mov     [eax+4], esi
  0xb3b842  lea     eax, [edx+4]
  0xb3b845  cmp     eax, ecx
  0xb3b847  ja      loc_B3C26D
  0xb3b84d  mov     ecx, [esp+50h+arg_8]
  0xb3b851  mov     [edx], ecx
  0xb3b853  lea     edx, [esp+50h+var_30]
  0xb3b857  mov     [esp+50h+var_30], eax
  0xb3b85b  push    edx
  0xb3b85c  lea     eax, [esp+54h+arg_C]
  0xb3b860  push    eax
  0xb3b861  call    sub_B02D80
  0xb3b866  add     esp, 8
  0xb3b869  test    al, al
  0xb3b86b  jz      loc_B3C26D
  0xb3b871  lea     ecx, [esp+50h+var_30]
  0xb3b875  push    ecx
  0xb3b876  lea     edx, [esp+54h+arg_10]
  0xb3b87a  push    edx
  0xb3b87b  call    sub_B02D80
  0xb3b880  add     esp, 8
  0xb3b883  test    al, al
  0xb3b885  jz      loc_B3C26D
  0xb3b88b  mov     ebp, [esp+50h+arg_18]
  0xb3b88f  cmp     ebp, 10h
  0xb3b892  ja      loc_B3C26D
  0xb3b898  lea     eax, [esp+50h+var_30]
  0xb3b89c  push    eax
  0xb3b89d  lea     ecx, [esp+54h+arg_18]
  0xb3b8a1  push    ecx
  0xb3b8a2  call    sub_B02D80
  0xb3b8a7  add     esp, 8
  0xb3b8aa  test    al, al
  0xb3b8ac  jz      loc_B3C26D
  0xb3b8b2  xor     esi, esi
  0xb3b8b4  test    ebp, ebp
  0xb3b8b6  jbe     short loc_B3B8E0
  0xb3b8b8  mov     edi, [esp+50h+arg_14]
  0xb3b8bc  lea     esp, [esp+0]
  0xb3b8c0  lea     edx, [esp+50h+var_30]
  0xb3b8c4  push    edx
  0xb3b8c5  push    edi
  0xb3b8c6  call    sub_B02DA0
  0xb3b8cb  add     esp, 8
  0xb3b8ce  test    al, al
  0xb3b8d0  jz      loc_B3C26D
  0xb3b8d6  add     esi, 1
  0xb3b8d9  add     edi, 2
  0xb3b8dc  cmp     esi, ebp
  0xb3b8de  jb      short loc_B3B8C0
  0xb3b8e0  mov     ebx, [esp+50h+arg_20]
  0xb3b8e4  cmp     ebx, 10h
  0xb3b8e7  ja      loc_B3C26D
  0xb3b8ed  lea     eax, [esp+50h+var_30]
  0xb3b8f1  push    eax
  0xb3b8f2  lea     ecx, [esp+54h+arg_20]
  0xb3b8f6  push    ecx
  0xb3b8f7  call    sub_B02D80
  0xb3b8fc  add     esp, 8
  0xb3b8ff  test    al, al
  0xb3b901  jz      loc_B3C26D
  0xb3b907  xor     esi, esi
  0xb3b909  test    ebx, ebx
  0xb3b90b  jbe     short loc_B3B931
  0xb3b90d  mov     edi, [esp+50h+arg_1C]
  0xb3b911  lea     edx, [esp+50h+var_30]
  0xb3b915  push    edx
  0xb3b916  push    edi
  0xb3b917  call    sub_B02DA0
  0xb3b91c  add     esp, 8
  0xb3b91f  test    al, al
  0xb3b921  jz      loc_B3C26D
  0xb3b927  add     esi, 1
  0xb3b92a  add     edi, 2
  0xb3b92d  cmp     esi, ebx
  0xb3b92f  jb      short loc_B3B911
  0xb3b931  mov     edi, [esp+50h+arg_28]
  0xb3b935  cmp     edi, 10h
  0xb3b938  ja      loc_B3C26D
  0xb3b93e  lea     eax, [esp+50h+var_30]
  0xb3b942  push    eax
  0xb3b943  lea     ecx, [esp+54h+arg_28]
  0xb3b94a  push    ecx
  0xb3b94b  call    sub_B02D80
  0xb3b950  add     esp, 8
  0xb3b953  test    al, al
  0xb3b955  jz      loc_B3C26D
  0xb3b95b  xor     esi, esi
  0xb3b95d  test    edi, edi
  0xb3b95f  jbe     short loc_B3B987
  0xb3b961  mov     edi, [esp+50h+arg_24]
  0xb3b965  lea     edx, [esp+50h+var_30]
  0xb3b969  push    edx
  0xb3b96a  push    edi
  0xb3b96b  call    sub_B02DA0
  0xb3b970  add     esp, 8
  0xb3b973  test    al, al
  0xb3b975  jz      loc_B3C26D
  0xb3b97b  add     esi, 1
  0xb3b97e  add     edi, 2
  0xb3b981  cmp     esi, [esp+50h+arg_28]
  0xb3b985  jb      short loc_B3B965
  0xb3b987  mov     edi, [esp+50h+arg_30]
  0xb3b98e  cmp     edi, 10h
  0xb3b991  ja      loc_B3C26D
  0xb3b997  lea     eax, [esp+50h+var_30]
  0xb3b99b  push    eax
  0xb3b99c  lea     ecx, [esp+54h+arg_30]
  0xb3b9a3  push    ecx
  0xb3b9a4  call    sub_B02D80
  0xb3b9a9  add     esp, 8
  0xb3b9ac  test    al, al
  0xb3b9ae  jz      loc_B3C26D
  0xb3b9b4  xor     esi, esi
  0xb3b9b6  test    edi, edi
  0xb3b9b8  jbe     short loc_B3B9E6
  0xb3b9ba  mov     edi, [esp+50h+arg_2C]
  0xb3b9c1  lea     edx, [esp+50h+var_30]
  0xb3b9c5  push    edx
  0xb3b9c6  push    edi
  0xb3b9c7  call    sub_B02DA0
  0xb3b9cc  add     esp, 8
  0xb3b9cf  test    al, al
  0xb3b9d1  jz      loc_B3C26D
  0xb3b9d7  add     esi, 1
  0xb3b9da  add     edi, 2
  0xb3b9dd  cmp     esi, [esp+50h+arg_30]
  0xb3b9e4  jb      short loc_B3B9C1
  0xb3b9e6  mov     edi, [esp+50h+arg_38]
  0xb3b9ed  cmp     edi, 10h
  0xb3b9f0  ja      loc_B3C26D
  0xb3b9f6  lea     eax, [esp+50h+var_30]
  0xb3b9fa  push    eax
  0xb3b9fb  lea     ecx, [esp+54h+arg_38]
  0xb3ba02  push    ecx
  0xb3ba03  call    sub_B02D80
  0xb3ba08  add     esp, 8
  0xb3ba0b  test    al, al
  0xb3ba0d  jz      loc_B3C26D
  0xb3ba13  xor     esi, esi
  0xb3ba15  test    edi, edi
  0xb3ba17  jbe     short loc_B3BA45
  0xb3ba19  mov     edi, [esp+50h+arg_34]
  0xb3ba20  lea     edx, [esp+50h+var_30]
  0xb3ba24  push    edx
  0xb3ba25  push    edi
  0xb3ba26  call    sub_B02DA0
  0xb3ba2b  add     esp, 8
  0xb3ba2e  test    al, al
  0xb3ba30  jz      loc_B3C26D
  0xb3ba36  add     esi, 1
  0xb3ba39  add     edi, 2
  0xb3ba3c  cmp     esi, [esp+50h+arg_38]
  0xb3ba43  jb      short loc_B3BA20
  0xb3ba45  mov     edi, [esp+50h+arg_40]
  0xb3ba4c  cmp     edi, 10h
  0xb3ba4f  ja      loc_B3C26D
  0xb3ba55  lea     eax, [esp+50h+var_30]
  0xb3ba59  push    eax
  0xb3ba5a  lea     ecx, [esp+54h+arg_40]
  0xb3ba61  push    ecx
  0xb3ba62  call    sub_B02D80
  0xb3ba67  add     esp, 8
  0xb3ba6a  test    al, al
  0xb3ba6c  jz      loc_B3C26D
  0xb3ba72  xor     esi, esi
  0xb3ba74  test    edi, edi
  0xb3ba76  jbe     short loc_B3BAA5
  0xb3ba78  mov     edi, [esp+50h+arg_3C]
  0xb3ba7f  nop
  0xb3ba80  lea     edx, [esp+50h+var_30]
  0xb3ba84  push    edx
  0xb3ba85  push    edi
  0xb3ba86  call    sub_B02DA0
  0xb3ba8b  add     esp, 8
  0xb3ba8e  test    al, al
  0xb3ba90  jz      loc_B3C26D
  0xb3ba96  add     esi, 1
  0xb3ba99  add     edi, 2
  0xb3ba9c  cmp     esi, [esp+50h+arg_40]
  0xb3baa3  jb      short loc_B3BA80
  0xb3baa5  mov     edi, [esp+50h+arg_48]
  0xb3baac  cmp     edi, 10h
  0xb3baaf  ja      loc_B3C26D
  0xb3bab5  lea     eax, [esp+50h+var_30]
  0xb3bab9  push    eax
  0xb3baba  lea     ecx, [esp+54h+arg_48]
  0xb3bac1  push    ecx
  0xb3bac2  call    sub_B02D80
  0xb3bac7  add     esp, 8
  0xb3baca  test    al, al
  0xb3bacc  jz      loc_B3C26D
  0xb3bad2  xor     esi, esi
  0xb3bad4  test    edi, edi
  0xb3bad6  jbe     short loc_B3BB05
  0xb3bad8  mov     edi, [esp+50h+arg_44]
  0xb3badf  nop
  0xb3bae0  lea     edx, [esp+50h+var_30]
  0xb3bae4  push    edx
  0xb3bae5  push    edi
  0xb3bae6  call    sub_B02DA0
  0xb3baeb  add     esp, 8
  0xb3baee  test    al, al
  0xb3baf0  jz      loc_B3C26D
  0xb3baf6  add     esi, 1
  0xb3baf9  add     edi, 2
  0xb3bafc  cmp     esi, [esp+50h+arg_48]
  0xb3bb03  jb      short loc_B3BAE0
  0xb3bb05  mov     edi, dword ptr [esp+50h+arg_50]
  0xb3bb0c  cmp     edi, 10h
  0xb3bb0f  ja      loc_B3C26D
  0xb3bb15  lea     eax, [esp+50h+var_30]
  0xb3bb19  push    eax
  0xb3bb1a  lea     ecx, [esp+54h+arg_50]
  0xb3bb21  push    ecx
  0xb3bb22  call    sub_B02D80
  0xb3bb27  add     esp, 8
  0xb3bb2a  test    al, al
  0xb3bb2c  jz      loc_B3C26D
  0xb3bb32  xor     esi, esi
  0xb3bb34  test    edi, edi
  0xb3bb36  jbe     short loc_B3BB65
  0xb3bb38  mov     edi, [esp+50h+arg_4C]
  0xb3bb3f  nop
  0xb3bb40  lea     edx, [esp+50h+var_30]
  0xb3bb44  push    edx
  0xb3bb45  push    edi
  0xb3bb46  call    sub_B02DA0
  0xb3bb4b  add     esp, 8
  0xb3bb4e  test    al, al
  0xb3bb50  jz      loc_B3C26D
  0xb3bb56  add     esi, 1
  0xb3bb59  add     edi, 2
  0xb3bb5c  cmp     esi, dword ptr [esp+50h+arg_50]
  0xb3bb63  jb      short loc_B3BB40
  0xb3bb65  lea     eax, [esp+50h+var_30]
  0xb3bb69  push    eax
  0xb3bb6a  lea     ecx, [esp+54h+arg_54]
  0xb3bb71  push    ecx
  0xb3bb72  call    sub_B061C0
  0xb3bb77  add     esp, 8
  0xb3bb7a  test    al, al
  0xb3bb7c  jz      loc_B3C26D
  0xb3bb82  lea     edx, [esp+50h+var_30]
  0xb3bb86  push    edx
  0xb3bb87  lea     eax, [esp+54h+arg_58]
  0xb3bb8e  push    eax
  0xb3bb8f  call    sub_B02DA0
  0xb3bb94  add     esp, 8
  0xb3bb97  test    al, al
  0xb3bb99  jz      loc_B3C26D
  0xb3bb9f  lea     ecx, [esp+50h+var_30]
  0xb3bba3  push    ecx
  0xb3bba4  lea     edx, [esp+54h+arg_5C]
  0xb3bbab  push    edx
  0xb3bbac  call    sub_B02DA0
  0xb3bbb1  add     esp, 8
  0xb3bbb4  test    al, al
  0xb3bbb6  jz      loc_B3C26D
  0xb3bbbc  lea     eax, [esp+50h+var_30]
  0xb3bbc0  push    eax
  0xb3bbc1  lea     ecx, [esp+54h+arg_60]
  0xb3bbc8  push    ecx
  0xb3bbc9  call    sub_B02D80
  0xb3bbce  add     esp, 8
  0xb3bbd1  test    al, al
  0xb3bbd3  jz      loc_B3C26D
  0xb3bbd9  lea     edx, [esp+50h+var_30]
  0xb3bbdd  push    edx
  0xb3bbde  lea     eax, [esp+54h+arg_64]
  0xb3bbe5  push    eax
  0xb3bbe6  call    sub_B061C0
  0xb3bbeb  add     esp, 8
  0xb3bbee  test    al, al
  0xb3bbf0  jz      loc_B3C26D
  0xb3bbf6  lea     ecx, [esp+50h+var_30]
  0xb3bbfa  push    ecx
  0xb3bbfb  lea     edx, [esp+54h+arg_68]
  0xb3bc02  push    edx
  0xb3bc03  call    sub_B061C0
  0xb3bc08  add     esp, 8
  0xb3bc0b  test    al, al
  0xb3bc0d  jz      loc_B3C26D
  0xb3bc13  mov     eax, [esp+50h+var_38]
  0xb3bc17  mov     esi, [eax+3E64h]
  0xb3bc1d  test    esi, esi
  0xb3bc1f  jz      loc_B3C202
  0xb3bc25  lea     ecx, [esp+50h+var_28]
  0xb3bc29  push    ecx
  0xb3bc2a  call    sub_CA0CE0
  0xb3bc2f  add     esp, 4
  0xb3bc32  mov     edx, [esp+50h+var_38]
  0xb3bc36  mov     ecx, [edx+8]
  0xb3bc39  push    offset aProtoBattleCli_242; ")<-_proto_battle_client::send_weapon_hi"...
  0xb3bc3e  push    ecx
  0xb3bc3f  push    offset aId; " (id:"
  0xb3bc44  push    eax
  0xb3bc45  push    esi
  0xb3bc46  mov     byte ptr [esp+64h+var_4], 1
  0xb3bc4b  call    sub_B03020
  0xb3bc50  add     esp, 8
  0xb3bc53  push    eax
  0xb3bc54  call    sub_41D990
  0xb3bc59  add     esp, 8
  0xb3bc5c  mov     ecx, eax
  0xb3bc5e  call    sub_ADC810
  0xb3bc63  push    eax
  0xb3bc64  call    sub_41D990
  0xb3bc69  add     esp, 8
  0xb3bc6c  lea     ecx, [esp+50h+var_28]
  0xb3bc70  mov     byte ptr [esp+50h+var_4], 0
  0xb3bc75  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3bc89  push    offset aPhash; "phash="
  0xb3bcb1  push    offset aFrameCount; "frame_count="
  0xb3bcd9  push    offset aWeaponItemid; "weapon_itemid="
  0xb3bd01  push    offset aFireId; "fire_id="
  0xb3bd1c  push    offset aEntIds; "ent_ids={"
  0xb3bd84  push    offset aHitPosX_0; "hit_pos_x={"
  0xb3bded  push    offset aHitPosY_0; "hit_pos_y={"
  0xb3be5d  push    offset aHitPosZ_0; "hit_pos_z={"
  0xb3becd  push    offset aHitDirs; "hit_dirs={"
  0xb3bf3d  push    offset aHitDistance; "hit_distance={"
  0xb3bfad  push    offset aBodyDistance; "body_distance={"
  0xb3c01d  push    offset aBodyRegions; "body_regions={"
  0xb3c08d  push    offset aChargeLv; "charge_lv="
  0xb3c0c8  push    offset aAiEntId; "AI_ent_id="
  0xb3c0f3  push    offset aInstateFromEnt; "instate_from_ent_id="
  0xb3c11e  push    offset aCreateFrameCou; "create_frame_count="
  0xb3c139  push    offset aIsDownRange; "is_down_range="
  0xb3c164  push    offset aIsWrestleFirst; "is_wrestle_first_high_lockon="
  0xb3c18a  push    offset aByte; "]byte"
  0xb3c190  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb3bca4  mov     ecx, [esp+58h+arg_8]
  0xb3bccc  mov     edx, [esp+58h+arg_C]
  0xb3bcf4  mov     eax, [esp+58h+arg_10]
  0xb3c0b8  mov     edx, [esp+58h+arg_58]
  0xb3c0e3  mov     eax, [esp+58h+arg_5C]
  0xb3c10e  mov     ecx, dword ptr [esp+58h+arg_60]
  0xb3c210  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb3b82a` | u16 |
| `phash` | `0xB3B839, 0xB3B83F` | u64 |
| `frame_count` | `0xB3B851` | u32 |
| `weapon_itemid` | `0xB3B861` | u32 |
| `fire_id` | `0xB3B87B` | u32 |
| `ent_ids_num` | `0xB3B8A2` | u32 |
| `ent_ids` | `0xB3B8C6 (loop @0xB3B8C0..0xB3B8DE)` | array<u16,N> |
| `hit_pos_x_num` | `0xB3B8F7` | u32 |
| `hit_pos_x` | `0xB3B917 (loop @0xB3B911..0xB3B92F)` | array<u16,N> |
| `hit_pos_y_num` | `0xB3B94B` | u32 |
| `hit_pos_y` | `0xB3B96B (loop @0xB3B965..0xB3B985)` | array<u16,N> |
| `hit_pos_z_num` | `0xB3B9A4` | u32 |
| `hit_pos_z` | `0xB3B9C7 (loop @0xB3B9C1..0xB3B9E4)` | array<u16,N> |
| `hit_dirs_num` | `0xB3BA03` | u32 |
| `hit_dirs` | `0xB3BA26 (loop @0xB3BA20..0xB3BA43)` | array<u16,N> |
| `hit_distance_num` | `0xB3BA62` | u32 |
| `hit_distance` | `0xB3BA86 (loop @0xB3BA80..0xB3BAA3)` | array<u16,N> |
| `body_distance_num` | `0xB3BAC2` | u32 |
| `body_distance` | `0xB3BAE6 (loop @0xB3BAE0..0xB3BB03)` | array<u16,N> |
| `body_regions_num` | `0xB3BB22` | u32 |
| `body_regions` | `0xB3BB46 (loop @0xB3BB40..0xB3BB63)` | array<u16,N> |
| `charge_lv` | `0xB3BB72` | u8 |
| `AI_ent_id` | `0xB3BB8F` | u16 |
| `instate_from_ent_id` | `0xB3BBAC` | u16 |
| `create_frame_count` | `0xB3BBC9` | u32 |
| `is_down_range` | `0xB3BBE6` | u8 |
| `is_wrestle_first_high_lockon` | `0xB3BC03` | u8 |

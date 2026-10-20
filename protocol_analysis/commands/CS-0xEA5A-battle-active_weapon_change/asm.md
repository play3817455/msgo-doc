# 汇编证据 —— CS-0xEA5A-battle-active_weapon_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B360B0`（`0x00B360B0`..`0x00B362E9`），函数 `sub_B360B0`
- 命令名字符串：`)<-_proto_battle_client::send_active_weapon_change(` @ `0x00EE0BEC`
- opcode 写入：`0x00B3612C`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B360F6`）
- 提交（`sub_B02FF0`）：`0x00B361CB`
- 发送去向：`vt[0x58]` @ `0x00B36278`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B360FF  push    eax
  00B36100  lea     ecx, [esp+4Ch+var_34]
  00B36104  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B36109  lea     eax, [ebp+0Eh]
  00B3610C  lea     ecx, [ebp+2]
  00B3610F  cmp     ecx, eax
  00B36111  mov     [esp+48h+var_4], 0
  00B36119  mov     [esp+48h+var_30], ebp
  00B3611D  mov     dword ptr [esp+48h+var_2C], eax
  00B36121  ja      loc_B362D4
  00B36127  lea     edx, [ecx+4]
  00B3612A  cmp     edx, eax
  00B3612C  mov     word ptr [ebp+0], 0EA5Ah   ; <<< 内联写线（u16）
  00B36132  ja      loc_B362D4
  00B36138  mov     esi, dword ptr [esp+48h+arg_0]
  00B3613C  mov     [ecx], esi   ; <<< 内联写线（u32）
  00B3613E  lea     ecx, [edx+1]
  00B36141  cmp     ecx, eax
  00B36143  ja      loc_B362D4
  00B36149  mov     al, byte ptr [esp+48h+arg_4]
  00B3614D  mov     [esp+48h+var_30], ecx
  00B36151  lea     ecx, [esp+48h+var_30]
  00B36155  mov     [edx], al   ; <<< 内联写线（u8）
  00B36157  push    ecx
  00B36158  lea     edx, [esp+4Ch+arg_8]
  00B3615C  push    edx
  00B3615D  call    sub_B02DA0   ; <<< 写线原语 u16
  00B36162  add     esp, 8
  00B36165  test    al, al
  00B36167  jz      loc_B362D4
  00B3616D  mov     esi, [edi+3DB4h]
  00B36173  test    esi, esi
  00B36175  mov     ebx, [esp+48h+var_30]
  00B36179  jz      loc_B36276
  00B3617F  lea     eax, [esp+48h+var_28]
  00B36183  push    eax
  00B36184  call    sub_CA0CE0
  00B36189  add     esp, 4
  00B3618C  mov     ecx, [edi+8]
  00B3618F  push    offset aProtoBattleCli_239
  00B36194  push    ecx
  00B36195  push    offset aId
  00B3619A  push    eax
  00B3619B  push    esi
  00B3619C  mov     byte ptr [esp+5Ch+var_4], 1
  00B361A1  call    sub_B03020
  00B361A6  add     esp, 8
  00B361A9  push    eax
  00B361AA  call    sub_41D990
  00B361AF  add     esp, 8
  00B361B2  mov     ecx, eax
  00B361B4  call    sub_ADC810
  00B361B9  push    eax
  00B361BA  call    sub_41D990
  00B361BF  add     esp, 8
  00B361C2  lea     ecx, [esp+48h+var_28]
  00B361C6  mov     byte ptr [esp+48h+var_4], 0
  00B361CB  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B361CB  call    sub_B02FF0
  00B361D0  mov     edx, dword ptr [esp+48h+arg_0]
  00B361D4  push    offset word_F641DC
  00B361D9  push    edx
  00B361DA  push    offset aFrameCount
  00B361DF  push    esi
  00B361E0  call    sub_41D990
  00B361E5  add     esp, 8
  00B361E8  mov     ecx, eax
  00B361EA  call    sub_B03580
  00B361EF  push    eax
  00B361F0  call    sub_41D990
  00B361F5  add     esp, 8
  00B361F8  push    offset word_F641DC
  00B361FD  lea     eax, [esp+4Ch+arg_4]
  00B36201  push    eax
  00B36202  push    offset aEquipIndex
  00B36207  push    esi
  00B36208  call    sub_41D990
  00B3620D  add     esp, 8
  00B36210  push    eax
  00B36211  call    sub_B0C1F0
  00B36216  add     esp, 8
  00B36219  push    eax
  00B3621A  call    sub_41D990
  00B3621F  mov     ecx, [esp+50h+arg_8]
  00B36223  add     esp, 8
  00B36226  push    ecx
  00B36227  push    offset aAiEntId
  00B3622C  push    esi
  00B3622D  call    sub_41D990
  00B36232  add     esp, 8
  00B36235  mov     ecx, eax
  00B36237  call    sub_B032A0
  00B3623C  push    offset aByte
  00B36241  mov     edx, ebx
  00B36243  sub     edx, ebp
  00B36245  push    edx
  00B36246  push    offset asc_EDAD58
  00B3624B  push    esi
  00B3624C  call    sub_41D990
  00B36251  add     esp, 8
  00B36254  mov     ecx, eax
  00B36256  call    sub_B03580
  00B3625B  push    eax
  00B3625C  call    sub_41D990
  00B36261  add     esp, 8
  00B36264  mov     esi, eax
  00B36266  push    0Ah
  00B36268  mov     ecx, esi
  00B3626A  call    sub_B036E0
  00B3626F  mov     ecx, esi
  00B36271  call    sub_40DDF0
  00B36276  mov     eax, [edi]
  00B36278  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B36276  mov     eax, [edi]
  00B36278  mov     edx, [eax+58h]
  00B3627B  mov     esi, ebx
  00B3627D  sub     esi, ebp
  00B3627F  push    esi
  00B36280  push    ebp
  00B36281  mov     ecx, edi
  00B36283  call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B3612C` | u16 / 2 |
| `frame_count` | `0xB36138`;`0xB3613C` | u32 / 4 |
| `equip_index` | `0xB36149`;`0xB36155` | u8 / 1 |
| `AI_ent_id` | `0xB3615D` | u16 / 2 |

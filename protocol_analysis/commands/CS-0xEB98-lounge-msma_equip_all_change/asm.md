# 汇编证据 —— CS-0xEB98-lounge-msma_equip_all_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B992A0`（`0x00B992A0`..`0x00B994B3`），函数 `sub_B992A0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_all_change(` @ `0x00EEBD1C`
- opcode 写入：`0x00B99322`
- 声明容量：`0x86`（分配器容量 `push` @ `0x00B992E6`）
- 提交（`sub_B02FF0`）：`0x00B993B7`
- 发送去向：`vt[0x58]` @ `0x00B99441`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B992F2  push    eax
  00B992F3  lea     ecx, [esp+4Ch+var_34]
  00B992F7  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B992FC  lea     ecx, [ebp+86h]
  00B99302  lea     eax, [ebp+2]
  00B99305  cmp     eax, ecx
  00B99307  mov     [esp+48h+var_4], 0
  00B9930F  mov     [esp+48h+var_30], ebp
  00B99313  mov     dword ptr [esp+48h+var_2C], ecx
  00B99317  ja      loc_B9949E
  00B9931D  lea     edx, [eax+8]
  00B99320  cmp     edx, ecx
  00B99322  mov     word ptr [ebp+0], 0EB98h   ; <<< 内联写线（u16）
  00B99328  ja      loc_B9949E
  00B9932E  mov     ecx, [esp+48h+arg_0]
  00B99332  mov     [eax], ecx   ; <<< 内联写线（u32）
  00B99334  mov     ecx, [esp+48h+arg_4]
  00B99338  mov     [esp+48h+var_30], edx
  00B9933C  lea     edx, [esp+48h+var_30]
  00B99340  mov     [eax+4], ecx   ; <<< 内联写线（u32）
  00B99343  mov     eax, [esp+48h+arg_8]
  00B99347  push    edx
  00B99348  push    eax
  00B99349  call    sub_B41C60   ; <<< 复合写入器
  00B9934E  add     esp, 8
  00B99351  test    al, al
  00B99353  jz      loc_B9949E
  00B99359  mov     esi, [edi+7E7Ch]
  00B9935F  test    esi, esi
  00B99361  mov     ebx, [esp+48h+var_30]
  00B99365  jz      loc_B9943F
  00B9936B  lea     ecx, [esp+48h+var_28]
  00B9936F  push    ecx
  00B99370  call    sub_CA0CE0
  00B99375  add     esp, 4
  00B99378  mov     edx, [edi+8]
  00B9937B  push    offset aProtoLoungeCli_438
  00B99380  push    edx
  00B99381  push    offset aId
  00B99386  push    eax
  00B99387  push    esi
  00B99388  mov     byte ptr [esp+5Ch+var_4], 1
  00B9938D  call    sub_B03020
  00B99392  add     esp, 8
  00B99395  push    eax
  00B99396  call    sub_41D990
  00B9939B  add     esp, 8
  00B9939E  mov     ecx, eax
  00B993A0  call    sub_ADC810
  00B993A5  push    eax
  00B993A6  call    sub_41D990
  00B993AB  add     esp, 8
  00B993AE  lea     ecx, [esp+48h+var_28]
  00B993B2  mov     byte ptr [esp+48h+var_4], 0
  00B993B7  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B993B7  call    sub_B02FF0
  00B993BC  mov     eax, [esp+48h+arg_4]
  00B993C0  mov     ecx, [esp+48h+arg_0]
  00B993C4  push    offset word_F641DC
  00B993C9  push    eax
  00B993CA  push    ecx
  00B993CB  push    offset aUniqidMs
  00B993D0  push    esi
  00B993D1  call    sub_41D990
  00B993D6  add     esp, 8
  00B993D9  mov     ecx, eax
  00B993DB  call    sub_B08500
  00B993E0  push    eax
  00B993E1  call    sub_41D990
  00B993E6  mov     edx, [esp+50h+arg_8]
  00B993EA  add     esp, 8
  00B993ED  push    edx
  00B993EE  push    offset aEquipSet
  00B993F3  push    esi
  00B993F4  call    sub_41D990
  00B993F9  add     esp, 8
  00B993FC  push    eax
  00B993FD  call    sub_B4AA30
  00B99402  add     esp, 8
  00B99405  push    offset aByte
  00B9940A  mov     eax, ebx
  00B9940C  sub     eax, ebp
  00B9940E  push    eax
  00B9940F  push    offset asc_EDAD58
  00B99414  push    esi
  00B99415  call    sub_41D990
  00B9941A  add     esp, 8
  00B9941D  mov     ecx, eax
  00B9941F  call    sub_B03580
  00B99424  push    eax
  00B99425  call    sub_41D990
  00B9942A  add     esp, 8
  00B9942D  mov     esi, eax
  00B9942F  push    0Ah
  00B99431  mov     ecx, esi
  00B99433  call    sub_B036E0
  00B99438  mov     ecx, esi
  00B9943A  call    sub_40DDF0
  00B9943F  mov     edx, [edi]
  00B99441  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00B9943F  mov     edx, [edi]
  00B99441  mov     eax, [edx+58h]
  00B99444  sub     ebx, ebp
  00B99446  push    ebx
  00B99447  push    ebp
  00B99448  mov     ecx, edi
  00B9944A  call    eax
  00B9944C  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B99322` | u16 / 2 |
| `uniqid_ms` | `0xB99332`;`0xB99340` | u64 / 8 |
| `equip_set` | `0xB99349` | bytes / 121 |

# 汇编证据 —— CS-0xDF37-lounge-msma_weapon_buildup_extra_cnt_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B96C30`（`0x00B96C30`..`0x00B96E24`），函数 `sub_B96C30`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_buildup_extra_cnt_update(` @ `0x00EEB968`
- opcode 写入：`0x00B96CA4`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B96C76`）
- 提交（`sub_B02FF0`）：`0x00B96D2A`
- 发送去向：`vt[0x58]` @ `0x00B96DB2`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B96C7F  push    eax
  00B96C80  lea     ecx, [esp+44h+var_2C]
  00B96C84  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B96C89  lea     ecx, [ebp+0Eh]
  00B96C8C  lea     eax, [ebp+2]
  00B96C8F  cmp     eax, ecx
  00B96C91  mov     [esp+40h+var_4], 0
  00B96C99  ja      loc_B96E0F
  00B96C9F  lea     edx, [eax+8]
  00B96CA2  cmp     edx, ecx
  00B96CA4  mov     word ptr [ebp+0], 0DF37h   ; <<< 内联写线（u16）
  00B96CAA  ja      loc_B96E0F
  00B96CB0  mov     esi, [esp+40h+arg_0]
  00B96CB4  mov     [eax], esi   ; <<< 内联写线（u32）
  00B96CB6  mov     esi, [esp+40h+arg_4]
  00B96CBA  lea     ebx, [edx+2]
  00B96CBD  cmp     ebx, ecx
  00B96CBF  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00B96CC2  ja      loc_B96E0F
  00B96CC8  mov     cx, word ptr [esp+40h+arg_8]
  00B96CCD  mov     [edx], cx   ; <<< 内联写线（u16）
  00B96CD0  mov     esi, [edi+7DECh]
  00B96CD6  test    esi, esi
  00B96CD8  jz      loc_B96DB0
  00B96CDE  lea     edx, [esp+40h+var_28]
  00B96CE2  push    edx
  00B96CE3  call    sub_CA0CE0
  00B96CE8  add     esp, 4
  00B96CEB  mov     ecx, [edi+8]
  00B96CEE  push    offset aProtoLoungeCli_456
  00B96CF3  push    ecx
  00B96CF4  push    offset aId
  00B96CF9  push    eax
  00B96CFA  push    esi
  00B96CFB  mov     byte ptr [esp+54h+var_4], 1
  00B96D00  call    sub_B03020
  00B96D05  add     esp, 8
  00B96D08  push    eax
  00B96D09  call    sub_41D990
  00B96D0E  add     esp, 8
  00B96D11  mov     ecx, eax
  00B96D13  call    sub_ADC810
  00B96D18  push    eax
  00B96D19  call    sub_41D990
  00B96D1E  add     esp, 8
  00B96D21  lea     ecx, [esp+40h+var_28]
  00B96D25  mov     byte ptr [esp+40h+var_4], 0
  00B96D2A  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B96D2A  call    sub_B02FF0
  00B96D2F  mov     edx, [esp+40h+arg_4]
  00B96D33  mov     eax, [esp+40h+arg_0]
  00B96D37  push    offset word_F641DC
  00B96D3C  push    edx
  00B96D3D  push    eax
  00B96D3E  push    offset aUniqidMs
  00B96D43  push    esi
  00B96D44  call    sub_41D990
  00B96D49  add     esp, 8
  00B96D4C  mov     ecx, eax
  00B96D4E  call    sub_B08500
  00B96D53  push    eax
  00B96D54  call    sub_41D990
  00B96D59  mov     ecx, [esp+48h+arg_8]
  00B96D5D  add     esp, 8
  00B96D60  push    ecx
  00B96D61  push    offset aWeaponBuildupE
  00B96D66  push    esi
  00B96D67  call    sub_41D990
  00B96D6C  add     esp, 8
  00B96D6F  mov     ecx, eax
  00B96D71  call    sub_B032A0
  00B96D76  push    offset aByte
  00B96D7B  mov     edx, ebx
  00B96D7D  sub     edx, ebp
  00B96D7F  push    edx
  00B96D80  push    offset asc_EDAD58
  00B96D85  push    esi
  00B96D86  call    sub_41D990
  00B96D8B  add     esp, 8
  00B96D8E  mov     ecx, eax
  00B96D90  call    sub_B03580
  00B96D95  push    eax
  00B96D96  call    sub_41D990
  00B96D9B  add     esp, 8
  00B96D9E  mov     esi, eax
  00B96DA0  push    0Ah
  00B96DA2  mov     ecx, esi
  00B96DA4  call    sub_B036E0
  00B96DA9  mov     ecx, esi
  00B96DAB  call    sub_40DDF0
  00B96DB0  mov     eax, [edi]
  00B96DB2  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B96DB0  mov     eax, [edi]
  00B96DB2  mov     edx, [eax+58h]
  00B96DB5  sub     ebx, ebp
  00B96DB7  push    ebx
  00B96DB8  push    ebp
  00B96DB9  mov     ecx, edi
  00B96DBB  call    edx
  00B96DBD  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B96CA4` | u16 / 2 |
| `uniqid_ms` | `0xB96CB4`;`0xB96CBF` | u64 / 8 |
| `weapon_buildup_extra_cnt` | `0xB96CCD` | u16 / 2 |

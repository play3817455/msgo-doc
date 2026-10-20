# 汇编证据 —— CS-0xF0FA-lounge-ranking_clan_get_page

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA3C40`（`0x00BA3C40`..`0x00BA3E8F`），函数 `sub_BA3C40`
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_clan_get_page(` @ `0x00EECE94`
- opcode 写入：`0x00BA3CC1`
- 声明容量：`0x16`（分配器容量 `push` @ `0x00BA3C86`）
- 提交（`sub_B02FF0`）：`0x00BA3D6E`
- 发送去向：`vt[0x58]` @ `0x00BA3E1D`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA3C8F  push    eax
  00BA3C90  lea     ecx, [esp+4Ch+var_34]
  00BA3C94  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA3C99  lea     ecx, [ebp+16h]
  00BA3C9C  lea     eax, [ebp+2]
  00BA3C9F  cmp     eax, ecx
  00BA3CA1  mov     [esp+48h+var_4], 0
  00BA3CA9  mov     [esp+48h+var_30], ebp
  00BA3CAD  mov     dword ptr [esp+48h+var_2C], ecx
  00BA3CB1  ja      loc_BA3E7A
  00BA3CB7  mov     edx, [esp+48h+arg_0]
  00BA3CBB  lea     ecx, [esp+48h+var_30]
  00BA3CBF  push    ecx
  00BA3CC0  push    edx
  00BA3CC1  mov     word ptr [ebp+0], 0F0FAh   ; <<< 内联写线（u16）
  00BA3CC7  mov     [esp+50h+var_30], eax
  00BA3CCB  call    sub_B42060   ; <<< 复合写入器
  00BA3CD0  add     esp, 8
  00BA3CD3  test    al, al
  00BA3CD5  jz      loc_BA3E7A
  00BA3CDB  mov     ecx, [esp+48h+var_30]
  00BA3CDF  lea     eax, [ecx+4]
  00BA3CE2  cmp     eax, dword ptr [esp+48h+var_2C]
  00BA3CE6  ja      loc_BA3E7A
  00BA3CEC  mov     edx, dword ptr [esp+48h+arg_4]
  00BA3CF0  mov     [esp+48h+var_30], eax
  00BA3CF4  lea     eax, [esp+48h+var_30]
  00BA3CF8  mov     [ecx], edx   ; <<< 内联写线（u32）
  00BA3CFA  push    eax
  00BA3CFB  lea     ecx, [esp+4Ch+arg_8]
  00BA3CFF  push    ecx
  00BA3D00  call    sub_B061C0   ; <<< 写线原语 u8
  00BA3D05  add     esp, 8
  00BA3D08  test    al, al
  00BA3D0A  jz      loc_BA3E7A
  00BA3D10  mov     esi, [edi+8180h]
  00BA3D16  test    esi, esi
  00BA3D18  mov     ebx, [esp+48h+var_30]
  00BA3D1C  jz      loc_BA3E1B
  00BA3D22  lea     edx, [esp+48h+var_28]
  00BA3D26  push    edx
  00BA3D27  call    sub_CA0CE0
  00BA3D2C  add     esp, 4
  00BA3D2F  mov     ecx, [edi+8]
  00BA3D32  push    offset aProtoLoungeCli_424
  00BA3D37  push    ecx
  00BA3D38  push    offset aId
  00BA3D3D  push    eax
  00BA3D3E  push    esi
  00BA3D3F  mov     byte ptr [esp+5Ch+var_4], 1
  00BA3D44  call    sub_B03020
  00BA3D49  add     esp, 8
  00BA3D4C  push    eax
  00BA3D4D  call    sub_41D990
  00BA3D52  add     esp, 8
  00BA3D55  mov     ecx, eax
  00BA3D57  call    sub_ADC810
  00BA3D5C  push    eax
  00BA3D5D  call    sub_41D990
  00BA3D62  add     esp, 8
  00BA3D65  lea     ecx, [esp+48h+var_28]
  00BA3D69  mov     byte ptr [esp+48h+var_4], 0
  00BA3D6E  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA3D6E  call    sub_B02FF0
  00BA3D73  mov     edx, [esp+48h+arg_0]
  00BA3D77  push    offset word_F641DC
  00BA3D7C  push    edx
  00BA3D7D  push    offset aOrder
  00BA3D82  push    esi
  00BA3D83  call    sub_41D990
  00BA3D88  add     esp, 8
  00BA3D8B  push    eax
  00BA3D8C  call    sub_B4F620
  00BA3D91  add     esp, 8
  00BA3D94  push    eax
  00BA3D95  call    sub_41D990
  00BA3D9A  mov     eax, dword ptr [esp+50h+arg_4]
  00BA3D9E  add     esp, 8
  00BA3DA1  push    offset word_F641DC
  00BA3DA6  push    eax
  00BA3DA7  push    offset aPage_0
  00BA3DAC  push    esi
  00BA3DAD  call    sub_41D990
  00BA3DB2  add     esp, 8
  00BA3DB5  mov     ecx, eax
  00BA3DB7  call    sub_B03580
  00BA3DBC  push    eax
  00BA3DBD  call    sub_41D990
  00BA3DC2  add     esp, 8
  00BA3DC5  lea     ecx, [esp+48h+arg_8]
  00BA3DC9  push    ecx
  00BA3DCA  push    offset aClanKind
  00BA3DCF  push    esi
  00BA3DD0  call    sub_41D990
  00BA3DD5  add     esp, 8
  00BA3DD8  push    eax
  00BA3DD9  call    sub_B0C1F0
  00BA3DDE  add     esp, 8
  00BA3DE1  push    offset aByte
  00BA3DE6  mov     edx, ebx
  00BA3DE8  sub     edx, ebp
  00BA3DEA  push    edx
  00BA3DEB  push    offset asc_EDAD58
  00BA3DF0  push    esi
  00BA3DF1  call    sub_41D990
  00BA3DF6  add     esp, 8
  00BA3DF9  mov     ecx, eax
  00BA3DFB  call    sub_B03580
  00BA3E00  push    eax
  00BA3E01  call    sub_41D990
  00BA3E06  add     esp, 8
  00BA3E09  mov     esi, eax
  00BA3E0B  push    0Ah
  00BA3E0D  mov     ecx, esi
  00BA3E0F  call    sub_B036E0
  00BA3E14  mov     ecx, esi
  00BA3E16  call    sub_40DDF0
  00BA3E1B  mov     eax, [edi]
  00BA3E1D  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00BA3E1B  mov     eax, [edi]
  00BA3E1D  mov     edx, [eax+58h]
  00BA3E20  sub     ebx, ebp
  00BA3E22  push    ebx
  00BA3E23  push    ebp
  00BA3E24  mov     ecx, edi
  00BA3E26  call    edx
  00BA3E28  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA3CC1` | u16 / 2 |
| `order` | `0xBA3CCB` | bytes / 10 |
| `page` | `0xBA3CEC`;`0xBA3CF8` | u32 / 4 |
| `clan_kind` | `0xBA3D00` | u8 / 1 |

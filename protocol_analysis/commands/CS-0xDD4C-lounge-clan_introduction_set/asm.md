# 汇编证据 —— CS-0xDD4C-lounge-clan_introduction_set

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA1200`（`0x00BA1200`..`0x00BA140D`），函数 `sub_BA1200`
- 命令名字符串：`)<-_proto_lounge_client::send_clan_introduction_set(` @ `0x00EECA0C`
- opcode 写入：`0x00BA1287`
- 声明容量：`0x22A`（分配器容量 `push` @ `0x00BA1246`）
- 提交（`sub_B02FF0`）：`0x00BA1312`
- 发送去向：`vt[0x58]` @ `0x00BA1399`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA1252  push    eax
  00BA1253  lea     ecx, [esp+4Ch+var_34]
  00BA1257  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA125C  lea     ecx, [ebp+22Ah]
  00BA1262  lea     eax, [ebp+2]
  00BA1265  cmp     eax, ecx
  00BA1267  mov     [esp+48h+var_4], 0
  00BA126F  mov     [esp+48h+var_30], ebp
  00BA1273  mov     dword ptr [esp+48h+var_2C], ecx
  00BA1277  ja      loc_BA13F8
  00BA127D  mov     edx, dword ptr [esp+48h+arg_0]
  00BA1281  lea     ecx, [esp+48h+var_30]
  00BA1285  push    ecx
  00BA1286  push    edx
  00BA1287  mov     word ptr [ebp+0], 0DD4Ch   ; <<< 内联写线（u16）
  00BA128D  mov     [esp+50h+var_30], eax
  00BA1291  call    sub_B41EC0   ; <<< 复合写入器
  00BA1296  add     esp, 8
  00BA1299  test    al, al
  00BA129B  jz      loc_BA13F8
  00BA12A1  mov     eax, [esp+48h+var_30]
  00BA12A5  lea     ebx, [eax+1]
  00BA12A8  cmp     ebx, dword ptr [esp+48h+var_2C]
  00BA12AC  ja      loc_BA13F8
  00BA12B2  mov     cl, [esp+48h+arg_4]
  00BA12B6  mov     [eax], cl   ; <<< 内联写线（u8）
  00BA12B8  mov     edi, [esi+80D0h]
  00BA12BE  test    edi, edi
  00BA12C0  jz      loc_BA1397
  00BA12C6  lea     edx, [esp+48h+var_28]
  00BA12CA  push    edx
  00BA12CB  call    sub_CA0CE0
  00BA12D0  add     esp, 4
  00BA12D3  mov     ecx, [esi+8]
  00BA12D6  push    offset aProtoLoungeCli_483
  00BA12DB  push    ecx
  00BA12DC  push    offset aId
  00BA12E1  push    eax
  00BA12E2  push    edi
  00BA12E3  mov     byte ptr [esp+5Ch+var_4], 1
  00BA12E8  call    sub_B03020
  00BA12ED  add     esp, 8
  00BA12F0  push    eax
  00BA12F1  call    sub_41D990
  00BA12F6  add     esp, 8
  00BA12F9  mov     ecx, eax
  00BA12FB  call    sub_ADC810
  00BA1300  push    eax
  00BA1301  call    sub_41D990
  00BA1306  add     esp, 8
  00BA1309  lea     ecx, [esp+48h+var_28]
  00BA130D  mov     byte ptr [esp+48h+var_4], 0
  00BA1312  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA1312  call    sub_B02FF0
  00BA1317  mov     edx, dword ptr [esp+48h+arg_0]
  00BA131B  push    offset word_F641DC
  00BA1320  push    edx
  00BA1321  push    offset aIntroInfo
  00BA1326  push    edi
  00BA1327  call    sub_41D990
  00BA132C  add     esp, 8
  00BA132F  push    eax
  00BA1330  call    sub_B4F080
  00BA1335  add     esp, 8
  00BA1338  push    eax
  00BA1339  call    sub_41D990
  00BA133E  add     esp, 8
  00BA1341  lea     eax, [esp+48h+arg_4]
  00BA1345  push    eax
  00BA1346  push    offset aClanKind
  00BA134B  push    edi
  00BA134C  call    sub_41D990
  00BA1351  add     esp, 8
  00BA1354  push    eax
  00BA1355  call    sub_B0C1F0
  00BA135A  add     esp, 8
  00BA135D  push    offset aByte
  00BA1362  mov     ecx, ebx
  00BA1364  sub     ecx, ebp
  00BA1366  push    ecx
  00BA1367  push    offset asc_EDAD58
  00BA136C  push    edi
  00BA136D  call    sub_41D990
  00BA1372  add     esp, 8
  00BA1375  mov     ecx, eax
  00BA1377  call    sub_B03580
  00BA137C  push    eax
  00BA137D  call    sub_41D990
  00BA1382  add     esp, 8
  00BA1385  mov     edi, eax
  00BA1387  push    0Ah
  00BA1389  mov     ecx, edi
  00BA138B  call    sub_B036E0
  00BA1390  mov     ecx, edi
  00BA1392  call    sub_40DDF0
  00BA1397  mov     edx, [esi]
  00BA1399  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA1397  mov     edx, [esi]
  00BA1399  mov     eax, [edx+58h]
  00BA139C  mov     edi, ebx
  00BA139E  sub     edi, ebp
  00BA13A0  push    edi
  00BA13A1  push    ebp
  00BA13A2  mov     ecx, esi
  00BA13A4  call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA1287` | u16 / 2 |
| `intro_info` | `0xBA1291` | bytes / 547 |
| `clan_kind` | `0xBA12B2`;`0xBA12B6` | u8 / 1 |

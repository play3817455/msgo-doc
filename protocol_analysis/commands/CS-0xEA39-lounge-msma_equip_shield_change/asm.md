# 汇编证据 —— CS-0xEA39-lounge-msma_equip_shield_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B93850`（`0x00B93850`..`0x00B93A42`），函数 `sub_B93850`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_shield_change(` @ `0x00EEB400`
- opcode 写入：`0x00B938C4`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B93896`）
- 提交（`sub_B02FF0`）：`0x00B93948`
- 发送去向：`vt[0x58]` @ `0x00B939D0`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B9389F  push    eax
  00B938A0  lea     ecx, [esp+44h+var_2C]
  00B938A4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B938A9  lea     ecx, [ebp+0Eh]
  00B938AC  lea     eax, [ebp+2]
  00B938AF  cmp     eax, ecx
  00B938B1  mov     [esp+40h+var_4], 0
  00B938B9  ja      loc_B93A2D
  00B938BF  lea     edx, [eax+8]
  00B938C2  cmp     edx, ecx
  00B938C4  mov     word ptr [ebp+0], 0EA39h   ; <<< 内联写线（u16）
  00B938CA  ja      loc_B93A2D
  00B938D0  mov     esi, [esp+40h+arg_0]
  00B938D4  mov     [eax], esi   ; <<< 内联写线（u32）
  00B938D6  mov     esi, [esp+40h+arg_4]
  00B938DA  lea     ebx, [edx+4]
  00B938DD  cmp     ebx, ecx
  00B938DF  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00B938E2  ja      loc_B93A2D
  00B938E8  mov     ecx, [esp+40h+arg_8]
  00B938EC  mov     [edx], ecx   ; <<< 内联写线（u32）
  00B938EE  mov     esi, [edi+7D10h]
  00B938F4  test    esi, esi
  00B938F6  jz      loc_B939CE
  00B938FC  lea     edx, [esp+40h+var_28]
  00B93900  push    edx
  00B93901  call    sub_CA0CE0
  00B93906  add     esp, 4
  00B93909  mov     ecx, [edi+8]
  00B9390C  push    offset aProtoLoungeCli_435
  00B93911  push    ecx
  00B93912  push    offset aId
  00B93917  push    eax
  00B93918  push    esi
  00B93919  mov     byte ptr [esp+54h+var_4], 1
  00B9391E  call    sub_B03020
  00B93923  add     esp, 8
  00B93926  push    eax
  00B93927  call    sub_41D990
  00B9392C  add     esp, 8
  00B9392F  mov     ecx, eax
  00B93931  call    sub_ADC810
  00B93936  push    eax
  00B93937  call    sub_41D990
  00B9393C  add     esp, 8
  00B9393F  lea     ecx, [esp+40h+var_28]
  00B93943  mov     byte ptr [esp+40h+var_4], 0
  00B93948  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B93948  call    sub_B02FF0
  00B9394D  mov     edx, [esp+40h+arg_4]
  00B93951  mov     eax, [esp+40h+arg_0]
  00B93955  push    offset word_F641DC
  00B9395A  push    edx
  00B9395B  push    eax
  00B9395C  push    offset aUniqidMs
  00B93961  push    esi
  00B93962  call    sub_41D990
  00B93967  add     esp, 8
  00B9396A  mov     ecx, eax
  00B9396C  call    sub_B08500
  00B93971  push    eax
  00B93972  call    sub_41D990
  00B93977  mov     ecx, [esp+48h+arg_8]
  00B9397B  add     esp, 8
  00B9397E  push    ecx
  00B9397F  push    offset aItemId
  00B93984  push    esi
  00B93985  call    sub_41D990
  00B9398A  add     esp, 8
  00B9398D  mov     ecx, eax
  00B9398F  call    sub_B03580
  00B93994  push    offset aByte
  00B93999  mov     edx, ebx
  00B9399B  sub     edx, ebp
  00B9399D  push    edx
  00B9399E  push    offset asc_EDAD58
  00B939A3  push    esi
  00B939A4  call    sub_41D990
  00B939A9  add     esp, 8
  00B939AC  mov     ecx, eax
  00B939AE  call    sub_B03580
  00B939B3  push    eax
  00B939B4  call    sub_41D990
  00B939B9  add     esp, 8
  00B939BC  mov     esi, eax
  00B939BE  push    0Ah
  00B939C0  mov     ecx, esi
  00B939C2  call    sub_B036E0
  00B939C7  mov     ecx, esi
  00B939C9  call    sub_40DDF0
  00B939CE  mov     eax, [edi]
  00B939D0  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B939CE  mov     eax, [edi]
  00B939D0  mov     edx, [eax+58h]
  00B939D3  sub     ebx, ebp
  00B939D5  push    ebx
  00B939D6  push    ebp
  00B939D7  mov     ecx, edi
  00B939D9  call    edx
  00B939DB  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B938C4` | u16 / 2 |
| `uniqid_ms` | `0xB938D4`;`0xB938DF` | u64 / 8 |
| `item_id` | `0xB938EC` | u32 / 4 |

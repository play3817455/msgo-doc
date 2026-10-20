# 汇编证据 —— CS-0xF5AC-lounge-msma_equipset_switch

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00B990A0`（`0x00B990A0`..`0x00B99294`），函数 `sub_B990A0`
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equipset_switch(` @ `0x00EEBCE4`
- opcode 写入：`0x00B99114`
- 声明容量：`0xE`（分配器容量 `push` @ `0x00B990E6`）
- 提交（`sub_B02FF0`）：`0x00B9919A`
- 发送去向：`vt[0x58]` @ `0x00B99222`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00B990EF  push    eax
  00B990F0  lea     ecx, [esp+44h+var_2C]
  00B990F4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00B990F9  lea     ecx, [ebp+0Eh]
  00B990FC  lea     eax, [ebp+2]
  00B990FF  cmp     eax, ecx
  00B99101  mov     [esp+40h+var_4], 0
  00B99109  ja      loc_B9927F
  00B9910F  lea     edx, [eax+8]
  00B99112  cmp     edx, ecx
  00B99114  mov     word ptr [ebp+0], 0F5ACh   ; <<< 内联写线（u16）
  00B9911A  ja      loc_B9927F
  00B99120  mov     esi, [esp+40h+arg_0]
  00B99124  mov     [eax], esi   ; <<< 内联写线（u32）
  00B99126  mov     esi, [esp+40h+arg_4]
  00B9912A  lea     ebx, [edx+2]
  00B9912D  cmp     ebx, ecx
  00B9912F  mov     [eax+4], esi   ; <<< 内联写线（u32）
  00B99132  ja      loc_B9927F
  00B99138  mov     cx, word ptr [esp+40h+arg_8]
  00B9913D  mov     [edx], cx   ; <<< 内联写线（u16）
  00B99140  mov     esi, [edi+7E74h]
  00B99146  test    esi, esi
  00B99148  jz      loc_B99220
  00B9914E  lea     edx, [esp+40h+var_28]
  00B99152  push    edx
  00B99153  call    sub_CA0CE0
  00B99158  add     esp, 4
  00B9915B  mov     ecx, [edi+8]
  00B9915E  push    offset aProtoLoungeCli_437
  00B99163  push    ecx
  00B99164  push    offset aId
  00B99169  push    eax
  00B9916A  push    esi
  00B9916B  mov     byte ptr [esp+54h+var_4], 1
  00B99170  call    sub_B03020
  00B99175  add     esp, 8
  00B99178  push    eax
  00B99179  call    sub_41D990
  00B9917E  add     esp, 8
  00B99181  mov     ecx, eax
  00B99183  call    sub_ADC810
  00B99188  push    eax
  00B99189  call    sub_41D990
  00B9918E  add     esp, 8
  00B99191  lea     ecx, [esp+40h+var_28]
  00B99195  mov     byte ptr [esp+40h+var_4], 0
  00B9919A  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00B9919A  call    sub_B02FF0
  00B9919F  mov     edx, [esp+40h+arg_4]
  00B991A3  mov     eax, [esp+40h+arg_0]
  00B991A7  push    offset word_F641DC
  00B991AC  push    edx
  00B991AD  push    eax
  00B991AE  push    offset aUniqidMs
  00B991B3  push    esi
  00B991B4  call    sub_41D990
  00B991B9  add     esp, 8
  00B991BC  mov     ecx, eax
  00B991BE  call    sub_B08500
  00B991C3  push    eax
  00B991C4  call    sub_41D990
  00B991C9  mov     ecx, [esp+48h+arg_8]
  00B991CD  add     esp, 8
  00B991D0  push    ecx
  00B991D1  push    offset aSlot
  00B991D6  push    esi
  00B991D7  call    sub_41D990
  00B991DC  add     esp, 8
  00B991DF  mov     ecx, eax
  00B991E1  call    sub_B032A0
  00B991E6  push    offset aByte
  00B991EB  mov     edx, ebx
  00B991ED  sub     edx, ebp
  00B991EF  push    edx
  00B991F0  push    offset asc_EDAD58
  00B991F5  push    esi
  00B991F6  call    sub_41D990
  00B991FB  add     esp, 8
  00B991FE  mov     ecx, eax
  00B99200  call    sub_B03580
  00B99205  push    eax
  00B99206  call    sub_41D990
  00B9920B  add     esp, 8
  00B9920E  mov     esi, eax
  00B99210  push    0Ah
  00B99212  mov     ecx, esi
  00B99214  call    sub_B036E0
  00B99219  mov     ecx, esi
  00B9921B  call    sub_40DDF0
  00B99220  mov     eax, [edi]
  00B99222  mov     edx, [eax+58h]
```

## 4. 发送去向切片

```asm
  00B99220  mov     eax, [edi]
  00B99222  mov     edx, [eax+58h]
  00B99225  sub     ebx, ebp
  00B99227  push    ebx
  00B99228  push    ebp
  00B99229  mov     ecx, edi
  00B9922B  call    edx
  00B9922D  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00B99114` | u16 / 2 |
| `uniqid_ms` | `0xB99124`;`0xB9912F` | u64 / 8 |
| `slot` | `0xB9913D` | u16 / 2 |

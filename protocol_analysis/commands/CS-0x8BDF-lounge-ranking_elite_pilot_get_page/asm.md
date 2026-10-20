# 汇编证据 —— CS-0x8BDF-lounge-ranking_elite_pilot_get_page

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA7770 @ `0xba7770`（`0xba7770`..`0xba7973`）
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_elite_pilot_get_page(` @ `0xeed4cc`
- opcode 写入：`0xba77f1`
- 声明容量：`0x12`（分配器容量 `push` @ `0xba77b6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba77ba  mov     ebp, eax
  0xba77bc  mov     eax, [esi+0Ch]
  0xba77bf  push    eax
  0xba77c0  lea     ecx, [esp+4Ch+var_34]
  0xba77c4  call    sub_ABB2F0
  0xba77c9  lea     ecx, [ebp+12h]
  0xba77cc  lea     eax, [ebp+2]
  0xba77cf  cmp     eax, ecx
  0xba77d1  mov     [esp+48h+var_4], 0
  0xba77d9  mov     [esp+48h+var_30], ebp
  0xba77dd  mov     dword ptr [esp+48h+var_2C], ecx
  0xba77e1  ja      loc_BA795E
  0xba77e7  mov     edx, [esp+48h+arg_0]
  0xba77eb  lea     ecx, [esp+48h+var_30]
  0xba77ef  push    ecx
  0xba77f0  push    edx
  0xba77f1  mov     word ptr [ebp+0], 8BDFh
  0xba77f7  mov     [esp+50h+var_30], eax
  0xba77fb  call    sub_B42060
  0xba7800  add     esp, 8
  0xba7803  test    al, al
  0xba7805  jz      loc_BA795E
  0xba780b  mov     eax, [esp+48h+var_30]
  0xba780f  lea     ebx, [eax+4]
  0xba7812  cmp     ebx, dword ptr [esp+48h+var_2C]
  0xba7816  ja      loc_BA795E
  0xba781c  mov     ecx, [esp+48h+arg_4]
  0xba7820  mov     [eax], ecx
  0xba7822  mov     edi, [esi+82E0h]
  0xba7828  test    edi, edi
  0xba782a  jz      loc_BA78FF
  0xba7830  lea     edx, [esp+48h+var_28]
  0xba7834  push    edx
  0xba7835  call    sub_CA0CE0
  0xba783a  add     esp, 4
  0xba783d  mov     ecx, [esi+8]
  0xba7840  push    offset aProtoLoungeCli_501; ")<-_proto_lounge_client::send_ranking_e"...
  0xba7845  push    ecx
  0xba7846  push    offset aId; " (id:"
  0xba784b  push    eax
  0xba784c  push    edi
  0xba784d  mov     byte ptr [esp+5Ch+var_4], 1
  0xba7852  call    sub_B03020
  0xba7857  add     esp, 8
  0xba785a  push    eax
  0xba785b  call    sub_41D990
  0xba7860  add     esp, 8
  0xba7863  mov     ecx, eax
  0xba7865  call    sub_ADC810
  0xba786a  push    eax
  0xba786b  call    sub_41D990
  0xba7870  add     esp, 8
  0xba7873  lea     ecx, [esp+48h+var_28]
  0xba7877  mov     byte ptr [esp+48h+var_4], 0
  0xba787c  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba788b  push    offset aOrder; "order="
  0xba78b0  push    offset aPage_0; "page="
  0xba78c5  push    offset aByte; "]byte"
  0xba78cf  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba7901  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba77f1` | u16 |
| `order` | `0xBA77FB (writer sub_B42060)` | u16[5] |
| `page` | `0xBA7820` | u32 |

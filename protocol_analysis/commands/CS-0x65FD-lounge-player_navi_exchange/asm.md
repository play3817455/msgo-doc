# 汇编证据 —— CS-0x65FD-lounge-player_navi_exchange

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA75C0 @ `0xba75c0`（`0xba75c0`..`0xba776d`）
- 命令名字符串：`)<-_proto_lounge_client::send_player_navi_exchange(` @ `0xeed494`
- opcode 写入：`0xba7634`
- 声明容量：`0x6`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba760a  mov     ebp, eax
  0xba760c  mov     eax, [esi+0Ch]
  0xba760f  push    eax
  0xba7610  lea     ecx, [esp+44h+var_2C]
  0xba7614  call    sub_ABB2F0
  0xba7619  lea     ecx, [ebp+6]
  0xba761c  lea     eax, [ebp+2]
  0xba761f  cmp     eax, ecx
  0xba7621  mov     [esp+40h+var_4], 0
  0xba7629  ja      loc_BA7758
  0xba762f  lea     ebx, [eax+4]
  0xba7632  cmp     ebx, ecx
  0xba7634  mov     word ptr [ebp+0], 65FDh
  0xba763a  ja      loc_BA7758
  0xba7640  mov     ecx, [esp+40h+arg_0]
  0xba7644  mov     [eax], ecx
  0xba7646  mov     edi, [esi+82D8h]
  0xba764c  test    edi, edi
  0xba764e  jz      loc_BA76F9
  0xba7654  lea     edx, [esp+40h+var_28]
  0xba7658  push    edx
  0xba7659  call    sub_CA0CE0
  0xba765e  add     esp, 4
  0xba7661  mov     ecx, [esi+8]
  0xba7664  push    offset aProtoLoungeCli_544; ")<-_proto_lounge_client::send_player_na"...
  0xba7669  push    ecx
  0xba766a  push    offset aId; " (id:"
  0xba766f  push    eax
  0xba7670  push    edi
  0xba7671  mov     byte ptr [esp+54h+var_4], 1
  0xba7676  call    sub_B03020
  0xba767b  add     esp, 8
  0xba767e  push    eax
  0xba767f  call    sub_41D990
  0xba7684  add     esp, 8
  0xba7687  mov     ecx, eax
  0xba7689  call    sub_ADC810
  0xba768e  push    eax
  0xba768f  call    sub_41D990
  0xba7694  add     esp, 8
  0xba7697  lea     ecx, [esp+40h+var_28]
  0xba769b  mov     byte ptr [esp+40h+var_4], 0
  0xba76a0  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba76aa  push    offset aNaviId; "navi_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba76bf  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba76fb  mov     eax, [edx+58h]
  0xba76fe  sub     ebx, ebp
  0xba7700  push    ebx
  0xba7701  push    ebp
  0xba7702  mov     ecx, esi
  0xba7704  call    eax
  0xba7706  test    al, al
  0xba7708  jz      short loc_BA7758
  0xba770a  mov     eax, [esi+79A8h]
  0xba7710  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA7634` | u16 |
| `navi_id` | `0xBA7644` | u32 |

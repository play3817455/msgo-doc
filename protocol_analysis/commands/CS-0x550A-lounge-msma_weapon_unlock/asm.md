# 汇编证据 —— CS-0x550A-lounge-msma_weapon_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B978A0 @ `0xb978a0`（`0xb978a0`..`0xb97b26`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_unlock(` @ `0xeebaa0`
- opcode 写入：`0xb9791c`
- 声明容量：`0x16`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb978ea  mov     ebp, eax
  0xb978ec  mov     eax, [edi+0Ch]
  0xb978ef  push    eax
  0xb978f0  lea     ecx, [esp+4Ch+var_34]
  0xb978f4  call    sub_ABB2F0
  0xb978f9  lea     ecx, [ebp+16h]
  0xb978fc  lea     eax, [ebp+2]
  0xb978ff  cmp     eax, ecx
  0xb97901  mov     [esp+48h+var_4], 0
  0xb97909  mov     [esp+48h+var_30], ebp
  0xb9790d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb97911  ja      loc_B97B11
  0xb97917  lea     edx, [eax+8]
  0xb9791a  cmp     edx, ecx
  0xb9791c  mov     word ptr [ebp+0], 550Ah
  0xb97922  ja      loc_B97B11
  0xb97928  mov     esi, [esp+48h+arg_0]
  0xb9792c  mov     [eax], esi
  0xb9792e  mov     esi, [esp+48h+arg_4]
  0xb97932  mov     [eax+4], esi
  0xb97935  lea     eax, [edx+4]
  0xb97938  cmp     eax, ecx
  0xb9793a  ja      loc_B97B11
  0xb97940  mov     ecx, [esp+48h+arg_8]
  0xb97944  mov     [edx], ecx
  0xb97946  lea     edx, [esp+48h+var_30]
  0xb9794a  mov     [esp+48h+var_30], eax
  0xb9794e  push    edx
  0xb9794f  lea     eax, [esp+4Ch+arg_C]
  0xb97953  push    eax
  0xb97954  call    sub_B02D80
  0xb97959  add     esp, 8
  0xb9795c  test    al, al
  0xb9795e  jz      loc_B97B11
  0xb97964  lea     ecx, [esp+48h+var_30]
  0xb97968  push    ecx
  0xb97969  lea     edx, [esp+4Ch+arg_10]
  0xb9796d  push    edx
  0xb9796e  call    sub_B02D80
  0xb97973  add     esp, 8
  0xb97976  test    al, al
  0xb97978  jz      loc_B97B11
  0xb9797e  mov     esi, [edi+7E14h]
  0xb97984  test    esi, esi
  0xb97986  mov     ebx, [esp+48h+var_30]
  0xb9798a  jz      loc_B97AB2
  0xb97990  lea     eax, [esp+48h+var_28]
  0xb97994  push    eax
  0xb97995  call    sub_CA0CE0
  0xb9799a  add     esp, 4
  0xb9799d  mov     ecx, [edi+8]
  0xb979a0  push    offset aProtoLoungeCli_470; ")<-_proto_lounge_client::send_msma_weap"...
  0xb979a5  push    ecx
  0xb979a6  push    offset aId; " (id:"
  0xb979ab  push    eax
  0xb979ac  push    esi
  0xb979ad  mov     byte ptr [esp+5Ch+var_4], 1
  0xb979b2  call    sub_B03020
  0xb979b7  add     esp, 8
  0xb979ba  push    eax
  0xb979bb  call    sub_41D990
  0xb979c0  add     esp, 8
  0xb979c3  mov     ecx, eax
  0xb979c5  call    sub_ADC810
  0xb979ca  push    eax
  0xb979cb  call    sub_41D990
  0xb979d0  add     esp, 8
  0xb979d3  lea     ecx, [esp+48h+var_28]
  0xb979d7  mov     byte ptr [esp+48h+var_4], 0
  0xb979dc  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb979f0  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97a18  push    offset aItemId; "item_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97a40  push    offset aUseGp; "use_gp="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97a63  push    offset aUseBc; "use_bc="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb97a78  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb97ab4  mov     eax, [edx+58h]
  0xb97ab7  sub     ebx, ebp
  0xb97ab9  push    ebx
  0xb97aba  push    ebp
  0xb97abb  mov     ecx, edi
  0xb97abd  call    eax
  0xb97abf  test    al, al
  0xb97ac1  jz      short loc_B97B11
  0xb97ac3  mov     eax, [edi+79A8h]
  0xb97ac9  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9791C` | u16 |
| `uniqid_ms` | `0xB9792C` | u64 |
| `item_id` | `0xB97944` | u32 |
| `use_gp` | `0xB97954` | u32 |
| `use_bc` | `0xB9796E` | u32 |

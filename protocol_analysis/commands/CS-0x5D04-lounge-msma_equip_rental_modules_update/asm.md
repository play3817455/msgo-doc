# 汇编证据 —— CS-0x5D04-lounge-msma_equip_rental_modules_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B944A0 @ `0xb944a0`（`0xb944a0`..`0xb947b0`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_rental_modules_update(` @ `0xeeb590`
- opcode 写入：`0xb9451c`
- 声明容量：`0x36`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb944ee  mov     esi, eax
  0xb944f0  mov     eax, [ebp+0Ch]
  0xb944f3  push    eax
  0xb944f4  lea     ecx, [esp+54h+var_3C]
  0xb944f8  mov     [esp+54h+var_34], esi
  0xb944fc  call    sub_ABB2F0
  0xb94501  lea     edx, [esi+36h]
  0xb94504  lea     eax, [esi+2]
  0xb94507  cmp     eax, edx
  0xb94509  mov     [esp+50h+var_4], 0
  0xb94511  mov     dword ptr [esp+50h+var_2C], edx
  0xb94515  ja      short loc_B94581
  0xb94517  lea     edi, [eax+8]
  0xb9451a  cmp     edi, edx
  0xb9451c  mov     word ptr [esi], 5D04h
  0xb94521  ja      short loc_B94581
  0xb94523  mov     ecx, [esp+50h+arg_0]
  0xb94527  mov     ebx, [esp+50h+arg_8]
  0xb9452b  test    ebx, ebx
  0xb9452d  mov     [eax], ecx
  0xb9452f  mov     ecx, [esp+50h+arg_4]
  0xb94533  mov     [eax+4], ecx
  0xb94536  jz      short loc_B94581
  0xb94538  xor     eax, eax
  0xb9453a  lea     ecx, [edi+4]
  0xb9453d  lea     ecx, [ecx+0]
  0xb94540  cmp     ecx, edx
  0xb94542  ja      short loc_B94581
  0xb94544  mov     esi, [ebx+eax*4]
  0xb94547  mov     [edi], esi
  0xb94549  add     eax, 1
  0xb9454c  add     edi, 4
  0xb9454f  add     ecx, 4
  0xb94552  cmp     eax, 0Ah
  0xb94555  jb      short loc_B94540
  0xb94557  mov     esi, [esp+50h+arg_C]
  0xb9455b  test    esi, esi
  0xb9455d  jz      short loc_B94581
  0xb9455f  xor     eax, eax
  0xb94561  lea     ecx, [edi+4]
  0xb94564  cmp     ecx, edx
  0xb94566  ja      short loc_B94581
  0xb94568  mov     edx, [esi+eax*4]
  0xb9456b  mov     [edi], edx
  0xb9456d  add     eax, 1
  0xb94570  add     edi, 4
  0xb94573  add     ecx, 4
  0xb94576  cmp     eax, 1
  0xb94579  jnb     short loc_B94599
  0xb9457b  mov     edx, dword ptr [esp+50h+var_2C]
  0xb9457f  jmp     short loc_B94564
  0xb94581  lea     ecx, [esp+50h+var_3C]
  0xb94585  mov     [esp+50h+var_4], 0FFFFFFFFh
  0xb9458d  call    sub_C85DF0
  0xb94592  xor     al, al
  0xb94594  jmp     loc_B9479A
  0xb94599  mov     esi, [ebp+7D54h]
  0xb9459f  test    esi, esi
  0xb945a1  jz      loc_B94748
  ; —— 本块**无** `call sub_B02FF0` 提交调用；
  ;    闭合由发送侧 `游标 − 缓冲首址`（`sub edi,esi; push edi; push esi`）的长度计算完成。
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb945b7  push    offset aProtoLoungeCli_434; ")<-_proto_lounge_client::send_msma_equi"...
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb945bd  push    offset aId; " (id:"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb94617  push    offset aUniqidMs; "uniqid_ms="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb94647  push    offset aEqModules; "eq_modules={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9469e  push    offset aEqRentalModule; "eq_rental_modules={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb946ce  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9474f  mov     eax, [edx+58h]
  0xb94752  sub     edi, esi
  0xb94754  push    edi
  0xb94755  push    esi
  0xb94756  mov     ecx, ebp
  0xb94758  call    eax
  0xb9475a  test    al, al
  0xb9475c  jz      loc_B94581
  0xb94762  mov     eax, [ebp+79A8h]
  0xb94768  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9451C` | u16 |
| `uniqid_ms` | `0xB9452D` | u64 |
| `eq_modules` | `0xB94547` | array<u32,10> |
| `eq_rental_modules` | `0xB9456B` | array<u32,1> |

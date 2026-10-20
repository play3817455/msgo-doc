# 汇编证据 —— CS-0x5456-battle-msma_AI_set_stat

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3CE60 @ `0xb3ce60`（`0xb3ce60`..`0xb3d203`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_AI_set_stat(` @ `0xee1264`
- opcode 写入：`0xb3cee4`
- 声明容量：`0x5E`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb3ceae  mov     esi, eax
  0xb3ceb0  mov     eax, [edi+0Ch]
  0xb3ceb3  push    eax
  0xb3ceb4  lea     ecx, [esp+54h+var_3C]
  0xb3ceb8  mov     [esp+54h+var_34], esi
  0xb3cebc  call    sub_ABB2F0
  0xb3cec1  lea     ecx, [esi+5Eh]
  0xb3cec4  lea     eax, [esi+2]
  0xb3cec7  cmp     eax, ecx
  0xb3cec9  mov     [esp+50h+var_4], 0
  0xb3ced1  mov     [esp+50h+var_30], esi
  0xb3ced5  mov     dword ptr [esp+50h+var_2C], ecx
  0xb3ced9  ja      loc_B3D1EE
  0xb3cedf  lea     edx, [eax+2]
  0xb3cee2  cmp     edx, ecx
  0xb3cee4  mov     word ptr [esi], 5456h
  0xb3cee9  ja      loc_B3D1EE
  0xb3ceef  mov     ebp, [esp+50h+arg_8]
  0xb3cef3  cmp     ebp, 0Ah
  0xb3cef6  mov     cx, word ptr [esp+50h+arg_0]
  0xb3cefb  mov     [eax], cx
  0xb3cefe  mov     [esp+50h+var_30], edx
  0xb3cf02  ja      loc_B3D1EE
  0xb3cf08  lea     edx, [esp+50h+var_30]
  0xb3cf0c  push    edx
  0xb3cf0d  lea     eax, [esp+54h+arg_8]
  0xb3cf11  push    eax
  0xb3cf12  call    sub_B02D80
  0xb3cf17  add     esp, 8
  0xb3cf1a  test    al, al
  0xb3cf1c  jz      loc_B3D1EE
  0xb3cf22  xor     eax, eax
  0xb3cf24  test    ebp, ebp
  0xb3cf26  jbe     short loc_B3CF55
  0xb3cf28  mov     ecx, [esp+50h+var_30]
  0xb3cf2c  mov     esi, dword ptr [esp+50h+var_2C]
  0xb3cf30  lea     edx, [ecx+4]
  0xb3cf33  cmp     edx, esi
  0xb3cf35  ja      loc_B3D1EA
  0xb3cf3b  mov     ebx, [esp+50h+arg_4]
  0xb3cf3f  mov     ebx, [ebx+eax*4]
  0xb3cf42  mov     [ecx], ebx
  0xb3cf44  add     eax, 1
  0xb3cf47  add     ecx, 4
  0xb3cf4a  add     edx, 4
  0xb3cf4d  cmp     eax, ebp
  0xb3cf4f  jb      short loc_B3CF33
  0xb3cf51  mov     [esp+50h+var_30], ecx
  0xb3cf55  mov     ebx, [esp+50h+arg_10]
  0xb3cf59  cmp     ebx, 0Ah
  0xb3cf5c  ja      loc_B3D1EE
  0xb3cf62  lea     ecx, [esp+50h+var_30]
  0xb3cf66  push    ecx
  0xb3cf67  lea     edx, [esp+54h+arg_10]
  0xb3cf6b  push    edx
  0xb3cf6c  call    sub_B02D80
  0xb3cf71  add     esp, 8
  0xb3cf74  test    al, al
  0xb3cf76  jz      loc_B3D1EE
  0xb3cf7c  mov     ecx, [esp+50h+var_30]
  0xb3cf80  xor     eax, eax
  0xb3cf82  test    ebx, ebx
  0xb3cf84  jbe     short loc_B3CFB4
  0xb3cf86  lea     edx, [ecx+4]
  0xb3cf89  lea     esp, [esp+0]
  0xb3cf90  cmp     edx, dword ptr [esp+50h+var_2C]
  0xb3cf94  ja      loc_B3D1EA
  0xb3cf9a  mov     esi, [esp+50h+arg_C]
  0xb3cf9e  mov     esi, [esi+eax*4]
  0xb3cfa1  mov     [ecx], esi
  0xb3cfa3  add     eax, 1
  0xb3cfa6  add     ecx, 4
  0xb3cfa9  add     edx, 4
  0xb3cfac  cmp     eax, ebx
  0xb3cfae  jb      short loc_B3CF90
  0xb3cfb0  mov     [esp+50h+var_30], ecx
  0xb3cfb4  mov     esi, [edi+3EE4h]
  0xb3cfba  test    esi, esi
  0xb3cfbc  jz      loc_B3D185
  0xb3cfc2  lea     eax, [esp+50h+var_28]
  0xb3cfc6  push    eax
  0xb3cfc7  call    sub_CA0CE0
  0xb3cfcc  add     esp, 4
  0xb3cfcf  mov     ecx, [edi+8]
  0xb3cfd2  push    offset aProtoBattleCli_270; ")<-_proto_battle_client::send_msma_AI_s"...
  0xb3cfd7  push    ecx
  0xb3cfd8  push    offset aId; " (id:"
  0xb3cfdd  push    eax
  0xb3cfde  push    esi
  0xb3cfdf  mov     byte ptr [esp+64h+var_4], 1
  0xb3cfe4  call    sub_B03020
  0xb3cfe9  add     esp, 8
  0xb3cfec  push    eax
  0xb3cfed  call    sub_41D990
  0xb3cff2  add     esp, 8
  0xb3cff5  mov     ecx, eax
  0xb3cff7  call    sub_ADC810
  0xb3cffc  push    eax
  0xb3cffd  call    sub_41D990
  0xb3d002  add     esp, 8
  0xb3d005  lea     ecx, [esp+50h+var_28]
  0xb3d009  mov     byte ptr [esp+50h+var_4], 0
  0xb3d00e  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb3d01d  push    offset aAiEntId; "AI_ent_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d038  push    offset aIdx; "idx={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d09e  push    offset aNum_0; "num={"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb3d107  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb3d0fc  mov     eax, [esp+58h+var_30]
  0xb3d100  sub     eax, [esp+58h+var_34]
  0xb3d104  add     esp, 8
  0xb3d107  push    offset aByte; "]byte"
  0xb3d10c  push    eax
  0xb3d10d  push    offset asc_EDAD58; " ) ["
  0xb3d112  push    esi
  0xb3d113  call    sub_41D990
  0xb3d118  add     esp, 8
  0xb3d11b  mov     ecx, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3CEE4` | u16 |
| `AI_ent_id` | `0xB3CEFB` | u16 |
| `idx_num` | `0xB3CF12` | u32 |
| `idx` | `0xB3CF42` | array<u32,N> |
| `num_num` | `0xB3CF6C` | u32 |
| `num` | `0xB3CFA1` | array<u32,N> |

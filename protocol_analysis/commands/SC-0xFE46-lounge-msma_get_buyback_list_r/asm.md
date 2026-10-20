# 汇编证据 —— SC-0xFE46-msma_get_buyback_list_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb8861d`..`0xb88852`
- 命令名字符串：`)->_proto_lounge_client::recv_msma_get_buyback_list_r( ` @ `0xee5534`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B8861D call    sub_B41120
00B88622 test    al, al
00B88624 jz      loc_B890FE
00B8862A mov     ecx, [esi+0Ch]
00B8862D mov     edx, [ecx]
00B8862F mov     eax, [edx+78h]
00B88632 push    79E4h
00B88637 call    eax
00B88639 mov     ecx, [esi+0Ch]
00B8863C push    ecx
00B8863D lea     ecx, [esp+2C60h+var_2834]
00B88644 mov     [esp+2C60h+var_2C3C], eax
00B88648 call    sub_ABB2F0
00B8864D lea     edx, [esp+2C5Ch+var_2C44]
00B88651 push    edx
00B88652 lea     eax, [esp+2C60h+var_2C20]
00B88656 push    eax
00B88662 call    sub_B02DD0
00B8866A test    al, al
00B8866C jnz     short loc_B8868A
00B8866E mov     edx, [esi]
00B88670 mov     eax, [edx+64h]
00B88673 push    1
00B88675 push    0D0h
00B8867A mov     ecx, esi
00B8867C call    eax
00B8867E lea     ecx, [esp+2C5Ch+var_2834]
00B8868A mov     ebx, [esp+2C5Ch+var_2C20]
00B8868E cmp     ebx, 64h
00B88691 ja      short loc_B8866E
00B88693 push    ebx
00B88694 lea     ecx, [esp+2C60h+var_2C3C]
00B88698 push    ecx
00B88699 lea     ecx, [esp+2C64h+var_2BE8]
00B8869D call    sub_B41550
00B886A2 xor     edi, edi
00B886A4 test    ebx, ebx
00B886A6 jbe     short loc_B886E7
00B886A8 mov     edx, [esp+2C5Ch+var_2BE8]
00B886AC mov     [esp+2C5Ch+var_2C3C], edx
00B886B0 mov     ecx, [esp+2C5Ch+var_2C3C]
00B886B4 lea     eax, [esp+2C5Ch+var_2C44]
00B886B8 push    eax
00B886B9 push    ecx
00B886BA call    sub_B43570
00B886C2 test    al, al
00B886C4 jz      short loc_B886D7
00B886C6 add     [esp+2C5Ch+var_2C3C], 138h
00B886CE add     edi, 1
00B886D1 cmp     edi, ebx
00B886D3 jb      short loc_B886B0
00B886D7 mov     edx, [esi]
00B886D9 mov     eax, [edx+64h]
00B886DC push    1
00B886DE push    0D0h
00B886E3 mov     ecx, esi
00B886E5 call    eax
00B886E7 mov     ecx, [esp+2C5Ch+var_2C44]
00B886EB cmp     ecx, [esp+2C5Ch+var_2C40]
00B886EF mov     ecx, esi
00B886F1 jz      short loc_B8870D
00B886F3 mov     edx, [esi]
00B886F5 mov     eax, [edx+64h]
00B886F8 push    1
00B886FA push    0D0h
00B886FF call    eax
00B88701 lea     ecx, [esp+2C5Ch+var_2834]
00B8870D push    0D0h
00B88712 call    sub_B41110
00B88717 mov     edi, eax
00B88719 test    edi, edi
00B8871B jz      loc_B88826
00B88721 lea     ecx, [esp+2C5Ch+var_D4]
00B88728 push    ecx
00B88731 mov     edx, [esi+8]
00B88734 push    offset aProtoLoungeCli_345
00B88739 push    edx
00B8873A push    offset aId
00B8873F push    eax
00B88740 push    edi
00B88751 push    eax
00B8875A mov     ecx, eax
00B88761 push    eax
00B8876A lea     ecx, [esp+2C5Ch+var_D4]
00B88779 call    sub_B02FF0
00B8877E push    offset aMsList
00B88783 push    edi
00B8878C test    ebx, ebx
00B8878E jbe     short loc_B8879E
00B88790 mov     eax, [esp+2C5Ch+var_2BE8]
00B88794 push    eax
00B88795 push    edi
00B88796 call    sub_B49DE0
00B8879E cmp     ebx, 1
00B887A1 jbe     short loc_B887DD
00B887A3 mov     ebx, [esp+2C5Ch+var_2BE8]
00B887A7 mov     ecx, [esp+2C5Ch+var_2C20]
00B887AB add     ebx, 138h
00B887B1 add     ecx, 0FFFFFFFFh
00B887B4 mov     [esp+2C5Ch+var_2C3C], ecx
00B887B8 push    ebx
00B887B9 push    offset word_F641DC
00B887BE push    edi
00B887C7 push    eax
00B887C8 call    sub_B49DE0
00B887D0 add     ebx, 138h
00B887D6 sub     [esp+2C5Ch+var_2C3C], 1
00B887DB jnz     short loc_B887B8
00B887DD push    offset unk_EDABE4
00B887E2 push    edi
00B887E8 mov     eax, [esp+2C64h+var_2C44]
00B887EC sub     eax, [ebp+arg_0]
00B887F2 push    offset sub_B03810
00B887F7 push    offset aByte
00B887FC push    eax
00B887FD push    offset asc_EDAD58
00B88802 push    edi
00B8880B mov     ecx, eax
00B88812 push    eax
00B8881B mov     ecx, eax
00B8881D call    sub_B02D30
00B88822 mov     ebx, [esp+2C5Ch+var_2C20]
00B88826 mov     edx, [esi]
00B88828 mov     eax, [esp+2C5Ch+var_2BE8]
00B8882C mov     edx, [edx+248h]
00B88832 push    ebx
00B88833 push    eax
00B88834 mov     ecx, esi
00B88836 call    edx
00B88838 add     dword ptr [esi+2C58h], 1
00B8883F lea     ecx, [esp+2C5Ch+var_2834]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb88734` | opcode 写入/分发指令 |
| `ms_list_count` | `0xB88662` | u32 |
| `ms_list` | `0xB8869D,0xB886BA` | array<ms_lounge> |

## 4. 块内字符串常量（含义取证用）

```
00B8870D
00EE5534
00EE4BB4
00B49DE0
00B887DD
00B49DE0
00B887B8
00EDABE4
00B02D30
```

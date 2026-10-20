# 汇编证据 —— SC-0x1D02-lounge-channellobby_members_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5800C` @ `0xB57506`）

```asm
; VA: 0xB574F1 .. （块入口，含守卫与容量申请）
00B574F1  call    sub_B41120
00B574F6  test    al, al
00B574F8  jz      loc_B890FE
00B574FE  mov     ecx, [esi+0Ch]
00B57501  mov     eax, [ecx]
00B57503  mov     edx, [eax+78h]
00B57506  push    5800Ch
00B5750B  call    edx
00B5750D  mov     [esp+2C5Ch+var_2C48], eax
00B57511  mov     eax, [esi+0Ch]
00B57514  push    eax
00B57515  lea     ecx, [esp+2C60h+var_2ACC]
00B5751C  call    sub_ABB2F0
00B57521  lea     ecx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`is_simple`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB57544 附近（是否简略模式）
00B5753A  mov     eax, [esp+2C5Ch+var_2C34]
00B5753E  lea     edx, [esp+2C5Ch+var_2C44]
00B57542  push    edx
00B57543  push    eax
00B57544  call    sub_B02DD0
00B57549  add     esp, 8
00B5754C  test    al, al
00B5754E  jnz     short loc_B57569
00B57550  mov     edx, [esi]
00B57552  mov     eax, [edx+64h]
```

## E3 字段 2：`world_client_num`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB57581 附近（本大区在线客户端数）
00B57577  mov     eax, [esp+2C5Ch+var_2C38]
00B5757B  lea     edx, [esp+2C5Ch+var_2C44]
00B5757F  push    edx
00B57580  push    eax
00B57581  call    sub_B02DD0
00B57586  add     esp, 8
00B57589  test    al, al
00B5758B  jz      short loc_B57550
00B5758D  lea     ecx, [esp+2C5Ch+var_2C44]
00B57591  push    ecx
```

## E4 字段 3：`pilots_num`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB57597 附近（成员条目数 N）
00B5758D  lea     ecx, [esp+2C5Ch+var_2C44]
00B57591  push    ecx
00B57592  lea     edx, [esp+2C60h+var_2C3C]
00B57596  push    edx
00B57597  call    sub_B02DD0
00B5759C  add     esp, 8
00B5759F  test    al, al
00B575A1  jnz     short loc_B575BC
00B575A3  mov     eax, [esi]
00B575A5  mov     edx, [eax+64h]
```

## E5 字段 4：`pilots`（array<pilot>，偏移 12，元素线上 159B × N）

```asm
; VA: 0xB575EF 附近（频道大厅成员列表；元素读取器 = pilot 读取器 sub_B06980）
00B575E5  mov     eax, [esp+2C5Ch+var_2C48]
00B575E9  lea     edx, [esp+2C5Ch+var_2C44]
00B575ED  push    edx
00B575EE  push    eax
00B575EF  call    sub_B06980
00B575F4  add     esp, 8
00B575F7  test    al, al
00B575F9  jz      short loc_B5760C
00B575FB  add     [esp+2C5Ch+var_2C48], 0B0h   ; 槽步进 176（≠ 元素线长 159）
00B57603  add     edi, 1
```

## E6 元素 = `pilot`（24 成员 / 线上 159B）

元素读取器 `sub_B06980`（读侧）与写入器 `sub_B06360`（写侧，pilot 159B）**同序同偏移**，
所以元素类型就是 db_design 的 `pilot` 复合体。逐成员读点（读原语：
`sub_B02DD0`=u32、`sub_B02DF0`=u16、`sub_B06230`=u8、`sub_B068B0`=avatar 18B）：

```asm
; sub_B06980  元素基址 = edi，游标 = [arg_4]
; +0x00 pilot_id         u32        00B06993  mov edx,[eax]      / 00B0699A mov [edi],edx
; +0x04 name             char[25]   00B069AF  mov cl,[ecx]…cmp eax,19h @00B069BD（循环 25 次）
; +0x1D troops           i8         00B069D0  mov [edi+1Dh],al
; +0x1E level            i8         00B069E6  mov [edi+1Eh],dl
; +0x1F mil_class        i8         00B069FC  mov [edi+1Fh],dl
; +0x20 byword           u16        00B06A13  mov [edi+20h],dx
; +0x24 cmdr_fame        u32        00B06A2A  mov [edi+24h],edx
; +0x28 rate_vslocal     u16        00B06A31  call sub_B02DF0   (lea edx,[edi+28h] @00B06A26)
; +0x2A rate_vslocal_4ev u16        00B06A42  call sub_B02DF0   (lea ecx,[edi+2Ah] @00B06A3D)
; +0x2C rate_vslocal_clan u16       00B06A53  call sub_B02DF0   (lea edx,[edi+2Ch] @00B06A4E)
; +0x30 level_point      u32        00B06A64  call sub_B02DD0   (lea eax,[edi+30h] @00B06A5F)
; +0x34 avatar           18B        00B06A75  call sub_B068B0   (lea ecx,[edi+34h] @00B06A70)
; +0x4C clan_id          u32        00B06A86  call sub_B02DD0   (lea edx,[edi+4Ch] @00B06A81)
; +0x50 clan_name        char[31]   00B06AA6  call sub_B06230   (循环 cmp ebx,1Fh @00B06ABC)
; +0x6F clan_emb_base    i8         00B06AC3  call sub_B06230   (lea ecx,[edi+6Fh] @00B06ABE)
; +0x70 clan_emb_parts1  i8         00B06AD8  call sub_B06230   (lea edx,[edi+70h] @00B06AD3)
; +0x71 clan_emb_parts2  i8         00B06AED  call sub_B06230   (lea eax,[edi+71h] @00B06AE8)
; +0x74 cupteam_id       u32        00B06B02  call sub_B02DD0   (lea ecx,[edi+74h] @00B06AFD)
; +0x78 cupteam_name     char[31]   00B06B16  call sub_B06230   (循环 cmp ebx,1Fh @00B06B25)
; +0x98 accum_point      u32        00B06B32  call sub_B02DD0   (lea eax,[edi+98h] @00B06B2A)
; +0x9C rank             u32        00B06B46  call sub_B02DD0   (lea ecx,[edi+9Ch] @00B06B3E)
; +0xA0 base_accump      u32        00B06B5A  call sub_B02DD0   (lea edx,[edi+0A0h] @00B06B52)
; +0xA4 req_accump       u32        00B06B6E  call sub_B02DD0   (lea eax,[edi+0A4h] @00B06B66)
; +0xA8 penalty          u32        00B06B88  call sub_B02DD0   (add edi,0A8h @00B06B81)

; 读原语宽度（同批共用）：
;   sub_B02DD0: lea edx,[ecx+4] / jbe → mov ecx,[ecx] / mov [edx],ecx   ⇒ u32
;   sub_B02DF0: lea edx,[ecx+2] / jbe → mov cx,[ecx]  / mov [edx],cx    ⇒ u16
;   sub_B06230: lea edx,[ecx+1] / jbe → mov cl,[ecx]  / mov [edx],cl    ⇒ u8
;   sub_B068B0: u32 + u8×3 + u16 + u32 + u8×3 + u16                      ⇒ 18B（avatar）

; 写入器 sub_B06360 与之同序同偏移（对照点）：
;   +0x00 mov [eax],edx / +0x04 循环 25 / +0x1D mov [ecx],dl / +0x20 mov dx,[edi+20h]
;   +0x24 mov edx,[edi+24h] / +0x28,+0x2A,+0x2C call sub_B02DA0（写 u16）
;   +0x30 call sub_B02D80（写 u32）/ +0x34 call sub_B06290（写 avatar）/ +0x4C call sub_B02D80
;   +0x50 循环 1Fh call sub_B061C0（写 u8）… 直至 +0xA8
```

元素线长 = 4+25+1+1+1+2+4 + 2+2+2+4+18+4+31+1+1+1+4+31 + 4×5 = **159**；
内存跨度 `0xAC`（172，含 avatar 由 18B 补到 24B 与 u32 对齐），缓冲槽步进 `0xB0`（176）。

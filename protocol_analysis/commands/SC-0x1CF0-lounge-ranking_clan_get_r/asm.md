# 汇编证据 —— SC-0x1CF0-lounge-ranking_clan_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2BDC` @ `0xB56F1C`）

```asm
; VA: 0xB56F00 .. （块入口，含守卫与容量申请）
00B56F00  push    1F5h
00B56F05  mov     ecx, esi
00B56F07  call    sub_B41120
00B56F0C  test    al, al
00B56F0E  jz      loc_B890FE
00B56F14  mov     ecx, [esi+0Ch]
00B56F17  mov     eax, [ecx]
00B56F19  mov     edx, [eax+78h]
00B56F1C  push    2BDCh
00B56F21  call    edx
00B56F23  mov     [esp+2C5Ch+var_2C28], eax
00B56F27  mov     eax, [esi+0Ch]
00B56F2A  push    eax
00B56F2B  lea     ecx, [esp+2C60h+var_2BB8]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB56F5A 附近（查询结果码）
00B56F50  mov     eax, [esp+2C5Ch+var_2C08]
00B56F54  lea     edx, [esp+2C5Ch+var_2C44]
00B56F58  push    edx
00B56F59  push    eax
00B56F5A  call    sub_B02DD0
00B56F5F  add     esp, 8
00B56F62  test    al, al
00B56F64  jnz     short loc_B56F82
00B56F66  mov     edx, [esi]
00B56F68  mov     eax, [edx+64h]
```

## E3 字段 2：`order`（u16[5]，偏移 4，长度 10）

```asm
; VA: 0x0xB56F9A 附近（排序字段组（5×u16；缓冲槽步进 10））
00B56F90  mov     eax, [esp+2C5Ch+var_2C0C]
00B56F94  lea     edx, [esp+2C5Ch+var_2C44]
00B56F98  push    edx
00B56F99  push    eax
00B56F9A  call    sub_B46420
00B56F9F  add     esp, 8
00B56FA2  test    al, al
00B56FA4  jz      short loc_B56F66
00B56FA6  lea     ecx, [esp+2C5Ch+var_2C28]
00B56FAA  push    ecx
```

## E4 字段 3：`rankself`（u64，偏移 14，长度 8）

```asm
; VA: 0x0xB56FBE 附近（自身战队名次/唯一 ID）
00B56FB4  mov     eax, [esp+2C5Ch+var_2C30]
00B56FB8  lea     edx, [esp+2C5Ch+var_2C44]
00B56FBC  push    edx
00B56FBD  push    eax
00B56FBE  call    sub_B434B0
00B56FC3  add     esp, 8
00B56FC6  test    al, al
00B56FC8  jz      short loc_B56F66
00B56FCA  lea     ecx, [esp+2C5Ch+var_2C28]
00B56FCE  push    ecx
```

## E5 字段 4：`page_now`（u32，偏移 22，长度 4）

```asm
; VA: 0x0xB56FE2 附近（当前页号）
00B56FD8  mov     eax, [esp+2C5Ch+var_2C34]
00B56FDC  lea     edx, [esp+2C5Ch+var_2C44]
00B56FE0  push    edx
00B56FE1  push    eax
00B56FE2  call    sub_B02DD0
00B56FE7  add     esp, 8
00B56FEA  test    al, al
00B56FEC  jz      loc_B56F66
00B56FF2  lea     ecx, [esp+2C5Ch+var_2C28]
00B56FF6  push    ecx
```

## E6 字段 5：`page_max`（u32，偏移 26，长度 4）

```asm
; VA: 0x0xB5700A 附近（总页数）
00B57000  mov     eax, [esp+2C5Ch+var_2C38]
00B57004  lea     edx, [esp+2C5Ch+var_2C44]
00B57008  push    edx
00B57009  push    eax
00B5700A  call    sub_B02DD0
00B5700F  add     esp, 8
00B57012  test    al, al
00B57014  jz      loc_B56F66
00B5701A  lea     ecx, [esp+2C5Ch+var_2C44]
00B5701E  push    ecx
```

## E7 字段 6：`ranking_num`（u32，偏移 30，长度 4）

```asm
; VA: 0x0xB57024 附近（排行榜条目数 N）
00B5701A  lea     ecx, [esp+2C5Ch+var_2C44]
00B5701E  push    ecx
00B5701F  lea     edx, [esp+2C60h+var_2C20]
00B57023  push    edx
00B57024  call    sub_B02DD0
00B57029  add     esp, 8
00B5702C  test    al, al
00B5702E  jnz     short loc_B5704C
00B57030  mov     eax, [esi]
00B57032  mov     edx, [eax+64h]
```

## E8 字段 7：`ranking`（array<`clan_ranking_entry`,N>，偏移 34，长度 99·N）

```asm
; VA: 0x0xB5707C 附近（战队排行榜（N ≤ 100；元素线上 99B / 槽步进 108B））
00B57072  mov     eax, [esp+2C5Ch+var_2C48]
00B57076  lea     edx, [esp+2C5Ch+var_2C44]
00B5707A  push    edx
00B5707B  push    eax
00B5707C  call    sub_B46690
00B57081  add     esp, 8
00B57084  test    al, al
00B57086  jz      short loc_B57096
00B57088  add     [esp+2C5Ch+var_2C48], 6Ch ; 'l'
00B5708D  add     edi, 1
```

**元素尾部（77 → 99 的 +22B）**：`sub_B46690` 在打印器列出并核对的那 11 个成员
（合计 77B，逐成员 VA 见 `clan_ranking_entry.json` 的 `0xB466AC`..`0xB4678A`）之后，
**同一趟**还读两个成员 —— `score`（u32 @+77，`0xB4678E`）与 `avatar`（18B @+81，
`0xB467A8`）。故元素线长 **99**（`+9` 对齐到 `sub_B41900` 的槽步进 `0x6C = 108`）。
本条不另贴反汇编：这两条的汇编已在 `db_design/schema/composites/clan_ranking_entry.json`
的 `asm_audit`（2026-09-22，`status: pass`，13/13 成员）里逐成员固化，此处只做指针引用，
避免抄写出第二种版本。

## E9 字段 8：`topclans_num`（u32，偏移 ?（数组后），长度 4）

```asm
; VA: 0x0xB570B0 附近（顶尖战队条目数 M）
00B570A6  lea     ecx, [esp+2C5Ch+var_2C44]
00B570AA  push    ecx
00B570AB  lea     edx, [esp+2C60h+var_2C2C]
00B570AF  push    edx
00B570B0  call    sub_B02DD0
00B570B5  add     esp, 8
00B570B8  test    al, al
00B570BA  jz      loc_B57030
00B570C0  cmp     [esp+2C5Ch+var_2C2C], 3
00B570C5  ja      loc_B57030
```

## E10 字段 9：`topclans`（array<`clan_ranking_entry`,N>，偏移 ?，长度 99·M）

```asm
; VA: 0x0xB570FA 附近（顶尖战队列表（M ≤ 3；元素线上 99B / 槽步进 108B））
00B570F0  mov     ecx, [esp+2C5Ch+var_2C48]
00B570F4  lea     eax, [esp+2C5Ch+var_2C44]
00B570F8  push    eax
00B570F9  push    ecx
00B570FA  call    sub_B46690
00B570FF  add     esp, 8
00B57102  test    al, al
00B57104  jz      short loc_B57116
00B57106  add     [esp+2C5Ch+var_2C48], 6Ch ; 'l'
00B5710B  add     edi, 1
```

## E11 字段 10：`term_str`（str，偏移 ?，长度 L+1）

```asm
; VA: 0x0xB5713F 附近（赛期（term）名称字符串（NUL 结尾））
00B57133  add     eax, 41h ; 'A'
00B57136  push    ecx
00B57137  mov     [esp+2C68h+var_2BFC], ecx
00B5713B  mov     [esp+2C68h+var_2C28], eax
00B5713F  call    sub_B02BA0
00B57144  add     esp, 0Ch
00B57147  test    al, al
00B57149  jz      loc_B57030
00B5714F  lea     eax, [esp+2C5Ch+var_2C28]
00B57153  push    eax
```

## E12 字段 11：`clan_kind`（u8，偏移 ?（末），长度 1）

```asm
; VA: 0x0xB57167 附近（战队类别）
00B5715D  mov     edx, [esp+2C5Ch+var_2C48]
00B57161  lea     ecx, [esp+2C5Ch+var_2C44]
00B57165  push    ecx
00B57166  push    edx
00B57167  call    sub_B06230
00B5716C  add     esp, 8
00B5716F  test    al, al
00B57171  jz      loc_B57030
00B57177  mov     eax, [esp+2C5Ch+var_2C44]
00B5717B  cmp     eax, [esp+2C5Ch+var_2C40]
```

## E13 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5717B
00B57166  push    edx
00B57167  call    sub_B06230
00B5716C  add     esp, 8
00B5716F  test    al, al
00B57171  jz      loc_B57030
00B57177  mov     eax, [esp+2C5Ch+var_2C44]
00B5717B  cmp     eax, [esp+2C5Ch+var_2C40]
00B5717F  mov     ecx, esi
00B57181  jz      short loc_B5719D
00B57183  mov     edx, [esi]
00B57185  mov     eax, [edx+64h]
00B57188  push    1
00B5718A  push    1F5h
00B5718F  call    eax
```

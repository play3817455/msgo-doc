"""一次性修补：把 SC-0x1D02 的 asm.md 从「E5..E12」改写成「E5 数组 + E6 元素 = pilot 159B」。

原 E6..E12 的汇编块是错的（都贴了块入口 `0xB574F1` 的同一段，不是 `sub_B06980` 的成员读取，
且把元素当成 7 个成员）。这里换成逐成员的真实读点。
"""

import pathlib

DIR = pathlib.Path(__file__).resolve().parents[1] / "commands" / "SC-0x1D02-lounge-channellobby_members_get_r"

TAIL = """## E5 字段 4：`pilots`（array<pilot>，偏移 12，元素线上 159B × N）

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
;   +0x00 mov [eax],edx / +0x04 循环 25 / +0x1DA mov [ecx],dl / +0x20 mov dx,[edi+20h]
;   +0x24 mov edx,[edi+24h] / +0x28,+0x2A,+0x2C call sub_B02DA0（写 u16）
;   +0x30 call sub_B02D80（写 u32）/ +0x34 call sub_B06290（写 avatar）/ +0x4C call sub_B02D80
;   +0x50 循环 1Fh call sub_B061C0（写 u8）… 直至 +0xA8
```

元素线长 = 4+25+1+1+1+2+4 + 2+2+2+4+18+4+31+1+1+1+4+31 + 4×5 = **159**；
内存跨度 `0xAC`（172，含 avatar 由 18B 补到 24B 与 u32 对齐），缓冲槽步进 `0xB0`（176）。
"""


def main() -> None:
    path = DIR / "asm.md"
    text = path.read_text(encoding="utf-8")
    cut = text.index("## E5 ")
    path.write_text(text[:cut] + TAIL, encoding="utf-8", newline="\n")
    print(path.read_text(encoding="utf-8")[-1200:])


if __name__ == "__main__":
    main()

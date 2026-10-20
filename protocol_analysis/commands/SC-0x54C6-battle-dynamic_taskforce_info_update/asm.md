# 汇编证据 —— SC-0x54C6-battle-dynamic_taskforce_info_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1AB` @ `0xB179F4`）

```asm
; VA: 0xB179F4（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB179F4  push    0x1AB          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— order_all_number：偏移 0，长度 54，线类型 u8[54]（全部指令编号（**定长数组**，无线上计数；预留 `sub_B060E0` 一次推进 `0x36`=54，循环上界字面量 `cmp edi,36h`@`0xB17A48`））
0xB17A23  call    sub_B06230     ; u8[54]
; 块内日志格式串 "order_all_number=" → 含义锚点：0xB17D27

; 字段 2 —— order_all_kind：偏移 54，长度 54，线类型 u8[54]（全部指令种类（定长 54，`cmp edi,36h`@`0xB17A8B`））
0xB17A68  call    sub_B06230     ; u8[54]
; 块内日志格式串 "order_all_kind=" → 含义锚点：0xB17D84

; 字段 3 —— order_all_param：偏移 108，长度 216，线类型 u32[54]（全部指令参数（定长 54×u32；预留 `sub_B06100` 推进 `0xD8`=216，`cmp edi,36h`@`0xB17ACE`））
0xB17AAB  call    sub_B02DD0     ; u32[54]
; 块内日志格式串 "order_all_param=" → 含义锚点：0xB17DE2

; 字段 4 —— members_order_idx：偏移 324，长度 51，线类型 u8[51]（成员指令序号（定长 51；预留 `sub_B06120` 推进 `0x33`=51，`cmp edi,33h`@`0xB17B18`））
0xB17AEE  call    sub_B06230     ; u8[51]
; 块内日志格式串 "members_order_idx=" → 含义锚点：0xB17E41

; 字段 5 —— npc_entid_count：偏移 375，长度 4，线类型 u32（NPC 实体 ID 个数（上限 `0xC`=12，`cmp ebx,0Ch`@`0xB17B65`））
0xB17B39  call    sub_B02DD0     ; u32
; 块内日志格式串 "npc_entid_count=" → 含义锚点：0xB17EA0

; 字段 6 —— npc_entid[]：偏移 379，长度 2N，线类型 array<u16>（NPC 实体 ID 列表（元素 2B / 槽步进 2B，预留 `sub_B05E40`））
0xB17B74  call    复合读取器（元素/结构体，见 notes.md）     ; array<u16>
; 块内日志格式串 "npc_entid[]=" → 含义锚点：0xB17EA0

; 字段 7 —— npc_order_index_count：偏移 （浮动），长度 4，线类型 u32（NPC 指令序号个数（上限 `0xC`=12，`cmp ebx,0Ch`@`0xB17BF1`））
0xB17BC5  call    sub_B02DD0     ; u32
; 块内日志格式串 "npc_order_index_count=" → 含义锚点：0xB17F10

; 字段 8 —— npc_order_index[]：偏移 （浮动），长度 N，线类型 array<u8>（NPC 指令序号列表（元素 1B / 槽步进 1B，预留 `sub_B05EA0`））
0xB17C00  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "npc_order_index[]=" → 含义锚点：0xB17F10

; 字段 9 —— party_worldid：偏移 （浮动），长度 4，线类型 u32（队伍所属世界 ID）
0xB17C58  call    sub_B02DD0     ; u32
; 块内日志格式串 "party_worldid=" → 含义锚点：0xB17F90

; 字段 10 —— party_pilotid：偏移 （浮动），长度 4，线类型 u32（队伍飞行员 ID）
0xB17C80  call    sub_B02DD0     ; u32
; 块内日志格式串 "party_pilotid=" → 含义锚点：0xB17FB5

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB17C94
0xB17C94  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB17C94  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1803B
0xB1803B  mov     <reg>, [obj]; mov <reg>, [<reg>+0x2FCh]
;       call    <reg>          ; vt[0x2FC]（10 实参）
```

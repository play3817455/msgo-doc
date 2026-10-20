# 汇编证据 —— SC-0x8669-lounge-dailycup_team_info_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB38` @ `B6A968`）

```asm
; VA: B6A968（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6A968  push    0xB38          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B6A9A6  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6AB47 → 含义锚点

; 字段 2 —— team_id：偏移 4，长度 4，线类型 u32（队伍 ID（日志串 `team_id=`））
B6A9E6  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6AB71 → 含义锚点

; 字段 3 —— troops：偏移 8，长度 4，线类型 u32（部队编号（日志串 `troops=`））
B6AA0A  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6AB9B → 含义锚点

; 字段 4 —— pilots_count：偏移 12，长度 4，线类型 u32（队伍成员数（日志串 `pilots={`；上限 51：`cmp ebx,33h; ja` @`0xB6AA4C`））
B6AA20  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6ABB6 → 含义锚点

; 字段 5 —— pilots：偏移 16，长度 ，线类型 array<pilot,N>（队伍成员数组）
B6AA7A  call    sub_B470B0     ; 读取 array<pilot,N>
; 块内日志格式串 @B6ABB6 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6AAA8
B6AAA8  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6AC67 —— `vt[0x564]`（5 实参）
B6AC67  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x564h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B419E0（阵列预留，槽步进 0x38=56）：add dword ptr [edx],38h @0xB41A00
; sub_B470B0（pilots 元素读取器，整函数）：4 + 25×1 + 1 + 18(sub_B068B0) = 48
;    （字面量循环 25：cmp ecx,19h @0xB470E8）
; 上限检查 cmp ebx,33h; ja @0xB6AA4C ⇒ 51
```

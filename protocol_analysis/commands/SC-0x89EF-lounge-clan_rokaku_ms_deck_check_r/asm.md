# 汇编证据 —— SC-0x89EF-lounge-clan_rokaku_ms_deck_check_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x18` @ `B6B30E`）

```asm
; VA: B6B30E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B6B30E  push    0x18          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— rokaku_pt：偏移 0，长度 4，线类型 u32（楼阁点数（日志串 `rokaku_pt=`））
B6B349  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6B4A7 → 含义锚点

; 字段 2 —— deck_msid_count：偏移 4，长度 4，线类型 u32（机体卡组条数（日志串 `deck_msid={`；上限 2：`cmp ebx,2; ja` @`0xB6B3A7`））
B6B37B  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B6B4C2 → 含义锚点

; 字段 3 —— deck_msid：偏移 8，长度 ，线类型 array<u64,N>（机体唯一 ID 卡组）
B6B3DA  call    sub_B06200     ; 读取 array<u64,N>
; 块内日志格式串 @B6B4C2 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6B408
B6B408  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6B56E —— `vt[0x498]`（3 实参）
B6B56E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x498h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B41690（阵列预留，槽步进 8）：add dword ptr [edx],8 @0xB416B0
; 元素读取 call sub_B06200（u64，游标 +8）@0xB6B3DA；循环步进 add [esp+2C5Ch+var_2C48],8 @0xB6B3E6
; 上限检查 cmp ebx,2; ja @0xB6B3A7 ⇒ 2
```

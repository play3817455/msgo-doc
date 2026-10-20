# 汇编证据 —— SC-0x8295-lounge-byword_rate_get

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1004` @ `B69E46`）

```asm
; VA: B69E46（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B69E46  push    0x1004          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— world_id：偏移 0，长度 4，线类型 u32（世界 ID（日志串 `world_id=`））
B69E84  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B69F95 → 含义锚点

; 字段 2 —— rate_ary：偏移 4，长度 4096，线类型 f32[1024]（称号/流行语达成率表（固定 1024 个单精度浮点；日志串 `rate_ary={`））
B69EC6  call    sub_B06250 ×1024     ; 读取 f32[1024]
; 块内日志格式串 @B69FB0 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B69EF6
B69EF6  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B6A04D —— `vt[0x5D0]`（2 实参）
B6A04D  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x5D0h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B06250（f32 读原语）：lea edx,[ecx+4]; cmp edx,[eax+4]; jbe; fld dword ptr [ecx]; fstp dword ptr [dst]; add dword ptr [eax],4 ⇒ 消费 4（0xB06250..0xB0626F）
; sub_B41AA0（阵列预留，不形如 add [mem],IMM）：mov edx,[ecx]; add edx,1000h; mov [ecx],edx ⇒ 推进 4096（0xB41AA0..0xB41AB7）
; 循环上界字面量 0x400=1024：cmp edi,400h @0xB69ED8；元素读取 call sub_B06250 @0xB69EC6
```

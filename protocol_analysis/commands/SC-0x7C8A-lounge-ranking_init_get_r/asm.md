# 汇编证据 —— SC-0x7C8A-lounge-ranking_init_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x28` @ `B68926`）

```asm
; VA: B68926（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B68926  push    0x28          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— is_revoked：偏移 0，长度 4，线类型 u32（名次是否被吊销（日志串 `is_revoked=`））
B68961  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68B30 → 含义锚点

; 字段 2 —— high_scores_count：偏移 4，长度 4，线类型 u32（高分列表计数（上限 7：`cmp ebx,7` @`0xB689BF`））
B68993  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68B4B → 含义锚点

; 字段 3 —— high_scores：偏移 8，长度 ，线类型 array<u16,N1>（高分列表（日志串 `high_scores={`））
B689CE  call    sub_B05E40 + sub_B02DF0     ; 读取 array<u16,N1>
; 块内日志格式串 @B68B4B → 含义锚点

; 字段 4 —— event_scores_count：偏移 ，长度 4，线类型 u32（活动分列表计数（上限 7：`cmp ebx,7` @`0xB68A33`））
B68A1F  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68BC0 → 含义锚点

; 字段 5 —— event_scores：偏移 ，长度 ，线类型 array<u16,N2>（活动分列表（日志串 `event_scores={`））
B68A46  call    sub_B05E40 + sub_B02DF0     ; 读取 array<u16,N2>
; 块内日志格式串 @B68BC0 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68A91
B68A91  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B68C6A —— `vt[0x4A8]`（5 实参）
B68C6A  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x4A8h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; sub_B05E40（u16 阵列预留）：`add [ecx],2` × count（0xB05E40..0xB05E6E）
; 两处上限检查：cmp ebx,7 @0xB689BF（high_scores 计数）、cmp ebx,7 @0xB68A33（event_scores 计数）
; 元素读取：call sub_B02DF0 @0xB689EB、@0xB68A63；循环步进 add [esp+2C5Ch+var_2C48],2
```

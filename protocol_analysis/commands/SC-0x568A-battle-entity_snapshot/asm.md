# 汇编证据 —— SC-0x568A-battle-entity_snapshot

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8F0C` @ `0xB18070`）

```asm
; VA: 0xB18070（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB18070  push    0x8F0C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— frame_count：偏移 0，长度 4，线类型 u32（帧计数）
0xB180AE  call    sub_B02DD0     ; u32
; 块内日志格式串 "frame_count=" → 含义锚点：0xB1821E

; 字段 2 —— remain_msec：偏移 4，长度 4，线类型 u32（剩余毫秒）
0xB180EB  call    sub_B02DD0     ; u32
; 块内日志格式串 "remain_msec=" → 含义锚点：0xB18248

; 字段 3 —— snapshot_count：偏移 8，长度 4，线类型 u32（快照条数（上限 `0x340`=832，`cmp ebx,340h`@`0xB1812A`））
0xB18101  call    sub_B02DD0     ; u32
; 块内日志格式串 "snapshot_count=" → 含义锚点：0xB18263

; 字段 4 —— snapshots[]：偏移 12，长度 39，线类型 array<snapshot>（实体快照数组（元素线长 39 / 槽步进 `0x2C`=44，预留 `sub_B06030`））
0xB1813C  call    复合读取器（元素/结构体，见 notes.md）     ; array<snapshot>
; 块内日志格式串 "snapshots[]=" → 含义锚点：0xB18263

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB18185
0xB18185  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB18185  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1832B
0xB1832B  mov     <reg>, [obj]; mov <reg>, [<reg>+0x180h]
;       call    <reg>          ; vt[0x180]（4 实参）
```

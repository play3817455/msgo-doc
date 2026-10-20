# 汇编证据 —— SC-0x5A2F-lounge-friend_list_get_detail_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3398` @ `0xB6310A`）

```asm
; VA: 0xB6310A（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB6310A  push    0x3398          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB63148  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB632AA

; 字段 2 —— friend_count：偏移 4，长度 4，线类型 u32（好友条数（上限 `0x64`=100，`cmp ebx,64h`@`0xB631A6`））
0xB6317A  call    sub_B02DD0     ; u32
; 块内日志格式串 "friend_count=" → 含义锚点：0xB632C5

; 字段 3 —— friend_details[]：偏移 8，长度 113，线类型 array<friend_detail>（好友详情数组（元素线长 113 / 槽步进 `0x84`=132，预留 `sub_B415D0`））
0xB631B5  call    复合读取器（元素/结构体，见 notes.md）     ; array<friend_detail>
; 块内日志格式串 "friend_details[]=" → 含义锚点：0xB632C5

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB6320B
0xB6320B  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB6320B  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB63385
0xB63385  mov     <reg>, [obj]; mov <reg>, [<reg>+0x358h]
;       call    <reg>          ; vt[0x358]（3 实参）
```

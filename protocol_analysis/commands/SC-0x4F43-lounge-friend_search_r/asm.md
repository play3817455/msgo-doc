# 汇编证据 —— SC-0x4F43-lounge-friend_search_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19D0` @ `0xB5F829`）

```asm
; VA: 0xB5F829（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5F829  push    0x19D0          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5F867  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB5F9C1

; 字段 2 —— friend_count：偏移 4，长度 4，线类型 u32（好友条数（上限 `0x32`=50，`cmp ebx,32h`@`0xB5F8C5`））
0xB5F899  call    sub_B02DD0     ; u32
; 块内日志格式串 "friend_count=" → 含义锚点：0xB5F9DC

; 字段 3 —— friend_details[]：偏移 8，长度 113，线类型 array<friend_detail>（好友详情数组（元素线长 113 / 槽步进 `0x84`=132，预留 `sub_B415D0`））
0xB5F8D4  call    复合读取器（元素/结构体，见 notes.md）     ; array<friend_detail>
; 块内日志格式串 "friend_details[]=" → 含义锚点：0xB5F9DC

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5F922
0xB5F922  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB5F922  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5FA9B
0xB5FA9B  mov     <reg>, [obj]; mov <reg>, [<reg>+0x36Ch]
;       call    <reg>          ; vt[0x36C]（3 实参）
```

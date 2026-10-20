# 汇编证据 —— SC-0x530D-lounge-adop_ignore_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7D4` @ `0xB611E9`）

```asm
; VA: 0xB611E9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB611E9  push    0x7D4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ignore_count：偏移 0，长度 4，线类型 u32（忽略名单条数（上限 `0x1F4`=500，`cmp ebx,1F4h`@`0xB61242`））
0xB61219  call    sub_B02DD0     ; u32
; 块内日志格式串 "ignore_count=" → 含义锚点：0xB61329

; 字段 2 —— ignore_list[]：偏移 4，长度 4N，线类型 array<u32>（忽略名单（元素 4B / 槽步进 4B，预留 `sub_B41850`））
0xB61254  call    复合读取器（元素/结构体，见 notes.md）     ; array<u32>
; 块内日志格式串 "ignore_list[]=" → 含义锚点：0xB61329

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB6129C
0xB6129C  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB6129C  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB613D6
0xB613D6  mov     <reg>, [obj]; mov <reg>, [<reg>+0x80h]
;       call    <reg>          ; vt[0x80]（2 实参）
```

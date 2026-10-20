# 汇编证据 —— SC-0x54AF-lounge-present_add_dialog_show

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xCD` @ `0xB61A68`）

```asm
; VA: 0xB61A68（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB61A68  push    0xCD          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— attach_type：偏移 0，长度 4，线类型 u32（附件类型）
0xB61AA6  call    sub_B02DD0     ; u32
; 块内日志格式串 "attach_type=" → 含义锚点：0xB61BD4

; 字段 2 —— attach_id：偏移 4，长度 4，线类型 u32（附件 ID）
0xB61AE6  call    sub_B02DD0     ; u32
; 块内日志格式串 "attach_id=" → 含义锚点：0xB61BFE

; 字段 3 —— amount：偏移 8，长度 4，线类型 u32（数量）
0xB61B0A  call    sub_B02DD0     ; u32
; 块内日志格式串 "amount=" → 含义锚点：0xB61C28

; 字段 4 —— message：偏移 12，长度 193，线类型 str（赠送留言（槽位预算 `0xC1`=193））
0xB61B25  call    sub_B02BA0     ; str
; 块内日志格式串 "message=" → 含义锚点：0xB61C50

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB61B51
0xB61B51  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB61B51  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB61CC7
0xB61CC7  mov     <reg>, [obj]; mov <reg>, [<reg>+0x3A4h]
;       call    <reg>          ; vt[0x3A4]（4 实参）
```
